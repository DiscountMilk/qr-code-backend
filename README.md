# QR Code Backend

## Setup

Required environment variables:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `CLERK_JWKS_URL`

Install dependencies:

```zsh
pip install -r requirements.txt
```

Run the API:

```zsh
uvicorn app.main:app --reload
```
