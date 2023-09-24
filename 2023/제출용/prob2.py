import wave
import json
import sys

def detect_errors(wav_file):
    errors = []
    try:
        with wave.open(wav_file, 'rb') as wf:
            # 헤더 정보를 읽어오기
            num_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            frame_rate = wf.getframerate()
            num_frames = wf.getnframes()

            # 데이터 값이 없는 경우 검출
            if num_frames == 0:
                errors.append("데이터 값이 없는 경우: " + wav_file)

            # 데이터만 있는 경우 검출
            if num_frames > 0 and (num_channels * sample_width * num_frames) == 0:
                errors.append("데이터만 있는 경우: " + wav_file)
    except wave.Error:
        # 헤더만 있는 경우 검출
        errors.append("헤더만 있는 경우: " + wav_file)
    except Exception as e:
        print("오류 발생:", str(e))

    # 클리핑 에러 검출 (클리핑을 검출하는 추가적인 코드가 필요할 수 있음)

    return errors

def main(input_file, output_file):
    error_list = []
    with open(input_file, 'r') as f:
        wav_files = f.read().splitlines()

    for wav_file in wav_files:
        errors = detect_errors(wav_file)
        error_list.extend(errors)

    result = {"error_list": error_list}

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python3 Q2.py 입력파일명 출력파일명")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        main(input_file, output_file)
