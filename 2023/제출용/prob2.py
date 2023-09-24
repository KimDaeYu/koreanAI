import sys
import json
import wave

def detect_errors(wav_list_file, output_file):
    error_list = []

    with open(wav_list_file, 'r') as file:
        wav_files = file.read().splitlines()

    for wav_file in wav_files:
        try:
            with wave.open(wav_file, 'rb') as w:
                if w.getnframes() == 0 or w.getnchannels() == 0 or w.getsampwidth() == 0 or w.getframerate() == 0:
                    error_list.append(wav_file)
                else:
                    frames = w.readframes(w.getnframes())
                    if min(frames) <= -1 or max(frames) >= 1: # Assuming data is normalized between -1 and +1 for clipping error.
                        error_list.append(wav_file)
        except Exception as e:
            print(f"Error occurred while processing {wav_file}: {str(e)}")

    result = {"error_list": error_list}

    with open(output_file, 'w') as file:
        json.dump(result, file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 Q2.py <wav_list.txt> <output.json>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    detect_errors(input_filename, output_filename)
