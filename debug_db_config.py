"""
Debug script to check database connection configuration
Run this to verify your DATABASE_URL is correct
"""
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

print("=" * 80)
print("DATABASE CONFIGURATION DEBUG")
print("=" * 80)
print(f"\nDATABASE_URL set: {bool(database_url)}")

if database_url:
    # Mask the password for security
    if "@" in database_url:
        parts = database_url.split("@")
        masked = parts[0].rsplit(":", 1)[0] + ":***@" + parts[1]
    else:
        masked = database_url
    
    print(f"DATABASE_URL (masked): {masked}")
    print(f"\nParsing connection details:")
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        print(f"  Scheme: {parsed.scheme}")
        print(f"  Host: {parsed.hostname}")
        print(f"  Port: {parsed.port}")
        print(f"  Database: {parsed.path.lstrip('/')}")
        print(f"  Username: {parsed.username}")
        
        # Check for problematic hostnames
        if "postgres.railway.internal" in database_url:
            print("\n⚠️  WARNING: Using internal Railway hostname!")
            print("   This will NOT work from outside Railway's network.")
            print("   Use the PUBLIC_URL instead.")
        elif "autorack.proxy.rlwy.net" in database_url:
            print("\n✅ Using Railway's public proxy - looks good!")
        else:
            print(f"\n⚠️  Unusual hostname detected: {parsed.hostname}")
    except Exception as e:
        print(f"  Error parsing URL: {e}")
else:
    print("\n❌ DATABASE_URL not found in environment!")
    print("   Check that .env file exists and contains DATABASE_URL")

print("\n" + "=" * 80)
