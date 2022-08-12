실행 명령어 
python problemP1.py --wave ./P1 --json ./answer.json

상위폴더 코딩공.json으로 결과를 덮어쓰고 싶을 경우 :
python problemP1.py --wave ./P1 --json ../코딩공.json

인자 설명
--wave : wav파일이 있는 폴더 경로 (주의: 해당 폴더에는 wav파일만 있어야함)
--json : json 출력 경로 (이미 있는 파일이라면 덮어 쓰여지도록 함 / 없으면 기본 구조로 정답을 작성)