import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Loaded DATABASE_URL: {DATABASE_URL}")

if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    print("SUCCESS: Configured for PostgreSQL (Neon)")
else:
    print(f"WARNING: URL is '{DATABASE_URL}'. Defaults effectively to SQLite.")
