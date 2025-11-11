import subprocess
import sys
import os

def install_requirements():
    """Install all required packages"""
    
    requirements = [
        "torch>=2.0.0",
        "torchaudio>=2.0.0", 
        "numpy>=1.21.0",
        "librosa>=0.10.0",
        "soundfile>=0.12.0",
        "pydub>=0.25.1",
        "speechrecognition>=3.10.0",
        "transformers>=4.30.0",
        "openai-whisper>=20231117",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
        "pyaudio>=0.2.11",
        "scikit-learn>=1.2.0",
        "requests>=2.25.1",
    ]
    
    # Try to install Bark
    bark_commands = [
        "pip install suno-bark",
        "pip install git+https://github.com/suno-ai/bark.git",
    ]
    
    print("Installing main requirements...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
    
    print("\nInstalling Bark...")
    bark_installed = False
    for cmd in bark_commands:
        try:
            subprocess.check_call(cmd.split())
            print("✓ Bark installed successfully!")
            bark_installed = True
            break
        except subprocess.CalledProcessError:
            continue
    
    if not bark_installed:
        print("✗ Could not install Bark. Some features will be limited.")
        print("You can try manual installation:")
        print("pip install git+https://github.com/suno-ai/bark.git")
    
    # Create necessary directories
    os.makedirs("data/raw_audio", exist_ok=True)
    os.makedirs("data/processed_audio", exist_ok=True)
    os.makedirs("data/models", exist_ok=True)
    
    print("\nSetup completed!")

if __name__ == "__main__":
    install_requirements()