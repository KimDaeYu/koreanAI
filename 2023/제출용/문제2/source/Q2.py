import wave
import os
import json
import sys
import struct

def check_errors(file_path):
    try:
        with wave.open(file_path, 'rb') as wf:
            nframes = wf.getnframes()
            
            frames = wf.readframes(nframes)
            if len(frames)==0:
                # data 없을때
                print(f"No data in file {file_path}")
                return True            
            max_possible_amplitude = 2 ** (wf.getsampwidth() * 8 - 1)
            
            frames = struct.unpack('{}h'.format(wf.getnframes()), frames)
            frames = list(frames)
            
            # 지워도 되는지 체크 23 ~ 25
            if max(frames) == 0 and min(frames) == 0: # All data values are zero.
                print(f"Zero data values for file {file_path}")
                return True
            
            threshold = 0.98
            max_amplitude = max(frames)
            min_amplitude = abs(min(frames))
            if  max_amplitude/max_possible_amplitude > threshold   or min_amplitude/max_possible_amplitude > threshold : # Clipping 에러

                print(f"Clipping error for file {file_path}")
                return True
            
    except Exception as e:
        # header 없을때
        print(f"No header {file_path}: {e}")
        return True
        
    return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 Q2.py <wav_list.txt> <output.json>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    with open(input_filename, 'r') as f:
        file_paths = [line.strip() for line in f]
    
    error_list = [fp for fp in file_paths if check_errors(fp)]
    
    with open(output_filename, 'w') as f:
        json.dump({"error_list": error_list}, f,indent=2)
        

if __name__ == "__main__":
    main()
