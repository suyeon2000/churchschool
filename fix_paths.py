#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

students = ['junyoung', 'yerim', 'joshua', 'elliot', 'anna', 'moses']

for student in students:
    filename = f'student_{student}.html'
    filepath = os.path.join(os.getcwd(), filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} 없음")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # /talents_data.json → talents_data.json으로 변경
    original_count = content.count("'/talents_data.json'")
    content = content.replace("'/talents_data.json'", "'talents_data.json'")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} - {original_count}개 경로 수정")

print("\n✨ 모든 경로 수정 완료!")
