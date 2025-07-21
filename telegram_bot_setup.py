#!/usr/bin/env python3
"""
🔮 COSMIC OMNI-BRAIN AI - TELEGRAM BOT SETUP WIZARD
Automated setup for Telegram integration
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

class TelegramSetupWizard:
    def __init__(self):
        self.bot_token = None
        self.chat_id = None
        
    def display_banner(self):
        print("🔮" * 50)
        print("🔮 COSMIC OMNI-BRAIN AI - TELEGRAM SETUP WIZARD 🔮")
        print("🔮" * 50)
        print()
        
    def create_bot_instructions(self):
        print("📱 STEP 1: CREATE TELEGRAM BOT")
        print("=" * 40)
        print("1. Open Telegram and search for: @BotFather")
        print("2. Start a chat with BotFather")
        print("3. Send command: /newbot")
        print("4. Choose bot name: COSMIC OMNI-BRAIN SIGNALS")
        print("5. Choose username: cosmic_omni_brain_signals_bot")
        print("   (or similar if taken)")
        print("6. BotFather will give you a token like:")
        print("   123456789:ABCdefGhIJklmnoPQrstuvwxyz")
        print()
        print("⚠️  IMPORTANT: This should start with numbers, not 'eyJ'")
        print("    The token you provided appears to be a Supabase token")
        print()
        
    def get_bot_token(self):
        while True:
            token = input("🤖 Enter your Telegram Bot Token: ").strip()
            
            if not token:
                print("❌ Token cannot be empty!")
                continue
                
            if token.startswith('eyJ'):
                print("❌ This looks like a JWT/Supabase token!")
                print("   Please get the Telegram bot token from @BotFather")
                continue
                
            if ':' not in token or len(token) < 35:
                print("❌ Invalid format! Telegram tokens look like: 123456789:ABC...")
                continue
                
            # Test the token
            test_url = f"https://api.telegram.org/bot{token}/getMe"
            try:
                response = requests.get(test_url, timeout=10)
                if response.status_code == 200:
                    bot_info = response.json()
                    if bot_info.get('ok'):
                        print(f"✅ Bot token valid! Bot name: {bot_info['result']['first_name']}")
                        self.bot_token = token
                        return token
                    else:
                        print("❌ Token validation failed!")
                else:
                    print("❌ Invalid token - please check and try again")
            except requests.RequestException:
                print("❌ Network error - please check your connection")
                
    def get_chat_id_instructions(self):
        print("\n📱 STEP 2: GET YOUR CHAT ID")
        print("=" * 40)
        print("1. Start a chat with your bot")
        print("2. Send any message to your bot")
        print("3. Visit this URL in your browser:")
        print(f"   https://api.telegram.org/bot{self.bot_token}/getUpdates")
        print("4. Look for 'chat':{'id': NUMBER}")
        print("5. The number is your Chat ID")
        print()
        
    def get_chat_id(self):
        self.get_chat_id_instructions()
        
        while True:
            chat_id = input("💬 Enter your Chat ID: ").strip()
            
            if not chat_id:
                print("❌ Chat ID cannot be empty!")
                continue
                
            try:
                chat_id = int(chat_id)
                
                # Test sending a message
                test_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                test_data = {
                    'chat_id': chat_id,
                    'text': '🔮 COSMIC OMNI-BRAIN AI Test Message!\n\nIf you see this, your setup is working! 🚀'
                }
                
                response = requests.post(test_url, data=test_data, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('ok'):
                        print("✅ Chat ID valid! Test message sent successfully!")
                        self.chat_id = str(chat_id)
                        return str(chat_id)
                    else:
                        print("❌ Failed to send test message. Check Chat ID.")
                else:
                    print("❌ Invalid Chat ID or bot can't send messages to you")
                    print("   Make sure you've started a chat with your bot first!")
                    
            except ValueError:
                print("❌ Chat ID must be a number!")
            except requests.RequestException:
                print("❌ Network error - please check your connection")
                
    def create_env_file(self):
        env_content = f"""# 🔮 COSMIC OMNI-BRAIN AI - Environment Configuration

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={self.bot_token}
TELEGRAM_CHAT_ID={self.chat_id}

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=cosmic_omni_brain_secret_key_ultra_secure

# AI Configuration
AI_CONFIDENCE_THRESHOLD=75
MANIPULATION_RISK_THRESHOLD=60
CLEANUP_INTERVAL_HOURS=24

