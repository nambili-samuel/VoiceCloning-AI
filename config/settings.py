import os
from dataclasses import dataclass
from typing import Dict, Any

# Try to import torch, but don't fail if it's not available
try:
    import torch
    CUDA_AVAILABLE = torch.cuda.is_available()
except ImportError:
    CUDA_AVAILABLE = False

@dataclass
class GrokConfig:
    model: str = "grok-beta"
    temperature: float = 0.8
    max_tokens: int = 200
    timeout: int = 30

@dataclass
class AudioConfig:
    sample_rate: int = 22050
    chunk_duration: int = 5  # seconds
    silence_threshold: float = 0.01
    min_audio_length: float = 3.0  # seconds for Bark
    max_audio_length: float = 300.0  # seconds

@dataclass
class ModelConfig:
    voice_clone_model: str = "bark"
    device: str = "cuda" if CUDA_AVAILABLE else "cpu"

@dataclass
class TrainingConfig:
    min_audio_samples: int = 3
    optimal_audio_duration: float = 10.0

@dataclass
class AgentConfig:
    wake_word: str = "assistant"
    response_timeout: int = 30
    max_response_length: int = 500

class Settings:
    def __init__(self):
        self.grok = GrokConfig()
        self.audio = AudioConfig()
        self.model = ModelConfig()
        self.training = TrainingConfig()
        self.agent = AgentConfig()
        self.data_dir = "data"
        self.models_dir = "data/models"
        
        # Create directories
        os.makedirs(f"{self.data_dir}/raw_audio", exist_ok=True)
        os.makedirs(f"{self.data_dir}/processed_audio", exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)

settings = Settings()