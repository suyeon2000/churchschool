#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

students = {
    'yerim': 'yerim',
    'joshua': 'joshua',
    'elliot': 'elliot',
    'anna': 'anna',
    'moses': 'moses',
}

talent_function = '''        function loadTalentData() {
            fetch('/get-talents')
                .then(r => {
                    if (!r.ok) throw new Error('API not available');
                    return r.json();
                })
                .then(data => {
                    if (data.success) {
                        const count = data.talents.{STUDENT_ID} || 0;
                        document.getElementById('talentCount').textContent = '⭐ ' + count + '개';
                    }
                })
                .catch(e => {
                    // API 실패 시 talents_data.json 직접 로드
                    fetch('talents_data.json')
                        .then(r => r.json())
                        .then(talents => {
                            const count = talents.{STUDENT_ID} || 0;
                            document.getElementById('talentCount').textContent = '⭐ ' + count + '개';
                        })
                        .catch(e => console.error('오류:', e));
                });
        }
'''

for filename_key, student_id in students.items():
    filename = f'student_{filename_key}.html'
    filepath = os.path.join(os.getcwd(), filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} 없음")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 이미 함수가 있는지 확인
    if 'loadTalentData' in content:
        print(f"⏭️  {filename} - 이미 loadTalentData 함수 있음")
        continue
    
    # 함수 추가 (updateStudentTalents 함수 이전에)
    talent_func = talent_function.replace('{STUDENT_ID}', student_id)
    
    # checkPasswordStatus 함수 이후에 추가
    if 'function checkPasswordStatus' in content:
        content = content.replace(
            '        }\n\n        function updateStudentTalents',
            f'        }}\n\n{talent_func}\n\n        function updateStudentTalents'
        )
    else:
        # updateStudentTalents 이전에 추가
        content = re.sub(
            r'(        function updateStudentTalents)',
            talent_func + r'\n\n\1',
            content
        )
    
    # checkPassword에서 loadTalentData 호출 추가
    if 'checkPassword()' in content and 'loadTalentData()' not in content:
        # checkPassword 함수 안에서 모달을 닫은 후 loadTalentData 호출
        content = content.replace(
            'document.getElementById(\'passwordModal\').classList.add(\'hidden\');',
            'document.getElementById(\'passwordModal\').classList.add(\'hidden\');\n                loadTalentData();'
        )
    
    # checkPasswordStatus에서도 loadTalentData 호출 추가
    if 'checkPasswordStatus()' in content and 'loadTalentData()' not in content:
        # else 블록에서 loadTalentData 호출
        content = content.replace(
            'modal.classList.add(\'hidden\');\n            } else {',
            'modal.classList.add(\'hidden\');\n            } else {'
        )
        if '} else {\n                modal.classList.add(\'hidden\')' in content:
            content = content.replace(
                '} else {\n                modal.classList.add(\'hidden\');',
                '} else {\n                modal.classList.add(\'hidden\');\n                loadTalentData();'
            )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} - loadTalentData 함수 추가")

print("\n✨ 모든 학생 파일에 달란트 데이터 연결 완료!")