# Timezone
TIMEZONE=Asia/Dhaka
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
            
        print("✅ Environment file created: .env")
        
    def create_docker_env(self):
        docker_env = f"""TELEGRAM_BOT_TOKEN={self.bot_token}
TELEGRAM_CHAT_ID={self.chat_id}
FLASK_ENV=production
"""
        
        with open('docker.env', 'w') as f:
            f.write(docker_env)
            
        print("✅ Docker environment file created: docker.env")
        
    def test_full_integration(self):
        print("\n🧪 TESTING FULL INTEGRATION...")
        print("=" * 40)
        
        # Send a comprehensive test signal
        test_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        test_signal = """🔮 COSMIC OMNI-BRAIN SIGNAL TEST

🕒 1M | {}
🎯 Signal: CALL (Test)
📖 Strategy: Integration Test
📊 Confidence: 99%
🧠 AI Logic: Testing Telegram integration - all systems operational!

⚖️ Market Health: 95%
🌀 Volatility: Low
📊 Trend: Bullish
🛡️ Manipulation Risk: 5%

🤖 Analysis by COSMIC OMNI-BRAIN AI v∞.UNBEATABLE
⚡ Integration test successful! Ready for live trading signals! 🚀""".format(
            datetime.now().strftime("%H:%M (UTC+6)")
        )
        
        test_data = {
            'chat_id': self.chat_id,
            'text': test_signal,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(test_url, data=test_data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print("✅ Full integration test successful!")
                    print("✅ You should see a test signal in your Telegram!")
                    return True
            print("❌ Integration test failed")
            return False
        except Exception as e:
            print(f"❌ Integration test error: {e}")
            return False
            
    def show_deployment_commands(self):
        print("\n🚀 DEPLOYMENT COMMANDS")
        print("=" * 40)
        print("🐳 DOCKER DEPLOYMENT:")
        print(f"   docker build -t cosmic-ai .")
        print(f"   docker run --env-file docker.env -p 5000:5000 cosmic-ai")
        print()
        print("☁️ HEROKU DEPLOYMENT:")
        print(f"   heroku config:set TELEGRAM_BOT_TOKEN={self.bot_token}")
        print(f"   heroku config:set TELEGRAM_CHAT_ID={self.chat_id}")
        print("   git push heroku main")
        print()
        print("⚡ VERCEL DEPLOYMENT:")
        print("   Add environment variables in Vercel dashboard:")
        print(f"   TELEGRAM_BOT_TOKEN = {self.bot_token}")
        print(f"   TELEGRAM_CHAT_ID = {self.chat_id}")
        print()
        print("🚄 RAILWAY DEPLOYMENT:")
        print("   Add environment variables in Railway dashboard")
        print()
        
    def save_config_summary(self):
        config = {
            "telegram_bot_token": self.bot_token,
            "telegram_chat_id": self.chat_id,
            "setup_completed": datetime.now().isoformat(),
            "deployment_ready": True
        }
        
        with open('cosmic_ai_config.json', 'w') as f:
            json.dump(config, f, indent=2)
            
        print("✅ Configuration saved: cosmic_ai_config.json")
        
    def run_setup(self):
        self.display_banner()
        
        print("🎯 This wizard will set up Telegram integration for your")
        print("   COSMIC OMNI-BRAIN AI signal delivery system!")
        print()
        
        # Step 1: Create bot
        self.create_bot_instructions()
        input("Press Enter when you have your bot token ready...")
        
        # Step 2: Get bot token
        self.get_bot_token()
        
        # Step 3: Get chat ID
        self.get_chat_id()
        
        # Step 4: Create configuration files
        print("\n⚙️ CREATING CONFIGURATION FILES...")
        print("=" * 40)
        self.create_env_file()
        self.create_docker_env()
        self.save_config_summary()
        
        # Step 5: Test integration
        self.test_full_integration()
        
        # Step 6: Show deployment commands
        self.show_deployment_commands()
        
        print("\n🎊 TELEGRAM SETUP COMPLETE! 🎊")
        print("=" * 40)
        print("✅ Bot token configured")
        print("✅ Chat ID configured") 
        print("✅ Environment files created")
        print("✅ Integration tested")
        print("✅ Ready for deployment!")
        print()
        print("🔮 Your COSMIC OMNI-BRAIN AI is now ready to send")
        print("   live trading signals directly to your Telegram! 🚀")

def main():
    try:
        wizard = TelegramSetupWizard()
        wizard.run_setup()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()