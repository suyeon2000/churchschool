@echo off
chcp 65001 >nul
cd /d "C:\Users\suyeo\Documents\Claude\Projects\김준영의 홈페이지 만들기"

echo ========================================
echo 강제 PUSH 실행 (GitHub 덮어쓰기)
echo ========================================
git push -f origin main -v

echo.
echo ========================================
echo 완료!
echo ========================================

pause