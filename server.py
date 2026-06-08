#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
학습자료 관리 로컬 서버
"""

from flask import Flask, jsonify, request, send_from_directory
import subprocess
import os
import sys
import json
import webbrowser
import threading
import time

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_html_file(filename):
    """HTML 파일을 읽어서 반환"""
    try:
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "파일을 찾을 수 없습니다.", 404

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>학습자료 관리</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                padding: 40px;
                max-width: 500px;
                width: 100%;
            }
            h1 {
                color: #3B5998;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 40px;
                font-size: 1.05em;
            }
            .tools {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 30px;
            }
            .tool-btn {
                padding: 25px 20px;
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                font-size: 1.05em;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: center;
            }
            .tool-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
            }
            .btn-file {
                background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
            }
            .btn-update {
                background: linear-gradient(135deg, #F57C00 0%, #D84315 100%);
            }
            .btn-deploy {
                background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
                grid-column: 1 / -1;
            }
            .btn-admin {
                background: linear-gradient(135deg, #7B1FA2 0%, #4A148C 100%);
                grid-column: 1 / -1;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                justify-content: center;
            }
            .btn-admin:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
            }
            .status {
                text-align: center;
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                display: none;
                font-weight: 500;
            }
            .status.show { display: block; }
            .status.success { background: #c8e6c9; color: #2e7d32; }
            .status.error { background: #ffcdd2; color: #d32f2f; }
            .status.loading { background: #e3f2fd; color: #1976d2; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 학습자료 관리</h1>
            <p class="subtitle">빠른 도구 모음</p>

            <div class="tools">
                <button class="tool-btn btn-file" onclick="runFileProcess()">
                    📁 파일<br>자동 처리
                </button>
                <button class="tool-btn btn-update" onclick="runUpdate()">
                    🔄 자동<br>업데이트
                </button>
                <button class="tool-btn btn-deploy" onclick="runGitPush()">
                    📤 GitHub에 배포
                </button>
                <a href="/admin.html" class="tool-btn btn-admin">
                    🔐 달란트 관리
                </a>
            </div>

            <div id="status" class="status"></div>
        </div>

        <script>
            function showStatus(type, message) {
                const el = document.getElementById('status');
                el.className = 'status show ' + type;
                el.textContent = message;
                console.log('Status:', type, message);
            }

            function runFileProcess() {
                console.log('파일 자동 처리 시작...');
                showStatus('loading', '⏳ 파일 자동 처리 프로그램을 실행하는 중...');

                fetch('/run-file-process')
                    .then(r => {
                        console.log('응답 상태:', r.status);
                        return r.json();
                    })
                    .then(data => {
                        console.log('응답 데이터:', data);
                        if (data.success) {
                            showStatus('success', '✅ 파일 자동 처리 프로그램이 실행되었습니다!');
                        } else {
                            showStatus('error', '❌ 오류: ' + data.message);
                        }
                    })
                    .catch(e => {
                        console.error('오류:', e);
                        showStatus('error', '❌ 오류: ' + e.message);
                    });
            }

            function runUpdate() {
                console.log('자동 업데이트 시작...');
                showStatus('loading', '⏳ 자동 업데이트를 실행하는 중...');

                fetch('/run-update')
                    .then(r => {
                        console.log('응답 상태:', r.status);
                        return r.json();
                    })
                    .then(data => {
                        console.log('응답 데이터:', data);
                        if (data.success) {
                            showStatus('success', '✅ learning.html이 업데이트되었습니다!');
                        } else {
                            showStatus('error', '❌ 오류: ' + data.message);
                        }
                    })
                    .catch(e => {
                        console.error('오류:', e);
                        showStatus('error', '❌ 오류: ' + e.message);
                    });
            }

            function runGitPush() {
                console.log('GitHub 업로드 시작...');
                showStatus('loading', '⏳ GitHub에 업로드하는 중 (1-3분 소요)...');

                fetch('/run-git-push')
                    .then(r => {
                        console.log('응답 상태:', r.status);
                        return r.json();
                    })
                    .then(data => {
                        console.log('응답 데이터:', data);
                        if (data.success) {
                            showStatus('success', '✅ ' + data.message);
                        } else {
                            showStatus('error', '❌ 오류: ' + data.message);
                        }
                    })
                    .catch(e => {
                        console.error('오류:', e);
                        showStatus('error', '❌ 오류: ' + e.message);
                    });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/run-file-process')
def run_file_process():
    try:
        script_path = os.path.join(PROJECT_DIR, '학습자료_파일_업로드.py')

        # GUI 프로그램 실행 (Windows에서 분리된 프로세스로 실행)
        if sys.platform == 'win32':
            subprocess.Popen(['python', script_path],
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(['python', script_path])

        return jsonify({'success': True, 'message': '파일 자동 처리 프로그램이 실행되었습니다!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류: {str(e)}'})

@app.route('/run-update')
def run_update():
    try:
        script_path = os.path.join(PROJECT_DIR, 'update_learning_files.py')
        result = subprocess.run(['python', script_path], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'learning.html이 업데이트되었습니다.'})
        else:
            return jsonify({'success': False, 'message': result.stderr})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/run-git-push')
def run_git_push():
    try:
        os.chdir(PROJECT_DIR)

        # 1. git add -A
        subprocess.run(['git', 'add', '-A'], capture_output=True, text=True, timeout=10)

        # 2. git commit
        subprocess.run(['git', 'commit', '-m', '새 학습자료 추가', '--allow-empty'], capture_output=True, text=True, timeout=10)

        # 3. git push
        result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'GitHub에 업로드되었습니다! 1-3분 후 GitHub Pages에 반영됩니다.'})
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return jsonify({'success': False, 'message': f'Git 오류: {error_msg}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류: {str(e)}'})

@app.route('/get-talents')
def get_talents():
    try:
        talents_file = os.path.join(PROJECT_DIR, 'talents_data.json')
        with open(talents_file, 'r', encoding='utf-8') as f:
            talents = json.load(f)
        return jsonify({'success': True, 'talents': talents})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류: {str(e)}'})

@app.route('/save-talents', methods=['POST'])
def save_talents():
    try:
        data = request.get_json()
        talents = data.get('talents', {})

        talents_file = os.path.join(PROJECT_DIR, 'talents_data.json')
        with open(talents_file, 'w', encoding='utf-8') as f:
            json.dump(talents, f, ensure_ascii=False, indent=2)

        return jsonify({'success': True, 'message': '달란트 데이터가 저장되었습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류: {str(e)}'})

# HTML 파일 경로들
@app.route('/admin.html')
def admin_page():
    return read_html_file('admin.html')

@app.route('/talents.html')
def talents_page():
    return read_html_file('talents.html')

@app.route('/learning.html')
def learning_page():
    return read_html_file('learning.html')

@app.route('/index.html')
def index_page():
    return read_html_file('index.html')

# 학생 페이지들
@app.route('/student_junyoung.html')
def student_junyoung_page():
    return read_html_file('student_junyoung.html')

@app.route('/student_yerim.html')
def student_yerim_page():
    return read_html_file('student_yerim.html')

@app.route('/student_joshua.html')
def student_joshua_page():
    return read_html_file('student_joshua.html')

@app.route('/student_elliot.html')
def student_elliot_page():
    return read_html_file('student_elliot.html')

@app.route('/student_anna.html')
def student_anna_page():
    return read_html_file('student_anna.html')

@app.route('/student_moses.html')
def student_moses_page():
    return read_html_file('student_moses.html')

# 이미지 파일 제공
@app.route('/picture/<filename>')
def serve_picture(filename):
    try:
        picture_dir = os.path.join(PROJECT_DIR, 'picture')
        return send_from_directory(picture_dir, filename)
    except:
        return "파일을 찾을 수 없습니다.", 404

if __name__ == '__main__':
    print("=" * 60)
    print("📚 학습자료 관리 서버 시작")
    print("=" * 60)
    print("\n🌐 브라우저에서 열기:")
    print("   http://localhost:5000")
    print("\n⚠️  이 창을 닫으면 서버가 종료됩니다.")
    print("=" * 60 + "\n")

    # 별도 스레드에서 브라우저 자동으로 열기
    def open_browser():
        time.sleep(2)  # 서버가 시작될 때까지 대기
        webbrowser.open('http://localhost:5000')
        print("🌐 브라우저가 열렸습니다!\n")

    threading.Thread(target=open_browser, daemon=True).start()

    app.run(debug=False, port=5000)
