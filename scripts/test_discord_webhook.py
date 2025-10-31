"""
Test Discord webhook notification
"""

import os
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))


def send_test_notification(webhook_url):
    """Send a test notification to Discord"""
    
    if not webhook_url:
        print("❌ No webhook URL configured in .env")
        print("   Add DISCORD_WEBHOOK_URL to your .env file")
        return False
    
    print(f"📤 Sending test notification to Discord...")
    print(f"   Webhook: {webhook_url[:50]}...")
    
    embed = {
        "title": "🧪 Test Notification - SOL Trading Bot",
        "color": 0x5865F2,  # Discord blue
        "fields": [
            {
                "name": "Status",
                "value": "✅ Webhook is working correctly!",
                "inline": False
            },
            {
                "name": "Test Details",
                "value": "This is a test message from your SOL trading bot.\nYou will receive notifications here when trades are executed.",
                "inline": False
            }
        ],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "footer": {
            "text": "SOL Trading Bot - Test Message"
        }
    }
    
    payload = {
        "embeds": [embed]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            print("✅ Test notification sent successfully!")
            print("   Check your Discord channel for the message")
            return True
        else:
            print(f"❌ Failed to send notification")
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending notification: {str(e)}")
        return False


def main():
    """Test Discord webhook"""
    
    load_dotenv()
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    print("=" * 70)
    print("🧪 DISCORD WEBHOOK TEST")
    print("=" * 70)
    
    if send_test_notification(webhook_url):
        print("\n✅ SUCCESS - Discord notifications are configured correctly!")
    else:
        print("\n❌ FAILED - Please check your webhook URL in .env")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
