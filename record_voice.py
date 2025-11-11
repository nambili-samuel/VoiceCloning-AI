import pyaudio
import wave
import os

def record_audio(filename, duration=10, sample_rate=22050, channels=1, chunk=1024):
    """Record audio from microphone"""
    audio = pyaudio.PyAudio()
    
    print(f"Recording {duration} seconds of audio...")
    print("Speak now!")
    
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk
    )
    
    frames = []
    
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Recording finished!")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the recorded data
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(f"Audio saved to {filename}")

if __name__ == "__main__":
    os.makedirs("data/raw_audio/your_voice", exist_ok=True)
    
    print("Voice Recording for AI Training")
    print("Record several clips of your voice (10 seconds each)")
    print("Speak clearly and naturally\n")
    
    num_recordings = int(input("How many recordings? (3-5 recommended): "))
    
    for i in range(num_recordings):
        filename = f"data/raw_audio/your_voice/recording_{i+1}.wav"
        input(f"Press Enter to start recording {i+1}...")
        record_audio(filename, duration=10)
        print()
    
    print("All recordings completed!")
    print("You can now train your voice clone when Bark finishes downloading.")