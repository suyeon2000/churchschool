#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

students = ['junyoung', 'yerim', 'joshua', 'elliot', 'anna', 'moses']

print("📋 학생 페이지 패스워드 기능 검사\n")
print("=" * 60)

for student in students:
    filename = f'student_{student}.html'
    filepath = os.path.join(os.getcwd(), filename)
    
    if not os.path.exists(filepath):
        print(f"❌ {filename} - 파일 없음")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 확인 목록
    checks = {
        'passwordModal': 'id="passwordModal"' in content,
        'checkPassword()': 'function checkPassword()' in content,
        'checkPasswordStatus()': 'function checkPasswordStatus()' in content,
        'loadWorksheets()': 'function loadWorksheets()' in content,
        'loadTalentData()': 'function loadTalentData()' in content,
        'studentData': 'const studentData' in content,
        'addEventListener load': "window.addEventListener('load'" in content,
        'CORRECT_PASSWORD': 'const CORRECT_PASSWORD' in content,
    }
    
    print(f"\n{student.upper()}:")
    all_good = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        if not result:
            all_good = False
    
    if all_good:
        print(f"  ➜ {filename} 상태: 정상")
    else:
        print(f"  ➜ {filename} 상태: 문제 있음 ⚠️")

print("\n" + "=" * 60)
