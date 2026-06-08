#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
학습자료 자동 업데이트 스크립트
picture 폴더의 파일들을 감지하고 learning.html을 자동으로 업데이트합니다.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import re
from pathlib import Path

def get_project_dir():
    """현재 스크립트의 디렉토리를 프로젝트 디렉토리로 반환"""
    return os.path.dirname(os.path.abspath(__file__))

def scan_picture_folder(picture_dir):
    """picture 폴더의 모든 이미지 파일을 스캔하고 학생별로 정렬"""
    student_files = {
        'junyoung': [],
        'yerim': [],
        'joshua': [],
        'elliot': [],
        'anna': [],
        'moses': []
    }

    # 모든 이미지 파일 수집
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

    for filename in sorted(os.listdir(picture_dir)):
        if not filename.lower().endswith(image_extensions):
            continue

        # 파일명 파싱: 학생이름_날짜_페이지번호.확장자
        parts = filename.split('_')

        if len(parts) < 2:
            print(f"경고: '{filename}' - 파일명 형식이 올바르지 않습니다")
            continue

        student = parts[0]

        if student not in student_files:
            print(f"경고: '{filename}' - 알려지지 않은 학생 ({student})")
            continue

        date_str = parts[1]

        # YYYYMMDD 형식을 YYYY-MM-DD로 변환
        if len(date_str) == 8 and date_str.isdigit():
            date = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
        else:
            print(f"경고: '{filename}' - 날짜 형식이 올바르지 않습니다")
            continue

        # 같은 날짜의 파일 개수 계산
        page_num = len([f for f in student_files[student] if f["date"] == date]) + 1

        student_files[student].append({
            'title': f'Page {page_num}',
            'date': date,
            'image': f'picture/{filename}'
        })

    # 학생별 파일을 날짜별로 정렬
    for student in student_files:
        student_files[student] = sorted(student_files[student], key=lambda x: (x['date'], x['image']))

    return student_files

def generate_javascript_code(student_files):
    """JavaScript 코드 생성"""
    students_list = ['junyoung', 'yerim', 'joshua', 'elliot', 'anna', 'moses']

    js_code = "        const studentData = {\n"

    for idx, student in enumerate(students_list):
        files = student_files[student]
        js_code += f"            {student}: {{\n"
        js_code += f"                name: '{student.capitalize()}',\n"
        js_code += "                worksheets: [\n"

        for file in files:
            js_code += f"                    {{ title: '{file['title']}', date: '{file['date']}', image: '{file['image']}' }},\n"

        if files:
            js_code = js_code.rstrip(',\n') + "\n"

        js_code += "                ]\n"
        js_code += "            }"

        if idx < len(students_list) - 1:
            js_code += ",\n"
        else:
            js_code += "\n"

    js_code += "        };"

    return js_code

def update_learning_html(html_file, new_js_code):
    """learning.html 파일에서 studentData 부분을 업데이트"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 기존 const studentData {...}; 부분을 찾아 교체
    pattern = r'const studentData = \{[\s\S]*?\};'

    if not re.search(pattern, content):
        print("오류: learning.html에서 studentData 패턴을 찾을 수 없습니다")
        return False

    new_content = re.sub(pattern, new_js_code, content)

    # 파일 업데이트
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    print("=" * 70)
    print("학습자료 자동 업데이트 스크립트")
    print("=" * 70)

    project_dir = get_project_dir()
    picture_dir = os.path.join(project_dir, 'picture')
    html_file = os.path.join(project_dir, 'learning.html')

    # 디렉토리 존재 확인
    if not os.path.isdir(picture_dir):
        print(f"오류: picture 폴더를 찾을 수 없습니다 ({picture_dir})")
        return

    if not os.path.isfile(html_file):
        print(f"오류: learning.html 파일을 찾을 수 없습니다 ({html_file})")
        return

    print(f"\n프로젝트 경로: {project_dir}")
    print(f"picture 폴더: {picture_dir}")
    print(f"learning.html: {html_file}\n")

    # picture 폴더 스캔
    print("picture 폴더를 스캔하는 중...")
    student_files = scan_picture_folder(picture_dir)

    # 결과 출력
    print("\n스캔 결과:")
    print("-" * 70)
    total_files = 0
    for student, files in student_files.items():
        if files:
            print(f"\n  {student.upper()} ({len(files)}개 파일):")
            for file in files:
                print(f"    - {file['image']} ({file['date']})")
            total_files += len(files)
        else:
            print(f"\n  {student.upper()}: 파일 없음")

    print(f"\n  총 {total_files}개 파일 찾음")
    print("-" * 70)

    # JavaScript 코드 생성
    print("\nJavaScript 코드 생성 중...")
    js_code = generate_javascript_code(student_files)

    # learning.html 업데이트
    print("learning.html 업데이트 중...")
    success_count = 0
    if update_learning_html(html_file, js_code):
        print("✅ learning.html이 성공적으로 업데이트되었습니다!")
        success_count += 1

    # 각 학생 페이지도 업데이트
    students = ['junyoung', 'yerim', 'joshua', 'elliot', 'anna', 'moses']
    print("\n학생 페이지 업데이트 중...")
    for student_name in students:
        student_html = os.path.join(project_dir, f'student_{student_name}.html')
        if os.path.isfile(student_html):
            if update_learning_html(student_html, js_code):
                print(f"✅ student_{student_name}.html이 업데이트되었습니다!")
                success_count += 1
            else:
                print(f"⚠️  student_{student_name}.html 업데이트 실패")
        else:
            print(f"⚠️  student_{student_name}.html을 찾을 수 없습니다")

    if success_count > 0:
        print("\n" + "=" * 70)
        print(f"✅ 총 {success_count}개 파일이 업데이트되었습니다!")
        print("=" * 70)
        print("\n다음 단계:")
        print("  1. 웹 브라우저를 새로고침하세요")
        print("  2. learning.html과 학생 페이지에서 학습자료가 올바르게 표시되는지 확인하세요")
        print("\n팁:")
        print("  - 새 파일을 picture 폴더에 추가한 후 이 스크립트를 다시 실행하세요")
        print("  - 파일명 형식: 학생이름_YYYYMMDD_페이지번호.확장자")
        print("  - 예: junyoung_20260605_1.jpg\n")
    else:
        print("\n업데이트에 실패했습니다\n")

if __name__ == '__main__':
    main()
