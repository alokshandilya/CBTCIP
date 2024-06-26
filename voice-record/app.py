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


def main():
    while True:
        print("\nVoice Recorder")
        print("1. Record Audio")
        print("2. Play Audio")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            filename = input(
                "Enter the file name to save the recording (e.g., recording.wav): "
            )
            duration = int(input("Enter the duration of the recording in seconds: "))
            record_audio(filename, duration)
        elif choice == "2":
            filename = input("Enter the file name to play (e.g., recording.wav): ")
            play_audio(filename)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
