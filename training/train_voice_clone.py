import os
import sys
sys.path.append('..')

from src.audio_processing import AudioProcessor
from src.voice_cloning import BarkVoiceCloner  # Updated import
from config.settings import settings

def train_voice_clone(audio_directory: str, speaker_name: str):
    """Train voice clone from audio samples using Bark"""
    
    audio_processor = AudioProcessor()
    voice_cloner = BarkVoiceCloner()  # Updated class name
    
    # Process audio files and create voice prompt
    print("Creating voice clone with Bark...")
    success = voice_cloner.create_voice_from_multiple_samples(audio_directory, speaker_name)
    
    if success:
        print("Voice cloning successful!")
        
        # Test the cloned voice
        test_text = "Hello, this is my cloned voice speaking through Bark. How do I sound?"
        
        print("Synthesizing test speech...")
        test_audio = voice_cloner.synthesize_speech(
            text=test_text,
            speaker_name=speaker_name,
            output_path="data/processed_audio/test_bark_voice.wav"
        )
        
        if test_audio is not None:
            print("Test audio saved to data/processed_audio/test_bark_voice.wav")
            
            # Calculate voice similarity if we have reference audio
            audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.wav')]
            if audio_files:
                reference_path = os.path.join(audio_directory, audio_files[0])
                reference_audio, _ = audio_processor.load_audio(reference_path)
                
                similarity = voice_cloner.fine_tune_voice_similarity(
                    reference_audio, test_audio
                )
                print(f"Voice similarity score: {similarity:.3f}")
        else:
            print("Test synthesis failed")
        
        return True
    else:
        print("Voice cloning failed")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train voice clone with Bark')
    parser.add_argument('--audio_dir', type=str, required=True, 
                       help='Directory containing audio files')
    parser.add_argument('--speaker_name', type=str, required=True,
                       help='Name for the cloned voice')
    
    args = parser.parse_args()
    
    train_voice_clone(args.audio_dir, args.speaker_name)