@echo off
cd /d "C:\Users\suyeo\Documents\Claude\Projects\김준영의 홈페이지 만들기"
del .git\HEAD.lock 2>nul
git add -A
git commit -m "모든 학생 페이지 표준화 및 학습자료 데이터 업데이트"
git push origin main -v
pause