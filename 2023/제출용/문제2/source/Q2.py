import wave
import json
import sys
import struct
import numpy as np

def check_errors(file_path):
    try:
        with wave.open(file_path, 'rb') as wf:
            # case 2. 데이터만 있는 경우 -> Exception
            nframes = wf.getnframes()
            
            frames = wf.readframes(nframes)
            # case 1. 헤더만 있는 경우
            if len(frames)==0:
                # case 
                print(f"No data in file {file_path}")
                return True            
            max_possible_amplitude = 2 ** (wf.getsampwidth() * 8 - 1)
            
            frames = struct.unpack('{}h'.format(wf.getnframes()), frames)
            frames = list(frames)
                        
            threshold = 0.99
            max_amplitude = max(frames)
            min_amplitude = abs(min(frames))
            
            # case 4. 클리핑 에러
            if  max_amplitude/max_possible_amplitude > threshold   or min_amplitude/max_possible_amplitude > threshold :
                print(f"Clipping error for file {file_path}")
                return True
            
            #case 3. 데이터 값이 없는 경우
            frames = np.diff(frames)
            frames = frames/max_possible_amplitude*100

            if max(abs(frames)) < 5:
                print(f"No voice data : {file_path}")
                return True
            
    except Exception as e:
        # case 2. 데이터만 있는 경우
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
        json.dump({"error_list": error_list}, f,indent=2,ensure_ascii=False)
        

if __name__ == "__main__":
    main()
