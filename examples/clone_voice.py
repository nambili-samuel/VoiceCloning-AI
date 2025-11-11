import os
import sys
sys.path.append('..')

from training.train_voice_clone import train_voice_clone
from src.voice_cloning import BarkVoiceCloner  # Updated import

def clone_voice_example():
    """Example of cloning a voice from audio files using Bark"""
    
    # Path to directory with your audio recordings
    audio_dir = "data/raw_audio/your_voice"
    speaker_name = "your_voice"
    
    # Train the voice clone
    print("Training voice clone with Bark...")
    success = train_voice_clone(audio_dir, speaker_name)
    
    if success:
        print("Voice cloning successful!")
        
        # Test with different texts
        voice_cloner = BarkVoiceCloner()  # Updated class name
        test_texts = [
            "Hello, this is my cloned voice speaking.",
            "I'm really excited about how this technology works.",
            "The weather is beautiful today, isn't it?",
            "This is a longer test to see how the voice handles extended speech."
        ]
        
        for i, text in enumerate(test_texts):
            output_path = f"data/processed_audio/test_cloned_voice_{i+1}.wav"
            print(f"Synthesizing: '{text}'")
            voice_cloner.synthesize_speech(
                text=text,
                speaker_name=speaker_name,
                output_path=output_path
            )
            print(f"Saved to: {output_path}")
        
        print("\nYou can now play the test files to check the voice quality.")
    else:
        print("Voice cloning failed")

if __name__ == "__main__":
    clone_voice_example()