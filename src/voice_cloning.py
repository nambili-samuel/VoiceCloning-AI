import torch
import torchaudio
import numpy as np
import os
from typing import List, Optional, Dict, Tuple
import json
import librosa
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import soundfile as sf

try:
    from bark import SAMPLE_RATE, generate_audio, preload_models
    from scipy.io.wavfile import write as write_wav
    BARK_AVAILABLE = True
except ImportError:
    print("Bark not available. Please install it with: pip install suno-bark")
    BARK_AVAILABLE = False
    # Define fallback constants
    SAMPLE_RATE = 24000

class BarkVoiceCloner:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.sample_rate = SAMPLE_RATE
        self.voice_embeddings = {}
        self.voice_prompts = {}
        
        if BARK_AVAILABLE:
            # Preload Bark models
            print("Loading Bark models...")
            preload_models()
            print("Bark models loaded successfully!")
        else:
            print("Bark is not available. Using fallback mode.")
    
    def extract_voice_characteristics(self, audio_path: str) -> Dict:
        """Extract voice characteristics from audio for better cloning"""
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Extract features
            features = {}
            
            # MFCC features
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
            features['mfcc_mean'] = np.mean(mfcc, axis=1)
            features['mfcc_std'] = np.std(mfcc, axis=1)
            
            # Spectral features
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
            features['spectral_centroid_mean'] = np.mean(spectral_centroid)
            
            # Pitch features
            f0, voiced_flag, voiced_probs = librosa.pyin(audio, fmin=50, fmax=500, sr=sr)
            features['pitch_mean'] = np.nanmean(f0) if np.any(voiced_flag) else 0
            features['pitch_std'] = np.nanstd(f0) if np.any(voiced_flag) else 0
            
            # Energy features
            rms = librosa.feature.rms(y=audio)
            features['energy_mean'] = np.mean(rms)
            
            # Duration and timing features
            features['duration'] = len(audio) / sr
            
            return features
            
        except Exception as e:
            print(f"Error extracting voice characteristics: {str(e)}")
            return {}
    
    def create_voice_prompt(self, audio_path: str, speaker_name: str) -> bool:
        """Create a voice prompt for Bark voice cloning"""
        try:
            # For Bark, we use the audio directly as a prompt
            # We'll create a cleaned version optimized for Bark
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Save the processed audio as voice prompt
            prompt_path = f"data/models/{speaker_name}_prompt.wav"
            sf.write(prompt_path, audio, sr)
            
            # Store voice characteristics for reference
            characteristics = self.extract_voice_characteristics(audio_path)
            self.voice_embeddings[speaker_name] = characteristics
            
            # Save characteristics to file
            char_path = f"data/models/{speaker_name}_characteristics.json"
            with open(char_path, 'w') as f:
                # Convert numpy arrays to lists for JSON serialization
                serializable_chars = {}
                for key, value in characteristics.items():
                    if isinstance(value, np.ndarray):
                        serializable_chars[key] = value.tolist()
                    else:
                        serializable_chars[key] = value
                json.dump(serializable_chars, f)
            
            print(f"Voice prompt created for {speaker_name}")
            return True
            
        except Exception as e:
            print(f"Error creating voice prompt: {str(e)}")
            return False
    
    def load_voice_prompt(self, speaker_name: str) -> Optional[str]:
        """Load voice prompt for a speaker"""
        try:
            prompt_path = f"data/models/{speaker_name}_prompt.wav"
            if os.path.exists(prompt_path):
                return prompt_path
            
            # Also try to load characteristics
            char_path = f"data/models/{speaker_name}_characteristics.json"
            if os.path.exists(char_path):
                with open(char_path, 'r') as f:
                    characteristics = json.load(f)
                    self.voice_embeddings[speaker_name] = characteristics
            
            return None
        except Exception as e:
            print(f"Error loading voice prompt: {str(e)}")
            return None
    
    def synthesize_speech(self, text: str, speaker_name: str, 
                         output_path: str = None,
                         temperature: float = 0.7,
                         silence_padding: float = 0.5) -> Optional[np.ndarray]:
        """Synthesize speech using Bark with voice cloning"""
        try:
            if not BARK_AVAILABLE:
                print("Bark is not available. Cannot synthesize speech.")
                return None
            
            # Load voice prompt
            prompt_path = self.load_voice_prompt(speaker_name)
            
            if not prompt_path:
                raise ValueError(f"No voice prompt found for {speaker_name}")
            
            # Generate audio using Bark with voice prompt
            audio_array = generate_audio(
                text,
                history_prompt=prompt_path,  # This enables voice cloning
                text_temp=temperature,
                waveform_temp=temperature,
                silent_duration=silence_padding
            )
            
            if output_path:
                write_wav(output_path, self.sample_rate, audio_array)
                return None
            else:
                return audio_array
                
        except Exception as e:
            print(f"Error synthesizing speech with Bark: {str(e)}")
            return None
    
    def fine_tune_voice_similarity(self, reference_audio: np.ndarray, 
                                  generated_audio: np.ndarray) -> float:
        """Calculate similarity between reference and generated audio"""
        try:
            # Extract features from both audios
            ref_features = self.extract_features_from_audio(reference_audio)
            gen_features = self.extract_features_from_audio(generated_audio)
            
            # Calculate similarity (simple cosine similarity on MFCCs)
            similarity = self.cosine_similarity(
                ref_features['mfcc_mean'], 
                gen_features['mfcc_mean']
            )
            
            return similarity
        except Exception as e:
            print(f"Error calculating voice similarity: {str(e)}")
            return 0.0
    
    def extract_features_from_audio(self, audio: np.ndarray) -> Dict:
        """Extract features from audio array"""
        features = {}
        
        # MFCC features
        mfcc = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=20)
        features['mfcc_mean'] = np.mean(mfcc, axis=1)
        features['mfcc_std'] = np.std(mfcc, axis=1)
        
        return features
    
    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def list_available_voices(self) -> List[str]:
        """List available cloned voices"""
        return list(self.voice_embeddings.keys())
    
    def optimize_prompt_for_bark(self, audio_path: str, output_path: str) -> bool:
        """Optimize audio prompt for better Bark performance"""
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Remove silence using simple energy-based method
            from pydub import AudioSegment, effects
            
            # Convert to AudioSegment for processing
            audio_segment = AudioSegment(
                (audio * 32768).astype(np.int16).tobytes(),
                frame_rate=sr,
                sample_width=2,
                channels=1
            )
            
            # Normalize
            optimized_audio = effects.normalize(audio_segment)
            
            # Export
            optimized_audio.export(output_path, format="wav")
            return True
            
        except Exception as e:
            print(f"Error optimizing prompt: {str(e)}")
            return False
    
    def create_voice_from_multiple_samples(self, audio_directory: str, 
                                         speaker_name: str) -> bool:
        """Create voice prompt from multiple audio samples"""
        try:
            audio_files = [f for f in os.listdir(audio_directory) 
                          if f.endswith(('.wav', '.mp3', '.m4a'))]
            
            if not audio_files:
                print("No audio files found")
                return False
            
            # Find the best sample (longest duration with good quality)
            best_file = None
            max_duration = 0
            
            for audio_file in audio_files:
                file_path = os.path.join(audio_directory, audio_file)
                try:
                    audio, sr = librosa.load(file_path, sr=self.sample_rate)
                    duration = len(audio) / sr
                    
                    # Check if this is a better sample
                    if duration > max_duration and duration > 3.0:  # At least 3 seconds
                        max_duration = duration
                        best_file = file_path
                except Exception as e:
                    print(f"Error processing {audio_file}: {e}")
                    continue
            
            if best_file:
                print(f"Using {best_file} for voice cloning (duration: {max_duration:.2f}s)")
                # Optimize the best sample for Bark
                optimized_path = f"data/models/{speaker_name}_optimized.wav"
                if self.optimize_prompt_for_bark(best_file, optimized_path):
                    return self.create_voice_prompt(optimized_path, speaker_name)
                else:
                    # Fallback: use original file
                    return self.create_voice_prompt(best_file, speaker_name)
            
            return False
            
        except Exception as e:
            print(f"Error creating voice from multiple samples: {str(e)}")
            return False