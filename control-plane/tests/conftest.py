import os

# The application module declares a default ASGI app at import time.
# Set a test-only key before importing it.
os.environ.setdefault("CONTROL_API_KEY", "development-test-key-not-secret")
