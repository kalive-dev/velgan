from pydub import AudioSegment
import scipy.signal as signal
import numpy as np

# Load MP3 file
def load_audio(file_path):
    return AudioSegment.from_mp3(file_path)

# Apply bandpass filter to simulate phone speaker dynamics
def apply_phone_eq(audio_segment, lowcut=300.0, highcut=3400.0, sample_rate=44100):
    samples = np.array(audio_segment.get_array_of_samples())
    
    # Design bandpass filter
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(4, [low, high], btype='band')

    # Apply filter
    filtered_samples = signal.lfilter(b, a, samples)
    
    # Create a new AudioSegment from the filtered samples
    filtered_audio_segment = audio_segment._spawn(filtered_samples.astype(np.int16).tobytes())
    return filtered_audio_segment

# Save modified audio
def save_audio(audio_segment, output_path):
    audio_segment.export(output_path, format="mp3")

# Example usage
input_mp3 = "output.mp3"  # Path to your MP3 file
output_mp3 = "output_phone_effect.mp3"  # Path for saving the modified file

audio = load_audio(input_mp3)
filtered_audio = apply_phone_eq(audio)
save_audio(filtered_audio, output_mp3)
