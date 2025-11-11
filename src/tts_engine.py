import threading
from queue import Queue
import time
import numpy as np
from scipy.io.wavfile import write as write_wav
import sounddevice as sd
from bark import SAMPLE_RATE

class BarkTTSEngine:
    def __init__(self, voice_cloner):
        self.voice_cloner = voice_cloner
        self.sample_rate = SAMPLE_RATE
        self.speech_queue = Queue()
        self.is_speaking = False
        self.thread = None
        
    def speak(self, text: str, speaker_name: str = "user", blocking: bool = False):
        """Speak text using Bark TTS with cloned voice"""
        if blocking:
            self._synthesize_and_play(text, speaker_name)
        else:
            self.speech_queue.put((text, speaker_name))
            if not self.is_speaking:
                self._start_speaking_thread()
    
    def _start_speaking_thread(self):
        """Start background speaking thread"""
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._speaking_worker)
            self.thread.daemon = True
            self.thread.start()
    
    def _speaking_worker(self):
        """Background worker for non-blocking speech"""
        self.is_speaking = True
        while not self.speech_queue.empty():
            text, speaker_name = self.speech_queue.get()
            self._synthesize_and_play(text, speaker_name)
            self.speech_queue.task_done()
            time.sleep(0.1)
        self.is_speaking = False
    
    def _synthesize_and_play(self, text: str, speaker_name: str):
        """Synthesize and play audio"""
        try:
            # Split long text into smaller chunks for better synthesis
            chunks = self._split_text_for_synthesis(text)
            
            for chunk in chunks:
                if chunk.strip():
                    # Synthesize audio using Bark
                    audio = self.voice_cloner.synthesize_speech(
                        text=chunk,
                        speaker_name=speaker_name
                    )
                    
                    if audio is not None:
                        # Play audio
                        sd.play(audio, self.sample_rate)
                        sd.wait()  # Wait until playback is finished
                    
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
    
    def _split_text_for_synthesis(self, text: str, max_length: int = 100) -> list:
        """Split text into chunks suitable for synthesis"""
        # Simple splitting by sentences or length
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def stop(self):
        """Stop speaking"""
        sd.stop()
        while not self.speech_queue.empty():
            self.speech_queue.get()
            self.speech_queue.task_done()