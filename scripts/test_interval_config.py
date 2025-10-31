"""
Test script to verify CHECK_INTERVAL_SECONDS configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Get check interval
check_interval = int(os.getenv("CHECK_INTERVAL_SECONDS", "20"))

print("✅ Configuration Test")
print("=" * 50)
print(f"CHECK_INTERVAL_SECONDS from .env: {check_interval}")
print()

# Test different values
print("Examples:")
print(f"  Current value: Check every {check_interval} seconds")
print(f"  10 seconds = more responsive (more API calls)")
print(f"  30 seconds = balanced")
print(f"  60 seconds = conservative (fewer API calls)")
print()

print("To change, edit .env:")
print("  CHECK_INTERVAL_SECONDS=30")
