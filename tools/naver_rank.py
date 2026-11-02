#!/usr/bin/env python3
"""
네이버 통합검색 영역 순위 확인 툴

키워드별로 네이버 검색 결과에서 특정 영역(기본: urB_coR, 블로그 UGC 영역)이
위에서 몇 번째로 노출되는지 확인합니다. 추가 패키지 없이 Python 3만 있으면 됩니다.

사용법:
  python naver_rank.py                         # 키워드를 직접 입력 (대화형)
  python naver_rank.py "갤러리 대관" "성수 갤러리"  # 여러 키워드 한 번에
  python naver_rank.py -f keywords.txt         # 파일에서 키워드 읽기 (한 줄에 하나)

옵션:
  --area urB_coR      확인할 영역 코드 (기본 urB_coR)
  --mobile            모바일 검색 결과 기준으로 확인
  --blog depthend     해당 블로그 ID 글이 영역 안에 몇 번째로 있는지도 확인
  --all               페이지의 전체 영역 순서도 함께 출력
  --csv results.csv   결과를 CSV에 누적 저장 (기본: naver_rank_log.csv, 끄려면 --csv "")
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime

PC_URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="
MO_URL = "https://m.search.naver.com/search.naver?where=m&sm=mtp_hty&query="

PC_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
         "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
MO_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
         "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1")


def fetch(keyword, mobile=False):
    url = (MO_URL if mobile else PC_URL) + urllib.parse.quote(keyword)
    req = urllib.request.Request(url, headers={
        "User-Agent": MO_UA if mobile else PC_UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "ko-KR,ko;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=15) as res:
        return res.read().decode("utf-8", errors="replace")


def parse_areas(html):
    """페이지의 영역 순서 목록 [(코드, 순위), ...] 반환."""
    m = re.search(r"nx_cr_area_info\s*=\s*(\[.*?\])\s*;", html, re.S)
    if m:
        try:
            items = json.loads(m.group(1))
            return [(it["n"], int(it["r"])) for it in items]
        except (ValueError, KeyError):
            pass
    # 예비 방법: data-slog-container 등장 순서로 추정
    seen = []
    for code in re.findall(r'data-slog-container="([^"]+)"', html):
        if code not in seen:
            seen.append(code)
    return [(c, i + 1) for i, c in enumerate(seen)]


def parse_posts(html, area):
    """영역 안에 노출된 글 URL 목록(노출 순서)."""
    pat = (r'data-nlog-area="' + re.escape(area) +
           r'\.\w+\.link"[^>]*?data-nlog-target-url="([^"]+)"')
    posts = []
    for u in re.findall(pat, html):
        u = u.replace("&amp;", "&")
        if u not in posts:
            posts.append(u)
    return posts


def blog_position(posts, blog_id):
    if not blog_id:
        return None
    needle = blog_id.lower()
    for i, u in enumerate(posts, 1):
        low = u.lower()
        if f"blog.naver.com/{needle}/" in low or f"blogid={needle}" in low:
            return i
    return 0


def check(keyword, args):
    html = fetch(keyword, args.mobile)
    areas = parse_areas(html)
    rank = next((r for n, r in areas if n == args.area), None)
    posts = parse_posts(html, args.area) if rank else []
    return {
        "keyword": keyword,
        "areas": areas,
        "rank": rank,
        "total": len(areas),
        "posts": posts,
        "blog_pos": blog_position(posts, args.blog) if rank else (0 if args.blog else None),
    }


def print_result(res, args):
    kw = res["keyword"]
    print()
    print(f"■ {kw}")
    if not res["areas"]:
        print("  ⚠ 영역 정보를 찾지 못했어요. (네이버 차단 또는 페이지 구조 변경 가능성)")
        return
    if res["rank"]:
        print(f"  {args.area}: {res['rank']}번째 영역 (전체 {res['total']}개 중)")
    else:
        print(f"  {args.area}: 노출 안 됨 (전체 {res['total']}개 영역)")
    for i, u in enumerate(res["posts"], 1):
        print(f"    {i}. {u}")
    if args.blog:
        p = res["blog_pos"]
        print(f"  블로그 '{args.blog}': " + (f"{p}번째 글로 노출" if p else "영역 안에 없음"))
    if args.all:
        print("  전체 영역 순서: " + " > ".join(f"{r}.{n}" for n, r in res["areas"]))


def save_csv(path, res, args):
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["일시", "키워드", "기기", "영역", "순위", "전체영역수",
                        "블로그", "블로그순위", "전체영역순서"])
        w.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            res["keyword"],
            "모바일" if args.mobile else "PC",
            args.area,
            res["rank"] or "미노출",
            res["total"],
            args.blog or "",
            "" if res["blog_pos"] is None else (res["blog_pos"] or "없음"),
            " > ".join(n for n, _ in res["areas"]),
        ])


def run(keywords, args):
    for i, kw in enumerate(keywords):
        if i:
            time.sleep(args.delay)
        try:
            res = check(kw, args)
        except Exception as e:  # 네트워크 오류 등
            print(f"\n■ {kw}\n  ⚠ 조회 실패: {e}")
            continue
        print_result(res, args)
        if args.csv:
            save_csv(args.csv, res, args)


def main():
    ap = argparse.ArgumentParser(description="네이버 검색 영역 순위 확인")
    ap.add_argument("keywords", nargs="*", help="검색 키워드")
    ap.add_argument("-f", "--file", help="키워드 파일 (한 줄에 하나)")
    ap.add_argument("--area", default="urB_coR", help="확인할 영역 코드 (기본 urB_coR)")
    ap.add_argument("--mobile", action="store_true", help="모바일 검색 기준")
    ap.add_argument("--blog", default="", help="영역 안에서 찾을 네이버 블로그 ID")
    ap.add_argument("--all", action="store_true", help="전체 영역 순서 출력")
    ap.add_argument("--csv", default="naver_rank_log.csv", help="결과 누적 CSV 경로")
    ap.add_argument("--delay", type=float, default=2.0, help="키워드 사이 대기(초)")
    args = ap.parse_args()

    keywords = list(args.keywords)
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            keywords += [l.strip() for l in f if l.strip() and not l.startswith("#")]

    if keywords:
        run(keywords, args)
    else:
        print("키워드를 입력하세요. 여러 개는 쉼표(,)로 구분. 종료하려면 빈 줄 Enter.")
        while True:
            try:
                line = input("\n키워드> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not line:
                break
            run([k.strip() for k in line.split(",") if k.strip()], args)

    if args.csv:
        print(f"\n결과가 {os.path.abspath(args.csv)} 에 저장됐어요.")


if __name__ == "__main__":
    main()
