#!/usr/bin/env python3
"""
🔮 COSMIC OMNI-BRAIN AI v∞.UNBEATABLE - SMART LAUNCHER
Automatically detects environment and launches the AI optimally
"""

import os
import sys
import subprocess
import socket
import threading
import time
import webbrowser
from pathlib import Path

def check_port(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ['flask', 'cv2', 'numpy', 'PIL']
    missing = []
    
    for module in required_modules:
        try:
            if module == 'cv2':
                import cv2
            elif module == 'PIL':
                from PIL import Image
            else:
                __import__(module)
        except ImportError:
            missing.append(module)
    
    return missing

def try_install_dependencies():
    """Try to install dependencies with different methods"""
    methods = [
        ["pip", "install", "-r", "requirements.txt"],
        ["pip3", "install", "-r", "requirements.txt"],
        ["python", "-m", "pip", "install", "-r", "requirements.txt"],
        ["python3", "-m", "pip", "install", "-r", "requirements.txt"],
        ["pip", "install", "--user", "-r", "requirements.txt"],
        ["pip3", "install", "--user", "-r", "requirements.txt"]
    ]
    
    for method in methods:
        print(f"🔄 Trying: {' '.join(method)}")
        try:
            result = subprocess.run(method, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Dependencies installed successfully!")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    return False

def launch_demo_mode():
    """Launch the dependency-free demo version"""
    print("🎭 Launching COSMIC AI in DEMO MODE...")
    print("   (No external dependencies required)")
    
    try:
        subprocess.run([sys.executable, "demo_cosmic_ai.py"])
        return True
    except Exception as e:
        print(f"❌ Demo mode failed: {e}")
        return False

def launch_full_app():
    """Launch the full Flask application"""
    print("🚀 Launching COSMIC AI FULL APPLICATION...")
    
    try:
        # Import the app to test if dependencies work
        sys.path.insert(0, os.getcwd())
        from app import app, cosmic_ai
        
        print("✅ All AI modules loaded successfully!")
        print("🔮 COSMIC OMNI-BRAIN AI v∞.UNBEATABLE is ONLINE!")
        print("=" * 60)
        print("🌐 Web Interface: http://localhost:5000")
        print("📱 Telegram: Configure in TELEGRAM_SETUP.md")
        print("📊 Status: http://localhost:5000/status")
        print("🏥 Health: http://localhost:5000/health")
        print("=" * 60)
        
        # Open browser automatically
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Run the app
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to start full app: {e}")
        return False

def show_deployment_options():
    """Show cloud deployment options"""
    print("\n☁️ CLOUD DEPLOYMENT OPTIONS:")
    print("=" * 50)
    print("🐳 Docker: docker build -t cosmic-ai . && docker run -p 5000:5000 cosmic-ai")
    print("☁️ Heroku: git push heroku main")
    print("⚡ Vercel: vercel --prod")
    print("🚄 Railway: Connect GitHub repo")
    print("🎨 Render: Connect GitHub repo")
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")

def main():
    """Smart launcher main function"""
    print("🔮" * 20)
    print("🔮 COSMIC OMNI-BRAIN AI v∞.UNBEATABLE 🔮")
    print("🔮      SMART LAUNCHER ACTIVATED      🔮")
    print("🔮" * 20)
    
    # Check if port 5000 is available
    if not check_port(5000):
        print("⚠️ Port 5000 is already in use!")
        print("🔄 Checking if COSMIC AI is already running...")
        try:
            import requests
            response = requests.get('http://localhost:5000/health', timeout=5)
            if response.status_code == 200:
                print("✅ COSMIC AI is already running at http://localhost:5000")
                webbrowser.open('http://localhost:5000')
                return
        except:
            pass
        print("❌ Port 5000 blocked by another application")
        return
    
    # Strategy 1: Try full application with existing dependencies
    print("\n🎯 STRATEGY 1: Checking dependencies...")
    missing = check_dependencies()
    
    if not missing:
        print("✅ All dependencies available!")
        if launch_full_app():
            return
    
    # Strategy 2: Try to install dependencies
    print(f"\n🎯 STRATEGY 2: Installing missing dependencies: {missing}")
    if Path("requirements.txt").exists():
        if try_install_dependencies():
            print("🔄 Retrying full application...")
            if launch_full_app():
                return
    
    # Strategy 3: Demo mode
    print("\n🎯 STRATEGY 3: Launching demo mode...")
    if launch_demo_mode():
        show_deployment_options()
        return
    
    # Strategy 4: Show deployment options
    print("\n🎯 STRATEGY 4: Manual deployment")
    print("❌ Unable to launch locally due to environment restrictions")
    print("✅ All files are ready for cloud deployment!")
    show_deployment_options()
    
    print("\n🔮 COSMIC AI FILES READY:")
    files = [
        "app.py", "ai_core/", "templates/", "requirements.txt",
        "Dockerfile", "docker-compose.yml", "Procfile", "vercel.json"
    ]
    for file in files:
        if Path(file).exists():
            print(f"   ✅ {file}")
    
    print("\n💫 Ready to dominate binary options markets! 💫")

if __name__ == "__main__":
    main()