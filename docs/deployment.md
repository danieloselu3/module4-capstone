<!-- Change for your project: env vars and health URL if renamed. Keep headings. -->
# Deployment

## Run locally
uvicorn services.<name>.app:app --port 8080

## Env vars
- OPENAI_API_KEY (optional; missing key routes to stub mode)

## Health
GET /health should return 200.

## Fallback
If cloud creds or Docker are missing, document the steps here as "not executed live".
