import sounddevice as sd
import wavio


def record_audio(filename, duration, samplerate=44100):
    print("Recording...")
    recording = sd.rec(
        int(duration * samplerate), samplerate=samplerate, channels=2, dtype="int16"
    )
    sd.wait()
    print("Recording finished.")
    wavio.write(filename, recording, samplerate, sampwidth=2)
    print(f"Audio saved to {filename}")


def play_audio(filename):
    try:
        wav = wavio.read(filename)
        sd.play(wav.data, wav.rate)
        sd.wait()  # Wait until playback is finished
        print("Playback finished.")
    except FileNotFoundError:
        print(f"No file named {filename} found.")
