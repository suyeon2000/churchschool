@echo off
chcp 65001 >nul
cd /d "C:\Users\suyeo\Documents\Claude\Projects\김준영의 홈페이지 만들기"

echo ========================================
echo Git 상태 확인
echo ========================================
git status

echo.
echo ========================================
echo 변경사항이 있으면 커밋
echo ========================================
git add -A
git commit -m "모든 학생 페이지 표준화 및 학습자료 데이터 업데이트" --allow-empty

echo.
echo ========================================
echo GitHub에 강제 푸시 (자세한 정보 포함)
echo ========================================
git push -u origin main -v

echo.
echo ========================================
echo 최종 확인
echo ========================================
git log --oneline -3
git remote -v

pause