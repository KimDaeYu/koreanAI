'''
    한국어AI 경진대회 2023 제출 코드 입출력 예시
'''

import argparse

def arg_parse():
    parser = argparse.ArgumentParser(description='Korean SR Contest 2023')
    parser.add_argument('--audiolist', type=str)
    parser.add_argument('--outfile', type=str)

    args = parser.parse_args()

    return args


'''
    - file_list : audio file list (pcmlist.txt)
    - out_file : output file (Q3.json)
'''
def detect_wav_error(file_list, out_file):
    #
    # YOUR CODE HRER
    #


def detect_silence(file_list, out_file):
    #
    # YOUR CODE HRER
    #


def main():
    args = arg_parse()

    # Q2
    detect_silence(args.audiolist, args.outfile)

    # Q3
    detect_wav_error(args.audiolist, args.outfile)


if __name__ == "__main__":
    main()