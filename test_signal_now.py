#!/usr/bin/env python3
"""
🔧 TELEGRAM SIGNAL TEST - SEND SIGNAL NOW!
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

def send_telegram_signal():
    """Send test signal to Telegram"""
    
    # Your Telegram credentials
    bot_token = "8173800058:AAEWDc9ocSz7Ohj1v62fjyA8LyJvMadl8NY"
    chat_id = "-1002793240027"
    
    # Create test signal message
    message = f"""🔮 <b>COSMIC AI TEST SIGNAL</b>

⏰ <b>{datetime.now().strftime('%H:%M:%S')} UTC+6</b>
🔥 <b>SIGNAL: CALL</b>
📊 <b>EUR/USD - Quotex</b>
🎯 <b>CONFIDENCE: 92%</b>

🧠 <b>STRATEGY:</b> Trap Fade Reversal
💡 <b>AI LOGIC:</b> Bullish breakout pattern detected

📈 <b>MARKET ANALYSIS:</b>
⚖️ Health: 87%
🌀 Volatility: Medium
🛡️ Risk: 23%

🤖 <b>COSMIC OMNI-BRAIN AI v∞.UNBEATABLE</b>
⚡ <i>Test signal - Bot is working!</i> 🌌"""

    try:
        # Telegram API URL
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        # Data to send
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        # Encode data
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url, data=encoded_data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        print("🔮 SENDING TEST SIGNAL TO TELEGRAM...")
        print(f"📱 Chat ID: {chat_id}")
        print(f"🤖 Bot Token: {bot_token[:10]}...")
        
        # Send request
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        if result.get('ok'):
            print("✅ SUCCESS! Signal sent to Telegram!")
            print("📱 Check your Telegram chat now!")
            print(f"📨 Message ID: {result.get('result', {}).get('message_id', 'Unknown')}")
            return True
        else:
            print(f"❌ TELEGRAM ERROR: {result.get('description', 'Unknown error')}")
            print(f"🔍 Error Code: {result.get('error_code', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ PYTHON ERROR: {e}")
        return False

def check_bot_info():
    """Check if bot token is valid"""
    
    bot_token = "8173800058:AAEWDc9ocSz7Ohj1v62fjyA8LyJvMadl8NY"
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        if result.get('ok'):
            bot_info = result.get('result', {})
            print("✅ BOT TOKEN IS VALID!")
            print(f"🤖 Bot Name: {bot_info.get('first_name', 'Unknown')}")
            print(f"👤 Username: @{bot_info.get('username', 'Unknown')}")
            return True
        else:
            print(f"❌ INVALID BOT TOKEN: {result.get('description', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR CHECKING BOT: {e}")
        return False

def main():
    """Main function"""
    
    print("🔮" * 60)
    print("🔮" + " COSMIC AI TELEGRAM TEST ".center(58) + "🔮")
    print("🔮" * 60)
    
    # Step 1: Check bot token
    print("\n🔍 STEP 1: Checking bot token...")
    if not check_bot_info():
        print("❌ Bot token is invalid. Cannot send signals.")
        return
        
    # Step 2: Send test signal
    print("\n📱 STEP 2: Sending test signal...")
    if send_telegram_signal():
        print("\n🎊 SUCCESS! The bot is working!")
        print("📱 You should see the signal in your Telegram chat now!")
        print("✅ If you received the signal, the bot is ready!")
    else:
        print("\n❌ FAILED to send signal.")
        print("🔍 Possible issues:")
        print("   1. Chat ID might be wrong")
        print("   2. Bot not added to the chat")
        print("   3. Bot doesn't have permission to send messages")
        
    print("\n🔮 TEST COMPLETE!")

if __name__ == "__main__":
    main()