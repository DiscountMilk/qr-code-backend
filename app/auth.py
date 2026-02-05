from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import requests
from jwt.algorithms import RSAAlgorithm
import json
import jwt
import os

security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Validiert JWT Token mit Clerk JWKS (inkl. Signatur-Prüfung)"""
    token = credentials.credentials

    try:
        # Hole JWKS von Clerk (ohne SSL-Verifizierung für lokale Entwicklung)
        jwks_url = os.getenv("CLERK_JWKS_URL")
        response = requests.get(jwks_url, verify=False)
        response.raise_for_status()
        jwks = response.json()

        # Dekodiere Token Header um kid zu bekommen
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        if not kid:
            raise HTTPException(status_code=401, detail="No kid in token header")

        # Finde den passenden Key im JWKS
        public_key = None
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                public_key = RSAAlgorithm.from_jwk(json.dumps(key))
                break

        if not public_key:
            raise HTTPException(status_code=401, detail=f"Public key not found for kid: {kid}")

        # Dekodiere und validiere den Token
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
            }
        )

        user_id = decoded.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found in token")

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")