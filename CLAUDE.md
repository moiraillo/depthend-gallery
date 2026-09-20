# 뎁센드 갤러리 웹사이트 (Depthend Gallery)

## 기본 정보
- **라이브 URL**: https://depthend-gallery.vercel.app
- **GitHub**: moiraillo/depthend-gallery
- **운영자**: 김민수 / moiraillo@gmail.com
- **위치**: 서울 성수동
- **1관**: 11평 / **2관**: 32평 (합계 43평)
- **전화**: 0507-1325-3176
- **오픈채팅**: https://open.kakao.com/o/sGlpZnBe
- **인스타그램**: @depthend_gallery

## 파일 구조
```
/
├── index.html       - 메인 페이지
├── hall1.html       - 뎁센드 1관 상세
├── hall2.html       - 뎁센드 2관 상세
├── location.html    - 오시는 길
├── archive.html     - 인스타그램 아카이브
├── sitemap.xml       - SEO 사이트맵
├── robots.txt        - 크롤러 설정 (Yeti 포함)
├── vercel.json        - Vercel 배포 설정 (rewrites만 사용)
└── images/            - 원본 소스 이미지 (HTML에서 직접 참조되지 않음, 백업/원본용)
```

**이미지 처리 방식**: 모든 페이지 이미지는 Base64로 인코딩되어 HTML에 직접 임베드되어 있음 (외부 이미지 호스팅 없음). `images/` 폴더는 원본 파일 백업용이며 HTML에서 직접 `src="images/..."`로 참조하지 않음.

## vercel.json 라우팅
```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "rewrites": [
    {"source": "/hall1", "destination": "/hall1.html"},
    {"source": "/hall2", "destination": "/hall2.html"},
    {"source": "/location", "destination": "/location.html"},
    {"source": "/archive", "destination": "/archive.html"}
  ]
}
```
⚠️ **routes와 cleanUrls를 함께 쓰면 충돌**한다. 반드시 `rewrites`만 사용할 것.

## 페이지별 상세

### index.html - 메인 페이지
- 히어로 슬라이더 (`sliderTrack`), 4초 자동 전환
- 1관/2관 카드 + 자세히 보기 버튼 (`href="/hall1"`, `/hall2"` — 절대 경로, 앵커(`#`) 아님)
- 인스타그램 섹션
- JS: main slider(`sliderTrack`) + reveal observer

### hall1.html - 뎁센드 1관
- 슬라이더 (`h1Track`)
- 요금표, 대관 절차, 편의시설
- JS: **h1 슬라이더만 포함** (`sliderTrack` 참조 없음 — index용 JS와 절대 공유 금지)
- `<style>`에 `.reveal { opacity: 1; transform: none; }` 오버라이드 포함 (스크롤 트리거 없이 즉시 표시)

### hall2.html - 뎁센드 2관
- 슬라이더 (`h2Track`)
- 요금표, 대관 절차
- JS: **h2 슬라이더만 포함** (`sliderTrack` 참조 없음)
- 동일하게 `.reveal` 오버라이드 포함

### location.html - 오시는 길
- 1관/2관 주소 + 네이버 지도 링크, 지하철 정보
- JS: common only

### archive.html - 아카이브
- 인스타그램 포스트 blockquote 임베드 (instagram embed.js 포함)

## 대관료 (최신: 2026-09-20 기준)

### 1관 (11평)
| 기간 | 요금 |
|---|---|
| 5일 이상 | 8만원 / 1일 |
| 4일 | 9만원 / 1일 |
| 3일 | 11만원 / 1일 |
| 1~2일 | 13만원 / 1일 |

주말 포함 대관 시 최소 4일부터 가능.

### 2관 (32평)
| 기간 | 요금 |
|---|---|
| 5일 이상 | 16만원 / 1일 |
| 4일 | 19만원 / 1일 |
| 3일 | 22만원 / 1일 |
| 2일 | 25만원 / 1일 |
| 1일 | 30만원 / 1일 |

⚠️ **가격은 다음 5개 파일에 흩어져 있으므로 변경 시 전부 함께 수정할 것**:
- `hall1.html` / `hall2.html`의 `.pricing-table` 본문
- `index.html`, `hall1.html`, `hall2.html`, `location.html`, `archive.html` 5개 파일 공통 FAQ JSON-LD (`"갤러리 대관료는 얼마인가요?"` 답변 문구)
- `hall2.html`의 `<meta name="description">` (2관 가격 언급)

## SEO 설정
- 타겟 키워드: 갤러리 대관, 갤러리 대여, 서울 갤러리 대관, 졸업전시 대관
- 각 페이지: 고유 title/description/canonical, Open Graph, JSON-LD(LocalBusiness, FAQPage, WebSite)
- Google Search Console / Naver Search Advisor 등록 완료, sitemap.xml 제출 완료

## 디자인 스펙
- 폰트: Noto Sans KR (300/400/500/700)
- 배경/헤더: 흰색
- 이미지 비율: 4:3 (PC/모바일 동일)
- 로고: 헤더에만 (푸터 로고 없음)
- 모바일: 로고 상단 + 메뉴 하단 배치, vertical divider 비표시
- 네비게이션: 뎁센드 1관 / 뎁센드 2관 / 오시는 길 / 아카이브

## 슬라이더 CSS 핵심 규칙
```css
/* 슬라이드 크기 고정 - 모바일 이미지 확대/오버플로우 방지 */
.slide, .h1-slide, .h2-slide {
  min-width: 0; width: 100%; height: 100%;
  flex: 0 0 100%; overflow: hidden;
}
/* 서브 페이지 콘텐츠 즉시 표시 (IntersectionObserver 없이) */
.reveal { opacity: 1; transform: none; }
```

## 작업 시 반드시 지킬 것
1. **슬라이더 JS 절대 공유 금지** — index의 main slider JS를 hall 페이지에 넣으면 `sliderTrack` 미존재로 전체 JS 크래시
2. **서브 페이지 `.reveal` 오버라이드 필수** — 없으면 흰 화면 버그 재발
3. **vercel.json은 `rewrites`만 사용** — `routes`와 `cleanUrls` 동시 사용 금지
4. **가격/연락처 등 반복 정보 수정 시 5개 파일 전부 확인** (위 "대관료" 섹션 참고)

## 알려진 이력 (요약)
- 서브 페이지 흰 화면 → `.reveal` opacity 오버라이드로 해결
- 1관/2관 슬라이더 버튼 미작동 → 페이지별 JS 완전 분리로 해결
- 모바일 이미지 확대/겹침 → `flex: 0 0 100%` + 컨테이너 `overflow: hidden`으로 해결
- robots.txt 네이버 미인식 → `User-agent: Yeti` 블록 추가로 해결
- "자세히 보기" 링크 미작동 → 앵커(`#hall1`) → 절대 경로(`/hall1`)로 수정
- 2026-09-20: 2관 대관료 인하 (18/22/26 → 16/19/22/25만원, 1일은 30만원 유지)

## TODO
- 도메인 구매 여부 미결정 (현재 vercel.app 서브도메인 사용, SEO엔 영향 없음)
- Google/Naver 색인 완료까지 2~4주 소요 예정
