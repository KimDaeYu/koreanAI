import numpy as np
import json
import sys
import noisereduce as nr
import librosa
import math
from tqdm import tqdm
import re

def find_silence_intervals(pcm_file):
    with open(pcm_file, 'rb') as opened_pcm_file:
        buf = opened_pcm_file.read()
        pcm_data = np.frombuffer(buf, dtype = 'int16')
        y = librosa.util.buf_to_float(pcm_data)
        sr=16000

    # 노이즈 줄이기
    y = nr.reduce_noise(y=y, sr=sr)

    # 음성 데이터를 시간 단위로 나누기
    sample_rate = 16000  # 적절한 샘플레이트로 설정
    audio_duration = len(pcm_data) / sample_rate
    time_intervals = np.arange(0, audio_duration, 0.1)

    # 무음 구간 찾기
    silence_intervals = []
    speaking = False
    silence_start = 0
    
    # 신호의 변화량 구하기
    sig_pre = np.diff(y)
    sig_pre = (sig_pre-sig_pre.mean())/sig_pre.std()
    
    # 무음 구간 찾기
    for i in tqdm(range(0,len(sig_pre),100)):
        if np.abs(sig_pre)[i:i+1100].sum()>150:
            end = i/sr
            end = math.floor(round(float(f"{end:.4f}") * 1000,2))/1000
            
            if speaking==False and silence_start < end:
                silence_end = end
                if silence_end - silence_start >= 3.99:
                    silence_intervals.append({"beg": round(silence_start,2), "end": round(silence_end,2)})
                silence_start = None            
            speaking = True
        else:
            if speaking:
                speaking = False
                begin = i/sr
                begin = math.floor(round(float(f"{begin:.4f}") * 1000,2))/1000                
                if silence_start is None:
                    silence_start = begin
    return silence_intervals

def main(input_file, output_file):
    silence_data = {}
    with open(input_file, 'r') as f:
        pcm_files = f.read().splitlines()
        
    for pcm_file in pcm_files:
        silence_intervals = find_silence_intervals(pcm_file)
        pcm_file = pcm_file.split('/')[-1]
        silence_data[pcm_file] = silence_intervals
            
    with open(output_file, 'w') as f:
        s = json.dumps(silence_data,indent=4,ensure_ascii=False)
        s = re.sub('{\s*"(.*)": (\d+.\d+),\s*"(.*)": (\d+.\d+)\s*}(,?)', r'{"\1":\2, "\3":\4}\5', s)
        f.write(s)

        
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python3 Q3.py 입력파일명 출력파일명")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        main(input_file, output_file)