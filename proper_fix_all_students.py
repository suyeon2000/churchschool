#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

# Junyoung 파일을 템플릿으로 사용
with open('student_junyoung.html', 'r', encoding='utf-8') as f:
    junyoung_content = f.read()

# JavaScript 부분 추출 (Junyoung에서)
import re
script_match = re.search(r'<script>.*?</script>', junyoung_content, re.DOTALL)
if not script_match:
    print("❌ Junyoung의 JavaScript를 찾을 수 없습니다")
    exit()

junyoung_script = script_match.group(0)

# 각 학생별 수정
students = {
    'yerim': {'password': '9393', 'prev': 'junyoung', 'next': 'joshua'},
    'joshua': {'password': '4780', 'prev': 'yerim', 'next': 'elliot'},
    'elliot': {'password': 'winter', 'prev': 'joshua', 'next': 'anna'},
    'anna': {'password': '921', 'prev': 'elliot', 'next': 'moses'},
    'moses': {'password': '1251', 'prev': 'anna', 'next': None},
}

for student_id, info in students.items():
    filename = f'student_{student_id}.html'
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"⚠️  {filename} 읽기 실패")
        continue
    
    # 기존 script 제거
    content = re.sub(r'\s*<script>.*?</script>\s*', '', content, flags=re.DOTALL)
    
    # Junyoung의 script를 복사하고 학생 정보로 교체
    new_script = junyoung_script
    new_script = new_script.replace('const CORRECT_PASSWORD = "BALD";', f'const CORRECT_PASSWORD = "{info["password"]}";\n        const STUDENT_ID = "{student_id}";')
    new_script = new_script.replace('const STUDENT_ID = "junyoung";', '')
    new_script = re.sub(
        r'talents\.junyoung',
        f'talents.{student_id}',
        new_script
    )
    new_script = re.sub(
        r'studentData\.junyoung',
        f'studentData.{student_id}',
        new_script
    )
    
    # script 추가
    content = content.replace('</body>', f'\n    {new_script}\n</body>')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} 수정 완료")

print("\n✨ 모든 학생 파일 수정 완료!")
