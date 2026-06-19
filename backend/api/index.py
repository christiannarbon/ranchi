# Vercel Python serverless entrypoint.
# Vercel's @vercel/python runtime detects the exported ASGI `app` and serves it.
from main import app  # noqa: F401
