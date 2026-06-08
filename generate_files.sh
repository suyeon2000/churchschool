#!/bin/bash

# 학생별 설정
declare -A colors=(
    ["joshua"]="#2E7D32"
    ["elliot"]="#F57C00"
    ["anna"]="#C2185B"
    ["moses"]="#E53935"
    ["yerim"]="#8B6BB8"
)

declare -A dark_colors=(
    ["joshua"]="#1b5e20"
    ["elliot"]="#E65100"
    ["anna"]="#880E4F"
    ["moses"]="#B71C1C"
    ["yerim"]="#6A4C93"
)

declare -A initials=(
    ["joshua"]="Jo"
    ["elliot"]="E"
    ["anna"]="A"
    ["moses"]="M"
    ["yerim"]="Y"
)

declare -A passwords=(
    ["joshua"]="4780"
    ["elliot"]="winter"
    ["anna"]="921"
    ["moses"]="1251"
    ["yerim"]="9393"
)

declare -A names=(
    ["joshua"]="Joshua"
    ["elliot"]="Elliot"
    ["anna"]="Anna"
    ["moses"]="Moses"
    ["yerim"]="Yerim"
)

for student in joshua elliot anna moses yerim; do
    # Junyoung 파일 읽기
    content=$(cat student_junyoung.html)
    
    # 학생 정보로 교체
    content="${content//Junyoung/${names[$student]}}"
    content="${content//junyoung/$student}"
    content="${content//BALD/${passwords[$student]}}"
    content="${content//>J</>${initials[$student]}<}"
    content="${content//#3B5998/${colors[$student]}}"
    content="${content//#2E4A7A/${dark_colors[$student]}}"
    
    # 파일 저장
    echo "$content" > "student_$student.html"
    echo "✅ student_$student.html 생성 완료"
done

echo "🎉 모든 파일 생성 완료!"
