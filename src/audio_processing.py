import librosa
import soundfile as sf
import numpy as np
import os
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence
import speech_recognition as sr
from typing import List, Tuple
import noisereduce as nr

class AudioProcessor:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.recognizer = sr.Recognizer()
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file and convert to target sample rate"""
        try:
            audio, sr = librosa.load(file_path, sr=self.sample_rate)
            return audio, sr
        except Exception as e:
            raise Exception(f"Error loading audio: {str(e)}")
    
    def save_audio(self, audio: np.ndarray, file_path: str):
        """Save audio to file"""
        sf.write(file_path, audio, self.sample_rate)
    
    def preprocess_audio(self, audio: np.ndarray) -> np.ndarray:
        """Preprocess audio: noise reduction, normalization"""
        # Noise reduction
        audio_clean = nr.reduce_noise(y=audio, sr=self.sample_rate)
        
        # Normalize audio
        audio_normalized = effects.normalize(
            AudioSegment(
                audio_clean.tobytes(), 
                frame_rate=self.sample_rate,
                sample_width=4, 
                channels=1
            )
        )
        
        return np.array(audio_normalized.get_array_of_samples()) / 32768.0
    
    def split_audio(self, audio: np.ndarray, min_length: float = 2.0) -> List[np.ndarray]:
        """Split audio on silence"""
        audio_segment = AudioSegment(
            (audio * 32768).astype(np.int16).tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        chunks = split_on_silence(
            audio_segment,
            min_silence_len=500,
            silence_thresh=-40,
            keep_silence=200
        )
        
        # Filter chunks by minimum length
        min_samples = int(min_length * self.sample_rate)
        valid_chunks = []
        
        for chunk in chunks:
            chunk_audio = np.array(chunk.get_array_of_samples()) / 32768.0
            if len(chunk_audio) >= min_samples:
                valid_chunks.append(chunk_audio)
        
        return valid_chunks
    
    def record_audio(self, duration: int = 5, output_path: str = None) -> np.ndarray:
        """Record audio from microphone"""
        with sr.Microphone() as source:
            print("Recording...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio_data = self.recognizer.record(source, duration=duration)
            
            # Convert to numpy array
            audio = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            audio = audio.astype(np.float32) / 32768.0
            
            if output_path:
                self.save_audio(audio, output_path)
            
            return audio
    
    def extract_features(self, audio: np.ndarray) -> dict:
        """Extract audio features for voice analysis"""
        features = {}
        
        # MFCC features
        mfcc = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfcc, axis=1)
        features['mfcc_std'] = np.std(mfcc, axis=1)
        
        # Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)
        features['spectral_centroid'] = np.mean(spectral_centroid)
        
        # Pitch features
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio, 
            fmin=50, 
            fmax=500, 
            sr=self.sample_rate
        )
        features['pitch_mean'] = np.nanmean(f0) if np.any(voiced_flag) else 0
        
        return features