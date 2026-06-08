#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 학생 페이지를 표준 형식(Yerim 형식)으로 자동 표준화
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import re

# 학생별 설정
STUDENTS = {
    'junyoung': {
        'name': 'Junyoung',
        'initial': 'J',
        'password': 'BALD',
        'avatar_gradient': '#3B5998 0%, #2E4A7A 100%',
        'color_primary': '#3B5998',
        'color_secondary': '#8B6BB8'
    },
    'yerim': {
        'name': 'Yerim',
        'initial': 'Y',
        'password': '9393',
        'avatar_gradient': '#8B6BB8 0%, #6B4D8D 100%',
        'color_primary': '#8B6BB8',
        'color_secondary': '#6B4D8D'
    },
    'joshua': {
        'name': 'Joshua',
        'initial': 'Jo',
        'password': '4780',
        'avatar_gradient': '#2E7D32 0%, #4CAF50 100%',
        'color_primary': '#2E7D32',
        'color_secondary': '#4CAF50'
    },
    'elliot': {
        'name': 'Elliot',
        'initial': 'E',
        'password': 'winter',
        'avatar_gradient': '#F57C00 0%, #FFA726 100%',
        'color_primary': '#F57C00',
        'color_secondary': '#FFA726'
    },
    'anna': {
        'name': 'Anna',
        'initial': 'A',
        'password': '921',
        'avatar_gradient': '#C2185B 0%, #E91E63 100%',
        'color_primary': '#C2185B',
        'color_secondary': '#E91E63'
    },
    'moses': {
        'name': 'Moses',
        'initial': 'M',
        'password': '1251',
        'avatar_gradient': '#E53935 0%, #F44336 100%',
        'color_primary': '#E53935',
        'color_secondary': '#F44336'
    }
}

