#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

students = {
    'yerim': {'password': '9393'},
    'joshua': {'password': '4780'},
    'elliot': {'password': 'winter'},
    'anna': {'password': '921'},
    'moses': {'password': '1251'},
}

javascript_template = '''    <script>
        const CORRECT_PASSWORD = "{PASSWORD}";
        const STUDENT_ID = "{STUDENT_ID}";

        function checkPassword() {{
            const input = document.getElementById('passwordInput');
            const password = input.value;
            const errorMsg = document.getElementById('passwordError');

            if (password === CORRECT_PASSWORD) {{
                // 비밀번호 맞음 - sessionStorage에 저장
                sessionStorage.setItem(`password_${{STUDENT_ID}}`, 'verified');
                document.getElementById('passwordModal').classList.add('hidden');
                loadTalentData();
                loadWorksheets();
            }} else {{
                // 비밀번호 틀림
                errorMsg.style.display = 'block';
                input.value = '';
                input.focus();
            }}
        }}

        // 페이지 로드 시 비밀번호 확인
        function checkPasswordStatus() {{
            const isVerified = sessionStorage.getItem(`password_${{STUDENT_ID}}`) === 'verified';
            const modal = document.getElementById('passwordModal');

            if (!isVerified) {{
                // 비밀번호 미입력 - 모달 표시
                modal.classList.remove('hidden');
                document.getElementById('passwordInput').focus();
            }} else {{
                // 이미 비밀번호 입력됨 - 모달 숨김
                modal.classList.add('hidden');
                loadTalentData();
                loadWorksheets();
            }}
        }}

        // 달란트 데이터 로드
        function loadTalentData() {{
            fetch('/get-talents')
                .then(r => {{
                    if (!r.ok) throw new Error('API not available');
                    return r.json();
                }})
                .then(data => {{
                    if (data.success) {{
                        const count = data.talents.{STUDENT_ID} || 0;
                        document.getElementById('talentCount').textContent = '⭐ ' + count + '개';
                    }}
                }})
                .catch(e => {{
                    // API 실패 시 talents_data.json 직접 로드
                    fetch('talents_data.json')
                        .then(r => r.json())
                        .then(talents => {{
                            const count = talents.{STUDENT_ID} || 0;
                            document.getElementById('talentCount').textContent = '⭐ ' + count + '개';
                        }})
                        .catch(e => console.error('오류:', e));
                }});
        }}

        // 학습자료 로드
        function loadWorksheets() {{
            const container = document.getElementById('worksheetContainer');

            // 컨테이너 CSS 초기화
            container.style.display = 'block';
            container.style.width = '100%';
            container.style.flexWrap = 'wrap';

            const worksheets = studentData.{STUDENT_ID}.worksheets;

            if (worksheets.length === 0) {{
                container.innerHTML = '<div class="empty-message"><div class="icon">📝</div><p>아직 게시된 학습자료가 없습니다.<br>수업 후에 학습지 사진이 업로드됩니다.</p></div>';
                return;
            }}

            // 날짜별로 그룹화
            const groupedByDate = {{}};
            worksheets.forEach(sheet => {{
                if (!groupedByDate[sheet.date]) {{
                    groupedByDate[sheet.date] = [];
                }}
                groupedByDate[sheet.date].push(sheet);
            }});

            // 날짜순으로 정렬 (최신순)
            const sortedDates = Object.keys(groupedByDate).sort((a, b) => new Date(b) - new Date(a));

            // HTML 생성
            let html = '';
            sortedDates.forEach(date => {{
                const dateObj = new Date(date);
                const formattedDate = dateObj.toLocaleDateString('ko-KR', {{
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                }});

                html += '<div style="display: block !important; width: 100% !important; clear: both !important; margin-bottom: 40px !important;">';
                html += `<h3 style="color: #3B5998; margin-bottom: 15px; font-size: 1.2em; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">📅 ${{formattedDate}}</h3>`;
                html += '<div class="worksheets-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">';

                groupedByDate[date].forEach(sheet => {{
                    html += '<div class="worksheet">';
                    html += `<img src="${{sheet.image}}" alt="${{sheet.title}}" style="width: 100%; height: auto; display: block;">`;
                    html += '<div class="worksheet-info">';
                    html += `<div class="worksheet-title">${{sheet.title}}</div>`;
                    html += `<div class="worksheet-date">${{date}}</div>`;
                    html += '</div></div>';
                }});

                html += '</div></div>';
            }});

            container.innerHTML = html;
        }}

        // 학생별 학습자료 데이터
        const studentData = {{
            junyoung: {{
                name: 'Junyoung',
                worksheets: [
                    {{ title: 'Page 1', date: '2026-05-31', image: 'picture/junyoung_20260531_1.jpg' }},
                    {{ title: 'Page 2', date: '2026-05-31', image: 'picture/junyoung_20260531_2.jpg' }},
                    {{ title: 'Page 1', date: '2026-06-07', image: 'picture/junyoung_20260607_1.jpg' }}
                ]
            }},
            yerim: {{
                name: 'Yerim',
                worksheets: [
                    {{ title: 'Page 1', date: '2026-05-31', image: 'picture/yerim_20260531_1.jpg' }},
                    {{ title: 'Page 2', date: '2026-05-31', image: 'picture/yerim_20260531_2.jpg' }},
                    {{ title: 'Page 1', date: '2026-06-07', image: 'picture/yerim_20260607_1.jpg' }}
                ]
            }},
            joshua: {{
                name: 'Joshua',
                worksheets: [
                    {{ title: 'Page 1', date: '2026-05-31', image: 'picture/joshua_20260531_1.jpg' }},
                    {{ title: 'Page 2', date: '2026-05-31', image: 'picture/joshua_20260531_2.jpg' }},
                    {{ title: 'Page 1', date: '2026-06-07', image: 'picture/joshua_20260607_1.jpg' }}
                ]
            }},
            elliot: {{
                name: 'Elliot',
                worksheets: [
                    {{ title: 'Page 1', date: '2026-05-31', image: 'picture/elliot_20260531_1.jpg' }},
                    {{ title: 'Page 2', date: '2026-05-31', image: 'picture/elliot_20260531_2.jpg' }},
                    {{ title: 'Page 1', date: '2026-06-07', image: 'picture/elliot_20260607_1.jpg' }}
                ]
            }},
            anna: {{
                name: 'Anna',
                worksheets: [
                    {{ title: 'Page 1', date: '2026-05-31', image: 'picture/anna_20260531_1.jpg' }},
                    {{ title: 'Page 2', date: '2026-05-31', image: 'picture/anna_20260531_2.jpg' }},
                    {{ title: 'Page 1', date: '2026-06-07', image: 'picture/anna_20260607_1.jpg' }}
                ]
            }},
            moses: {{
                name: 'Moses',
                worksheets: [
                    {{ title: 'Page 1', date: '2026-05-31', image: 'picture/moses_20260531_1.jpg' }},
                    {{ title: 'Page 2', date: '2026-05-31', image: 'picture/moses_20260531_2.jpg' }},
                    {{ title: 'Page 1', date: '2026-06-07', image: 'picture/moses_20260607_1.jpg' }}
                ]
            }}
        }};

        // 페이지 로드 시 비밀번호 상태 확인
        window.addEventListener('load', function() {{
            checkPasswordStatus();
        }});
    </script>'''

for student_id, info in students.items():
    filename = f'student_{student_id}.html'
    filepath = os.path.join(os.getcwd(), filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} 없음")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 기존 <script> 섹션 제거
    content = re.sub(r'    <script>.*?</script>', '', content, flags=re.DOTALL)
    
    # 새 JavaScript 추가
    new_js = javascript_template.replace('{PASSWORD}', info['password']).replace('{STUDENT_ID}', student_id)
    content = content.replace('    </body>', f'{new_js}\n    </body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} - 패스워드 함수 추가 완료")

print("\n✨ 모든 학생 페이지 수정 완료!")
