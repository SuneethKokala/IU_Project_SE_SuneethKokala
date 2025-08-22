#!/usr/bin/env python3

from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_whatsapp():
    try:
        # Get credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if not account_sid or not auth_token:
            print('❌ Twilio credentials not found in environment variables')
            return
        
        print(f"🔧 Testing Twilio WhatsApp...")
        print(f"📋 Account SID: {account_sid[:10]}...")
        print(f"🔑 Auth Token: {auth_token[:10]}...")
        
        # Create client
        client = Client(account_sid, auth_token)
        
        # Test message
        message = client.messages.create(
            body='🧪 Test message from Women Safety App',
            from_='whatsapp:+14155238886',
            to='whatsapp:+919902480636'
        )
        
        print(f"✅ SUCCESS!")
        print(f"📱 Message SID: {message.sid}")
        print(f"📊 Status: {message.status}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")
        
        # Common issues
        if "authenticate" in str(e).lower():
            print("\n🚨 AUTHENTICATION FAILED")
            print("1. Check your Account SID and Auth Token")
            print("2. Go to https://console.twilio.com/")
        elif "not a valid phone number" in str(e).lower():
            print("\n🚨 PHONE NUMBER ISSUE")
            print("1. Make sure phone number includes country code")
            print("2. Format: +919902480636")
        elif "sandbox" in str(e).lower() or "join" in str(e).lower():
            print("\n🚨 WHATSAPP SANDBOX NOT SET UP")
            print("1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
            print("2. Send 'join <code>' to +1 415 523 8886 from WhatsApp")
            print("3. Wait for confirmation message")

if __name__ == "__main__":
    test_whatsapp()