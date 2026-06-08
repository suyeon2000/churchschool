#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

# 학생 정보 (Junyoung 제외)
students = {
    'joshua': {'password': '4780', 'name': 'Joshua', 'avatar': 'Jo'},
    'elliot': {'password': 'winter', 'name': 'Elliot', 'avatar': 'E'},
    'anna': {'password': '921', 'name': 'Anna', 'avatar': 'A'},
    'moses': {'password': '1251', 'name': 'Moses', 'avatar': 'M'},
}

# CSS 패턴
password_css = '''
        /* 비밀번호 모달 */
        .password-modal {
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
        }

        .password-modal.hidden {
            display: none;
        }

        .password-box {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 400px;
            width: 90%;
        }

        .password-box h2 {
            color: #3B5998;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .password-box p {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.05em;
        }

        .password-input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1.05em;
            margin-bottom: 20px;
        }

        .password-input:focus {
            outline: none;
            border-color: #3B5998;
        }

        .password-button {
            width: 100%;
            padding: 12px 20px;
            background: linear-gradient(135deg, #3B5998 0%, #8B6BB8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.05em;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .password-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 89, 152, 0.3);
        }

        .password-error {
            color: #d32f2f;
            margin-top: 15px;
            display: none;
            font-size: 0.95em;
        }
'''

def update_student_file(filename, student_id, password, name, avatar):
    filepath = os.path.join(os.getcwd(), filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} 파일 없음")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. CSS 추가 (첫 번째 <style> 태그 안에)
    if '.password-modal' not in content:
        # <style> 직후에 CSS 추가 (nav 스타일 이전)
        content = re.sub(
            r'(</style>)',
            password_css + r'\n    \1',
            content,
            count=1
        )
    
    # 2. HTML 추가 (<body> 직후에 passwordModal)
    if 'passwordModal' not in content:
        password_html = f'''    <!-- 비밀번호 모달 -->
    <div id="passwordModal" class="password-modal">
        <div class="password-box">
            <h2>🔐 비밀번호 입력</h2>
            <p>{name}의 학습자료를 보시려면 비밀번호를 입력하세요.</p>
            <input type="password" id="passwordInput" class="password-input" placeholder="비밀번호 입력" onkeyup="if(event.key==='Enter') checkPassword()">
            <button class="password-button" onclick="checkPassword()">확인</button>
            <div id="passwordError" class="password-error">비밀번호가 잘못되었습니다!</div>
        </div>
    </div>

'''
        content = content.replace('<body>\n    <nav>', f'<body>\n{password_html}    <nav>')
    
    # 3. JavaScript 추가 (<script> 직후에)
    if 'checkPassword' not in content:
        password_js = f'''        const CORRECT_PASSWORD = "{password}";
        const STUDENT_ID = "{student_id}";

        function checkPassword() {{
            const input = document.getElementById('passwordInput');
            const password = input.value;
            const errorMsg = document.getElementById('passwordError');

            if (password === CORRECT_PASSWORD) {{
                sessionStorage.setItem(`password_${{STUDENT_ID}}`, 'verified');
                document.getElementById('passwordModal').classList.add('hidden');
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
            }}
        }}

'''
        content = content.replace('<script>\n', f'<script>\n{password_js}')
    
    # 4. window.addEventListener 수정
    if 'checkPasswordStatus' not in content:
        # 기존 addEventListener를 checkPasswordStatus 호출로 변경
        content = re.sub(
            r'window\.addEventListener\(["\']load["\']\s*,\s*function\s*\(\)\s*\{',
            'window.addEventListener(\'load\', function() {\n            checkPasswordStatus();\n        });\n        window.addEventListener(\'load\', function() {',
            content
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} ({name}) 업데이트 완료 - 비밀번호: {password}")

# 모든 학생 파일 업데이트
for student_id, info in students.items():
    filename = f'student_{student_id}.html'
    update_student_file(filename, student_id, info['password'], info['name'], info['avatar'])

print("\n✨ 모든 학생 페이지 패스워드 설정 완료!")
