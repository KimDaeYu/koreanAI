import json
import os
import argparse
import librosa
import numpy as np
import noisereduce as nr
import math

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Q3 Sovled code')

    # basic config
    parser.add_argument('--wave', type=str, required=True, default='./P3', help='set wave files folder path')
    parser.add_argument('--json', type=str, required=True, default='./코딩공.json', help='set json path')
    args = parser.parse_args()

    
    wave_folder_path = args.wave 
    json_path = args.json

    try:
        file_list = os.listdir(wave_folder_path)
    except Exception as e:
        print('Not Exist Path!')
        exit(0)

    basic_json = {
            "Q1": [],
            "Q2": [],
            "Q3": []
        }

    try:
        with open(json_path, encoding="UTF-8") as f:
            json_data = json.load(f)
    except Exception as e:
        with open(json_path, 'w', encoding="UTF-8") as n:
            json.dump(basic_json, n, indent="\t", ensure_ascii=False)
        with open(json_path, encoding="UTF-8") as f:
            json_data = json.load(f)

    json_data['Q3'] = []
    for idx, f in enumerate(file_list):
        ### process
        sig, sr = librosa.load(wave_folder_path + '/' + f,sr=32000)
        sig = nr.reduce_noise(y=sig, sr=sr)

        sig_pre = np.diff(sig)
        sig_pre = (sig_pre-sig_pre.mean())/sig_pre.std()
        for i in range(len(sig_pre)):
            if np.abs(sig_pre)[i:i+1100].sum()>150:
                #print("음성1 시작 시간 : {}".format(i/sr) )
                begin = i/sr
                begin = math.floor(round(float(f"{begin:.4f}") * 1000,2))/1000
                break
        sig_pre_reverse=sig_pre[::-1]
        for i in range(len(sig_pre_reverse)):
            if np.abs(sig_pre_reverse)[i:i+720].sum()>38:
                #print("음성1 끝 시간 : {}".format( (len(sig_pre_reverse)-i)/sr  ) )
                end = (len(sig_pre_reverse)-i)/sr
                end = math.floor(round(float(f"{end:.4f}") * 1000,2))/1000
                break

        tmp = {}
        tmp['filename'] = f
        tmp['begin'] = begin
        tmp['end'] = end
        json_data['Q3'].append(tmp)
                
    with open(json_path, 'w', encoding='UTF-8') as make_file:
        json.dump(json_data, make_file, indent="\t", ensure_ascii=False)