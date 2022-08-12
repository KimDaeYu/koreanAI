import re
import json
import argparse

def bracket_filter(sentence):
    new_sentence = str()
    flag = False

    for ch in sentence:
        if ch == '(' and flag is False:
            flag = True
            continue
        if ch == '(' and flag is True:
            flag = False
            continue
        if ch != ')' and flag is False:
            new_sentence += ch
    return new_sentence

def special_filter(sentence):
    SENTENCE_MARK = ['?', '!', '.']
    NOISE = ['o', 'n', 'u', 'b', 'l']
    EXCEPT = ['/', '+', '*', '-', '@', '$', '^', '&', '[', ']', '=', ':', ';', ',']

    new_sentence = str()
    for idx, ch in enumerate(sentence):
        if ch not in SENTENCE_MARK:
            if idx + 1 < len(sentence) and ch in NOISE and sentence[idx + 1] == '/':
                continue

        if ch not in EXCEPT:
            new_sentence += ch

    pattern = re.compile(r'\s\s+')
    new_sentence = re.sub(pattern, ' ', new_sentence.strip())
    return new_sentence



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Q2 Sovled code')

    # basic config
    parser.add_argument('--json', type=str, required=True, default='./코딩공.json', help='set json path')
    args = parser.parse_args()

    json_path = args.json

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


    for dic in json_data['Q2']:
        sent2 = dic['original']
        sent2 = special_filter(bracket_filter(sent2))
        dic['new'] = sent2
                
    with open(json_path, 'w', encoding='UTF-8') as make_file:
        json.dump(json_data, make_file, indent="\t", ensure_ascii=False)