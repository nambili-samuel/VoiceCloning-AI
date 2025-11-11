import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    try:
        from src.voice_cloning import BarkVoiceCloner
        print("✓ BarkVoiceCloner imported successfully")
        
        from src.audio_processing import AudioProcessor
        print("✓ AudioProcessor imported successfully")
        
        from src.grok_client import GrokClient
        print("✓ GrokClient imported successfully")
        
        print("\nAll imports successful! You can now run:")
        print("python main.py --test-voice --speaker-name your_voice")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("\nTrying to install requirements...")
        
        # Try to install requirements
        try:
            from install_requirements import install_requirements
            install_requirements()
        except:
            print("Please run: python install_requirements.py")
        
        return False

if __name__ == "__main__":
    test_imports()