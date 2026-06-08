@echo off
cd /d "C:\Users\suyeo\Documents\Claude\Projects\김준영의 홈페이지 만들기"
echo ========================================
echo Git Status 확인
echo ========================================
git status
echo.
echo ========================================
echo 최근 Commit 확인
echo ========================================
git log --oneline -5
pause