import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer

clerk_config = ClerkConfig(
    jwks_url=os.getenv(
        "CLERK_JWKS_URL",
        "https://splendid-toucan-17.clerk.accounts.dev/.well-known/jwks.json"))

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config, debug_mode=True)

#test_auth_guard = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(clerk_auth_guard),
) -> str:
    if not credentials or not credentials.decoded:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_id = credentials.decoded.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User id missing")

    return user_id


#def get_current_user_id_dev(
#    credentials: HTTPAuthorizationCredentials = Depends(test_auth_guard),
#) -> str:
#    """Development-only auth that accepts test tokens"""
#    if not credentials:
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
#
#    token = credentials.credentials
#
#    # Try test token first (in development)
#    if os.getenv("ENVIRONMENT", "development") != "production":
 #       try:
 #           secret = os.getenv("TEST_JWT_SECRET", "test_secret_key_for_development_only")
 #           decoded = jwt.decode(token, secret, algorithms=["HS256"])
 #           user_id = decoded.get("sub")
 #           if user_id:
 #               return user_id
#        except jwt.InvalidTokenError:
#            pass  # Fall through to Clerk auth
#
#    # Fall back to Clerk auth
#    try:
#        clerk_guard = ClerkHTTPBearer(config=clerk_config)
#        clerk_creds = clerk_guard(credentials)
#        if clerk_creds and clerk_creds.decoded:
     #       user_id = clerk_creds.decoded.get("sub")
    #        if user_id:
   #             return user_id
  #  except Exception:
 #       pass
#
#    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
