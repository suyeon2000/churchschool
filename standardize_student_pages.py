#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

# 학생 정보
students = {
    'junyoung': {'name': 'Junyoung', 'avatar': 'J', 'password': 'BALD', 'color': '#3B5998', 'prev': None, 'next': 'yerim'},
    'yerim': {'name': 'Yerim', 'avatar': 'Y', 'password': '9393', 'color': '#8B6BB8', 'prev': 'junyoung', 'next': 'joshua'},
    'joshua': {'name': 'Joshua', 'avatar': 'Jo', 'password': '4780', 'color': '#2E7D32', 'prev': 'yerim', 'next': 'elliot'},
    'elliot': {'name': 'Elliot', 'avatar': 'E', 'password': 'winter', 'color': '#F57C00', 'prev': 'joshua', 'next': 'anna'},
    'anna': {'name': 'Anna', 'avatar': 'A', 'password': '921', 'color': '#C2185B', 'prev': 'elliot', 'next': 'moses'},
    'moses': {'name': 'Moses', 'avatar': 'M', 'password': '1251', 'color': '#E53935', 'prev': 'anna', 'next': None},
}

for student_id, info in students.items():
    filename = f'student_{student_id}.html'
    filepath = os.path.join(os.getcwd(), filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} 없음")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 달란트 표시 칸의 ID를 talentCount로 통일
    # info-value 중 첫 번째를 찾아서 ID 추가
    content = re.sub(
        r'<div class="info-label">보유 달란트</div>\s*<div class="info-value">',
        '<div class="info-label">보유 달란트</div>\n                    <div class="info-value" id="talentCount">',
        content
    )
    
    # 2. profile-header 구조 확인 및 필요시 수정
    # h1이 있는지 확인하고, 없으면 추가
    if '<h1>' not in content:
        content = re.sub(
            r'<div class="student-avatar">[^<]*</div>',
            f'<div class="student-avatar">{info["avatar"]}</div>\n            <h1>{info["name"]}</h1>',
            content
        )
    
    # 3. 학습자료 섹션이 있는지 확인
    if '📚' not in content or '학습자료' not in content:
        # worksheetContainer가 있는지 확인
        if 'worksheetContainer' not in content:
            # section 추가 필요
            section_html = f'''        <div class="section">
            <h2>📚 학습자료</h2>
            <p style="color: #666; margin-bottom: 20px;">
                {info['name']}의 주간 학습 기록입니다.
            </p>

            <div id="worksheetContainer" class="worksheets-grid">
                <div class="empty-message" style="grid-column: 1 / -1;">
                    <div class="icon">📂</div>
                    <p>아직 업로드된 학습자료가 없습니다.</p>
                </div>
            </div>
        </div>
'''
            # nav-buttons 이후에 추가
            if 'nav-buttons' in content:
                content = re.sub(
                    r'(</div>)\s*(<!-- 푸터)',
                    f'\n{section_html}\n\n        \\1\n\n    \\2',
                    content
                )
    
    # 4. loadWorksheets 함수가 호출되는지 확인
    if 'loadWorksheets()' not in content and 'checkPassword' in content:
        # checkPassword에서 호출되도록 추가
        content = content.replace(
            'loadTalentData();\n                loadWorksheets();',
            'loadTalentData();\n                loadWorksheets();'
        )
        if 'loadTalentData();' in content and 'loadWorksheets()' not in content:
            content = content.replace(
                'loadTalentData();',
                'loadTalentData();\n                loadWorksheets();'
            )
    
    # 5. 네비게이션 버튼 확인 및 수정
    nav_buttons_html = '        <div class="nav-buttons">\n'
    if info['prev']:
        nav_buttons_html += f'            <a href="student_{info["prev"]}.html" class="nav-btn">← {students[info["prev"]]["name"]}</a>\n'
    else:
        nav_buttons_html += '            <a href="learning.html" class="nav-btn">← 학습자료 보기</a>\n'
    
    nav_buttons_html += '            <a href="learning.html" class="nav-btn">학습자료 보기</a>\n'
    
    if info['next']:
        nav_buttons_html += f'            <a href="student_{info["next"]}.html" class="nav-btn">{students[info["next"]]["name"]} →</a>\n'
    else:
        nav_buttons_html += '            <a href="learning.html" class="nav-btn">학습자료 보기 →</a>\n'
    
    nav_buttons_html += '        </div>'
    
    # 기존 nav-buttons 제거 및 새로 추가
    content = re.sub(
        r'<div class="nav-buttons">.*?</div>',
        nav_buttons_html,
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} - 형식 통일 및 달란트 데이터 연결 완료")

print("\n✨ 모든 학생 페이지 형식 통일 완료!")
