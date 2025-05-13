# SIGMA 프로젝트 구조 및 관리 규칙

## 폴더 구조 원칙

- **실제 개발/빌드/배포/자동화는 반드시 `sigma-monitor/` 폴더에서만 진행합니다.**
- 루트(src/ 등) 폴더는 더 이상 사용하지 않으며, 혼란 방지를 위해 삭제/백업 처리되었습니다.
- 앞으로는 `sigma-monitor/` 내부의 src, public, android, package.json 등만 관리/수정/배포하세요.

## 예시

- 프론트엔드 코드: `sigma-monitor/src/`
- 네이티브/안드로이드: `sigma-monitor/android/`
- 빌드/배포/자동화: `sigma-monitor/package.json`의 scripts 사용

---

이 규칙을 반드시 지켜주세요. (중복/혼란 방지)