def generate_html(student_id, student_info):
    """표준 형식 HTML 생성"""
    
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{student_info['name']} - 한영교회 주일학교</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            color: #333;
        }}

        /* 비밀번호 모달 */
        .password-modal {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }}

        .password-modal.hidden {{
            display: none;
        }}

        .password-box {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 400px;
            width: 90%;
        }}

        .password-box h2 {{
            color: {student_info['color_primary']};
            margin-bottom: 20px;
            font-size: 1.5em;
        }}

        .password-box p {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.05em;
        }}

        .password-input {{
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1.05em;
            margin-bottom: 20px;
        }}

        .password-input:focus {{
            outline: none;
            border-color: {student_info['color_primary']};
        }}

        .password-button {{
            width: 100%;
            padding: 12px 20px;
            background: linear-gradient(135deg, {student_info['color_primary']} 0%, {student_info['color_secondary']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.05em;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .password-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 89, 152, 0.3);
        }}

        .password-error {{
            color: #d32f2f;
            margin-top: 15px;
            display: none;
            font-size: 0.95em;
        }}

        nav {{
            background: linear-gradient(135deg, #3B5998 0%, #8B6BB8 100%);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        nav ul {{
            list-style: none;
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
            transition: color 0.3s ease;
        }}

        nav a:hover {{
            color: #FFD700;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .profile-header {{
            background: white;
            padding: 40px 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 40px;
            text-align: center;
            border-top: 5px solid {student_info['color_primary']};
        }}

        .student-avatar {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, {student_info['avatar_gradient']});
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 3em;
            color: white;
            box-shadow: 0 10px 30px rgba(139, 107, 184, 0.3);
        }}

        .profile-header h1 {{
            color: {student_info['color_primary']};
            font-size: 2.5em;
            margin-bottom: 15px;
        }}

        .profile-subtitle {{
            color: #999;
            font-size: 1.1em;
            margin-bottom: 20px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }}

        .info-box {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid {student_info['color_primary']};
        }}

        .info-label {{
            color: #999;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .info-value {{
            color: {student_info['color_primary']};
            font-size: 1.8em;
            font-weight: bold;
        }}

        .section {{
            background: white;
            padding: 40px 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 40px;
        }}

        .section h2 {{
            color: {student_info['color_primary']};
            font-size: 1.8em;
            margin-bottom: 30px;
            border-bottom: 3px solid #FFD700;
            padding-bottom: 15px;
        }}

        .worksheets-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .worksheet {{
            background: #f5f5f5;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}

        .worksheet:hover {{
            transform: translateY(-5px);
        }}

        .worksheet img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .worksheet-info {{
            padding: 12px;
            background: white;
        }}

        .worksheet-date {{
            color: #999;
            font-size: 0.85em;
        }}

        .worksheet-title {{
            color: {student_info['color_primary']};
            font-weight: 600;
            margin-top: 5px;
        }}

        .talents-display {{
            background: linear-gradient(135deg, #fff9e6 0%, #fffacd 100%);
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }}

        .talent-count {{
            font-size: 3em;
            color: #FFD700;
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .talent-label {{
            color: #666;
            font-size: 1.1em;
        }}

        .empty-message {{
            text-align: center;
            padding: 40px 20px;
            color: #999;
        }}

        .empty-message .icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}

        footer {{
            background: #3B5998;
            color: white;
            text-align: center;
            padding: 30px 20px;
            margin-top: 60px;
        }}

        @media (max-width: 768px) {{
            .info-grid {{
                grid-template-columns: 1fr;
            }}
            .worksheets-grid {{
                grid-template-columns: 1fr;
            }}
            nav ul {{
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <!-- 비밀번호 모달 -->
    <div id="passwordModal" class="password-modal">
        <div class="password-box">
            <h2>🔐 비밀번호 입력</h2>
            <p>{student_info['name']}의 학습자료를 보시려면 비밀번호를 입력하세요.</p>
            <input type="password" id="passwordInput" class="password-input" placeholder="비밀번호 입력" onkeyup="if(event.key==='Enter') checkPassword()">
            <button class="password-button" onclick="checkPassword()">확인</button>
            <div id="passwordError" class="password-error">비밀번호가 잘못되었습니다!</div>
        </div>
    </div>

    <!-- 네비게이션 -->
    <nav>
        <ul>
            <li><a href="index.html">🏠 홈</a></li>
            <li><a href="learning.html">📚 학습자료</a></li>
            <li><a href="talents.html">⭐ 달란트</a></li>
        </ul>
    </nav>

    <!-- 메인 컨테이너 -->
    <div class="container">
        <!-- 프로필 헤더 -->
        <div class="profile-header">
            <div class="student-avatar">{student_info['initial']}</div>
            <h1>{student_info['name']}</h1>
            <p class="profile-subtitle">한영교회 주일학교 학생</p>

            <div class="info-grid">
                <div class="info-box">
                    <div class="info-label">보유 달란트</div>
                    <div class="info-value" id="talentCount">⭐ 0개</div>
                </div>
                <div class="info-box">
                    <div class="info-label">상태</div>
                    <div class="info-value">✨ 활동 중</div>
                </div>
            </div>
        </div>

        <!-- 학습자료 섹션 -->
        <div class="section">
            <h2>📚 {student_info['name']}의 학습자료</h2>
            <div id="worksheetContainer">
                <div class="empty-message"><div class="icon">📝</div><p>아직 게시된 학습자료가 없습니다.<br>수업 후에 학습지 사진이 업로드됩니다.</p></div>
            </div>
        </div>

        <!-- 달란트 섹션 -->
        <div class="section">
            <h2>⭐ 달란트</h2>
            <p style="color: #666; margin-bottom: 20px;">
                {student_info['name']}의 수업 참여도를 보여줍니다.
            </p>

            <div class="talents-display">
                <div class="talent-label">현재 보유 달란트</div>
                <div class="talent-count">⭐ <span id="talentCountDisplay">0</span>개</div>
                <div class="talent-label">화이팅! 💪</div>
            </div>
        </div>
    </div>

    <!-- 푸터 -->
    <footer>
        <p>&copy; 2024 한영교회 주일학교. All rights reserved.</p>
    </footer>

    <script>
        const CORRECT_PASSWORD = "{student_info['password']}";
        const STUDENT_ID = "{student_id}";

        function checkPassword() {{
            const input = document.getElementById('passwordInput');
            const password = input.value;
            const errorMsg = document.getElementById('passwordError');

            if (password === CORRECT_PASSWORD) {{
                sessionStorage.setItem(`password_${{STUDENT_ID}}`, 'verified');
                document.getElementById('passwordModal').classList.add('hidden');
                loadTalentData();
                loadWorksheets();
            }} else {{
                errorMsg.style.display = 'block';
                input.value = '';
                input.focus();
            }}
        }}

        function checkPasswordStatus() {{
            const isVerified = sessionStorage.getItem(`password_${{STUDENT_ID}}`) === 'verified';
            const modal = document.getElementById('passwordModal');

            if (!isVerified) {{
                modal.classList.remove('hidden');
                document.getElementById('passwordInput').focus();
            }} else {{
                modal.classList.add('hidden');
                loadTalentData();
                loadWorksheets();
            }}
        }}

        function loadTalentData() {{
            fetch('/get-talents')
                .then(r => {{
                    if (!r.ok) throw new Error('API not available');
                    return r.json();
                }})
                .then(data => {{
                    if (data.success) {{
                        const count = data.talents[STUDENT_ID] || 0;
                        document.getElementById('talentCount').textContent = '⭐ ' + count + '개';
                        document.getElementById('talentCountDisplay').textContent = count;
                    }}
                }})
                .catch(e => {{
                    fetch('talents_data.json')
                        .then(r => r.json())
                        .then(talents => {{
                            const count = talents[STUDENT_ID] || 0;
                            document.getElementById('talentCount').textContent = '⭐ ' + count + '개';
                            document.getElementById('talentCountDisplay').textContent = count;
                        }});
                }});
        }}

        function loadWorksheets() {{
            const container = document.getElementById('worksheetContainer');
            container.style.display = 'block';
            container.style.width = '100%';

            const worksheets = studentData[STUDENT_ID].worksheets;

            if (worksheets.length === 0) {{
                container.innerHTML = '<div class="empty-message"><div class="icon">📝</div><p>아직 게시된 학습자료가 없습니다.<br>수업 후에 학습지 사진이 업로드됩니다.</p></div>';
                return;
            }}

            const groupedByDate = {{}};
            worksheets.forEach(sheet => {{
                if (!groupedByDate[sheet.date]) {{
                    groupedByDate[sheet.date] = [];
                }}
                groupedByDate[sheet.date].push(sheet);
            }});

            const sortedDates = Object.keys(groupedByDate).sort((a, b) => new Date(b) - new Date(a));

            let html = '';
            sortedDates.forEach(date => {{
                const dateObj = new Date(date);
                const formattedDate = dateObj.toLocaleDateString('ko-KR', {{
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                }});

                html += '<div style="display: block !important; width: 100% !important; margin-bottom: 40px !important;">';
                html += `<h3 style="color: #3B5998; margin-bottom: 15px; font-size: 1.2em; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">📅 ${{formattedDate}}</h3>`;
                html += '<div class="worksheets-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">';

                groupedByDate[date].forEach(sheet => {{
                    html += '<div class="worksheet">';
                    html += `<img src="${{sheet.image}}" alt="${{sheet.title}}" style="width: 100%; height: auto;">`;
                    html += '<div class="worksheet-info">';
                    html += `<div class="worksheet-title">${{sheet.title}}</div>`;
                    html += `<div class="worksheet-date">${{date}}</div>`;
                    html += '</div></div>';
                }});

                html += '</div></div>';
            }});

            container.innerHTML = html;
        }}

        const studentData = {{
            junyoung: {{
                name: 'Junyoung',
                worksheets: []
            }},
            yerim: {{
                name: 'Yerim',
                worksheets: []
            }},
            joshua: {{
                name: 'Joshua',
                worksheets: []
            }},
            elliot: {{
                name: 'Elliot',
                worksheets: []
            }},
            anna: {{
                name: 'Anna',
                worksheets: []
            }},
            moses: {{
                name: 'Moses',
                worksheets: []
            }}
        }};

        window.addEventListener('load', function() {{
            checkPasswordStatus();
        }});
    </script>
</body>
</html>
'''
    return html

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("모든 학생 페이지 표준화")
    print("=" * 70)
    
    updated = 0
    for student_id, student_info in STUDENTS.items():
        student_file = os.path.join(project_dir, f'student_{student_id}.html')
        html_content = generate_html(student_id, student_info)
        
        with open(student_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ student_{student_id}.html 표준화 완료")
        updated += 1
    
    print("\n" + "=" * 70)
    print(f"✅ 총 {updated}개 파일이 표준화되었습니다!")
    print("=" * 70)

if __name__ == '__main__':
    main()
