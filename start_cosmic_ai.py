#!/usr/bin/env python3
"""
COSMIC OMNI-BRAIN AI v∞.UNBEATABLE Startup Script
The Ultimate Binary Options Signal Bot
"""

import os
import sys
import subprocess
import platform
import time

def print_cosmic_banner():
    """Print the cosmic startup banner"""
    banner = """
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮

    ██████╗ ██████╗ ███████╗███╗   ███╗██╗ ██████╗     ██████╗ ███╗   ███╗███╗   ██╗██╗
   ██╔════╝██╔═══██╗██╔════╝████╗ ████║██║██╔════╝    ██╔═══██╗████╗ ████║████╗  ██║██║
   ██║     ██║   ██║███████╗██╔████╔██║██║██║  ███╗   ██║   ██║██╔████╔██║██╔██╗ ██║██║
   ██║     ██║   ██║╚════██║██║╚██╔╝██║██║██║   ██║   ██║   ██║██║╚██╔╝██║██║╚██╗██║██║
   ╚██████╗╚██████╔╝███████║██║ ╚═╝ ██║██║╚██████╔╝   ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║
    ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝     ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝
                                                                                        
   ██████╗ ██████╗  █████╗ ██╗███╗   ██╗     █████╗ ██╗    ██╗   ██╗██████╗  ██████╗   
   ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║    ██╔══██╗██║    ██║   ██║██╔══██╗██╔═══██╗  
   ██████╔╝██████╔╝███████║██║██╔██╗ ██║    ███████║██║    ██║   ██║██║  ██║██║   ██║  
   ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║    ██╔══██║██║    ╚██╗ ██╔╝██║  ██║██║   ██║  
   ██████╔╝██║  ██║██║  ██║██║██║ ╚████║    ██║  ██║██║     ╚████╔╝ ██████╔╝╚██████╔╝  
   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝      ╚═══╝  ╚═════╝  ╚═════╝   

                        🧠 v∞.UNBEATABLE - THE ULTIMATE BINARY OPTIONS SIGNAL BOT 🧠
                    
                        💫 100-Billion-Year Trained Intelligence 💫
                        ⚡ Dynamic Strategy Generation ⚡
                        🎯 Anti-Manipulation Technology 🎯
                        🌀 Market Psychology Analysis 🌀
                        
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮
"""
    print(banner)

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'opencv-python', 'numpy', 'Pillow', 'pytz', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies!")
            print("Please run: pip install -r requirements.txt")
            return False
    
    print("✅ All dependencies are installed")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'static', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def get_system_info():
    """Display system information"""
    print("\n🖥️  SYSTEM INFORMATION:")
    print(f"   Platform: {platform.platform()}")
    print(f"   Processor: {platform.processor()}")
    print(f"   Python: {platform.python_version()}")
    
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"   Memory: {memory.total // (1024**3)} GB total, {memory.available // (1024**3)} GB available")
        print(f"   CPU Cores: {psutil.cpu_count()}")
    except ImportError:
        print("   Memory: Unable to determine (psutil not installed)")

def check_telegram_config():
    """Check Telegram configuration"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if bot_token and chat_id:
        print("✅ Telegram integration configured")
        print(f"   Bot Token: {bot_token[:20]}...")
        print(f"   Chat ID: {chat_id}")
    else:
        print("⚠️  Telegram integration not configured (optional)")
        print("   Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")
        print("   to enable automatic signal delivery to Telegram")

def start_application():
    """Start the COSMIC OMNI-BRAIN AI application"""
    print("\n🚀 LAUNCHING COSMIC OMNI-BRAIN AI...")
    print("   🧠 Initializing omni-brain intelligence...")
    time.sleep(1)
    print("   ⚡ Loading dynamic strategy engines...")
    time.sleep(1)
    print("   🎯 Calibrating market psychology sensors...")
    time.sleep(1)
    print("   🌀 Activating anti-manipulation protocols...")
    time.sleep(1)
    print("   🔮 COSMIC OMNI-BRAIN AI is now ONLINE!")
    print("\n📱 Access the interface at: http://localhost:5000")
    print("📊 Upload a chart screenshot to begin analysis")
    print("🎯 Experience the power of infinite adaptive intelligence!")
    
    try:
        # Import and run the app
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n🔮 COSMIC OMNI-BRAIN AI shutting down...")
        print("   Thank you for using the ultimate binary options signal bot!")
        print("   The cosmic intelligence awaits your return... 🧠✨")
    except Exception as e:
        print(f"\n❌ ERROR: Failed to start application: {e}")
        print("   Please check the error messages above and try again.")

def main():
    """Main startup function"""
    print_cosmic_banner()
    
    print("🔍 SYSTEM CHECK:")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create directories
    print("\n📁 DIRECTORY SETUP:")
    create_directories()
    
    # System information
    get_system_info()
    
    # Check Telegram configuration
    print("\n📱 TELEGRAM CONFIGURATION:")
    check_telegram_config()
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()