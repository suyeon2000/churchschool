@echo off
chcp 65001 >nul
cd /d "C:\Users\suyeo\Documents\Claude\Projects\김준영의 홈페이지 만들기"

echo ========================================
echo GitHub에서 최신 파일 다운로드
echo ========================================
git pull origin main -v

echo.
echo ========================================
echo 완료!
echo ========================================
echo 로컬 파일이 최신으로 업데이트되었습니다.

pause