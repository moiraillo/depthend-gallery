# 네이버 영역 순위 확인 툴

키워드별로 네이버 통합검색에서 `urB_coR`(블로그 UGC 영역)이 몇 번째로 노출되는지 확인합니다.

> 사이트 배포와 무관한 로컬용 도구입니다. (`.vercelignore`로 배포 제외)
> 내 컴퓨터에서 실행해야 합니다. (클라우드 서버에서는 네이버 접속이 막힐 수 있음)

## 준비
Python 3 설치 (https://www.python.org/downloads/ — 설치 시 "Add Python to PATH" 체크)

## 실행
```bash
cd tools
python naver_rank.py
```
`키워드>` 가 나오면 입력. 여러 개는 쉼표로 구분 (`갤러리 대관, 성수 갤러리, 졸업전시 대관`). 빈 줄 Enter로 종료.

## 옵션 예시
```bash
python naver_rank.py "갤러리 대관" "성수 갤러리 대관"   # 키워드 바로 지정
python naver_rank.py -f keywords.txt                    # 파일(한 줄에 하나)
python naver_rank.py --mobile                           # 모바일 검색 기준
python naver_rank.py --blog 블로그아이디                # 내 블로그 글이 영역 안 몇 번째인지
python naver_rank.py --area urB_boR                     # 다른 영역 코드 확인
python naver_rank.py --all                              # 전체 영역 순서 출력
```
결과는 매번 `naver_rank_log.csv`에 누적 저장됩니다 (엑셀로 열기 가능).

## 참고
- 순위는 페이지 안의 `nx_cr_area_info` 값 기준입니다 (개발자 도구에서 보던 것과 동일).
- 로그인 여부·지역·시간에 따라 브라우저 화면과 다를 수 있습니다.
- 너무 자주/많이 조회하면 네이버가 일시 차단할 수 있어 키워드 사이 2초 대기합니다 (`--delay`로 조절).
