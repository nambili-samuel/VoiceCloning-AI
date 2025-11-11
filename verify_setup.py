"""
Setup Verification Script
Run this to verify your installation is complete
"""

import os
import sys
import importlib

def check_imports():
    """Check if all required modules can be imported"""
    modules = [
        'torch',
        'librosa',
        'soundfile',
        'speech_recognition',
        'bark',
        'requests',
        'numpy',
        'pyaudio'
    ]
    
    print("🔍 Checking imports...")
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")

def check_directories():
    """Check if required directories exist"""
    directories = [
        'src',
        'config',
        'data/raw_audio',
        'data/processed_audio',
        'data/models',
        'examples',
        'training'
    ]
    
    print("\n📁 Checking directories...")
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/")

def check_files():
    """Check if required files exist"""
    files = [
        'src/voice_cloning.py',
        'src/ai_agent.py',
        'src/grok_client.py',
        'config/settings.py',
        'main.py',
        'requirements.txt'
    ]
    
    print("\n📄 Checking files...")
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")

def check_api_keys():
    """Check if API keys are set"""
    print("\n🔑 Checking API keys...")
    try:
        from config.api_keys import GROK_API_KEY
        if GROK_API_KEY and GROK_API_KEY != "your_grok_api_key_here":
            print("  ✅ Grok API key is set")
        else:
            print("  ❌ Grok API key not set")
    except ImportError:
        print("  ❌ API keys file not found")

def main():
    print("🚀 VoiceCloning AI - Setup Verification")
    print("=" * 50)
    
    check_imports()
    check_directories()
    check_files()
    check_api_keys()
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. If any ❌ appear above, run: python setup_project.py")
    print("2. Set your API keys in config/api_keys.py")
    print("3. Record your voice: python record_voice.py")
    print("4. Test the system: python main.py --run-agent")

if __name__ == "__main__":
    main()