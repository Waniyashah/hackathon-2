from src.database.session import DATABASE_URL
import os
from dotenv import load_dotenv

print(f"Loaded DATABASE_URL: {DATABASE_URL}")

# Check if it starts with sqlite
if DATABASE_URL.startswith("sqlite"):
    print("WARNING: Using SQLite!")
else:
    print("SUCCESS: Using PostgreSQL!")
