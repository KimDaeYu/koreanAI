from ctypes import *
import json
import os
import math
import argparse

def readFourcc(f):
    return f.read(4).decode()
    
def readBytesAsInt(f,size):
    if size == 0 or size > 4:
        return 0
    
    data = bytes(f.read(size))
    if size == 1:
        return data[0]
    elif size == 2:
        return data[0] | data[1] <<8
    elif size == 3:
        return data[0] | data[1] <<8 | data[2] << 16
    else:
        return data[0] | data[1] <<8 | data[2] << 16 | data[3] << 24
    return 0


class fmt_chunk():
    wFormatTag = 0
    wChannels = 0
    dwSamplePerSec = 0
    dwAvgBytesPerSec = 0
    wBlockAlign = 0
    wBitsPerSample = 0
    cbsize = 0
    format_specific_data = []
    
    def parse(self, f, cksize):
        
        self.wFormatTag = readBytesAsInt(f,2)
        self.wChannels = readBytesAsInt(f,2)
        self.dwSamplePerSec = readBytesAsInt(f,4)
        self.dwAvgBytesPerSec = readBytesAsInt(f,4)
        self.wBlockAlign = readBytesAsInt(f,2)
        self.wBitsPerSample = readBytesAsInt(f,2)
        
        cksize -= 16
        
        # print('  wFormatTag :',self.wFormatTag)
        # print('  wChannels :',self.wChannels)
        # print('  dwSamplePerSec :',self.dwSamplePerSec)
        # print('  dwAvgBytesPerSec :',self.dwAvgBytesPerSec)
        # print('  wBlockAlign :',self.wBlockAlign)
        # print('  wBitsPerSample :',self.wBitsPerSample)
        
        if cksize > 0:
            self.cbsize = readBytesAsInt(f,2)
            cksize -= 2
            # print('  cbsize :',self.cbsize)
            
            if self.cbsize > 0 and cksize >= self.cbsize:
                self.format_specific_data = bytes(f.read(self.cbsize))
                # print('  format specific data : 0x',self.format_specific_data.hex())
                cksize -= self.cbsize
        
        if cksize > 0:
            f.read(cksize)
        
        return 0


        
class waveparser(object):
    def __init__(self, wave):
                
        self.fmt = fmt_chunk()
        
        self.data = []
        self.this = []
        self.IsThis = False
        
        if wave is not None:
            # print('wave file path :',wave)
            self.parse(open(wave,'rb'))

        self.WAVNumSamples = len(self.data) / (self.fmt.wChannels * self.fmt.wBitsPerSample/8) 
        self.WAVDuration = math.floor(round(float(f"{self.WAVNumSamples / self.fmt.dwSamplePerSec:.4f}") * 1000,2))/1000

        # check this
        if(len(self.this) != 0):
            self.IsThis = True
            
            try:
                self.this = self.this.decode('utf-8')
                self.IsText = True
            except Exception as e:
                self.IsText = False
                self.THISNumSamples = len(self.this) / (self.fmt.wChannels * self.fmt.wBitsPerSample/8) 
                self.THISWAVDuration = math.floor(round(float(f"{self.THISNumSamples / self.fmt.dwSamplePerSec:.4f}") * 1000,2))/1000
                self.this = self.THISWAVDuration 

    def parse_subchunk(self,f):
        chunkID = readFourcc(f)
        try:
            cksize = readBytesAsInt(f,4)
        except Exception as e:
            return -1

        # print('chunkID:',chunkID, ' cksize:',cksize)
        if chunkID == 'fmt ':
            return self.fmt.parse(f,cksize)
        elif chunkID == 'data':
            self.data = f.read(cksize)
            return 0
        elif chunkID == 'THIS':
            self.this = f.read(cksize)
            return 0
        else:
            _ = bytes(f.read(cksize))
            
        return 0
    
    def parse(self, f):
        if f is None:
            return
        
        chunkID = readFourcc(f)
        cksize = readBytesAsInt(f,4)
        mediaformat = readFourcc(f)
        # print('chunkID:',chunkID, ' cksize:',cksize, '  format:', mediaformat)    
        
        if chunkID != 'RIFF':
            return
        
        while(1):
            ret = self.parse_subchunk(f)
            if ret < 0:
                break    
            
        f.close()
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Q1 Sovled code')

    # basic config
    parser.add_argument('--wave', type=str, required=True, default='./P1', help='set wave files folder path')
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

    json_data['Q1'] = []
    for i, f in enumerate(file_list):
        wave = waveparser(wave_folder_path + '/' + f)

        tmp = {}
        tmp['filename'] = f
        tmp['duration'] = wave.WAVDuration
        json_data['Q1'].append(tmp)

        if(wave.IsThis):
            json_data['Q1'][i]['THIS'] = wave.this
                
    with open(json_path, 'w', encoding='UTF-8') as make_file:
        json.dump(json_data, make_file, indent="\t", ensure_ascii=False)