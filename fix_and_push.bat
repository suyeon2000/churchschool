@echo off
chcp 65001 >nul
cd /d "C:\Users\suyeo\Documents\Claude\Projects\김준영의 홈페이지 만들기"

echo ========================================
echo Git 파일 추적 복구 및 강제 푸시
echo ========================================

echo.
echo 1. 모든 HTML 파일 Git 추적 제거
git rm --cached *.html

echo.
echo 2. 모든 파일 다시 add
git add -A

echo.
echo 3. 상태 확인
git status

echo.
echo 4. 커밋
git commit -m "모든 학생 페이지 최신 버전 - 달란트 섹션 포함" --allow-empty

echo.
echo 5. GitHub에 강제 푸시
git push -f origin main -v

echo.
echo ========================================
echo 완료! GitHub에 최신 파일이 업로드되었습니다.
echo ========================================

pause