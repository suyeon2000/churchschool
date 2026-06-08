#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
학습자료 자동 파일 처리 애플리케이션
파일을 선택하면 자동으로 올바른 파일명으로 변경하고 picture 폴더에 저장합니다.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from pathlib import Path

class 학습자료업로더:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 학습자료 파일 자동 처리")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # 프로젝트 디렉토리
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.picture_dir = os.path.join(self.project_dir, 'picture')

        # 학생 목록
        self.students = {
            'junyoung': 'Junyoung',
            'yerim': 'Yerim',
            'joshua': 'Joshua',
            'elliot': 'Elliot',
            'anna': 'Anna',
            'moses': 'Moses'
        }

        self.setup_ui()

    def setup_ui(self):
        # 제목
        title = tk.Label(
            self.root,
            text="📚 학습자료 파일 자동 처리",
            font=("Arial", 16, "bold"),
            fg="#3B5998"
        )
        title.pack(pady=20)

        # 학생 선택
        student_frame = tk.Frame(self.root)
        student_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(student_frame, text="학생 선택:", font=("Arial", 10, "bold")).pack(side="left")
        self.student_var = tk.StringVar()
        student_menu = tk.OptionMenu(
            student_frame,
            self.student_var,
            *self.students.values()
        )
        student_menu.pack(side="left", padx=10, fill="x", expand=True)
        self.student_var.set(list(self.students.values())[0])

        # 날짜 선택
        date_frame = tk.Frame(self.root)
        date_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(date_frame, text="날짜 (YYYYMMDD):", font=("Arial", 10, "bold")).pack(side="left")
        self.date_entry = tk.Entry(date_frame, width=15)
        self.date_entry.pack(side="left", padx=10)

        # 오늘 날짜 기본값
        from datetime import datetime
        today = datetime.now().strftime("%Y%m%d")
        self.date_entry.insert(0, today)

        # 파일 선택
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(file_frame, text="📁 선택할 파일들:", font=("Arial", 10, "bold")).pack(anchor="w")

        # 파일 목록 표시
        scrollbar = tk.Scrollbar(file_frame)
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = tk.Listbox(
            file_frame,
            yscrollcommand=scrollbar.set,
            height=8,
            font=("Arial", 9)
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # 버튼 영역
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15, padx=20, fill="x")

        tk.Button(
            button_frame,
            text="📂 파일 선택",
            command=self.select_files,
            bg="#3B5998",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="🗑️ 목록 초기화",
            command=self.clear_list,
            bg="#f0f0f0",
            font=("Arial", 10),
            padx=20,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="✅ 파일 저장",
            command=self.save_files,
            bg="#2E7D32",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        ).pack(side="right", padx=5)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="저장할 파일들을 선택하세요",
            filetypes=[("이미지 파일", "*.jpg *.jpeg *.png *.gif *.webp"), ("모든 파일", "*.*")]
        )

        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)

            student_id = self.get_student_id()
            date = self.date_entry.get()

            # 파일 목록 표시 (변경될 파일명과 함께)
            for idx, file in enumerate(self.selected_files):
                original_name = os.path.basename(file)
                ext = os.path.splitext(file)[1]
                new_name = f"{student_id}_{date}_{idx + 1}{ext}"
                display = f"{original_name} → {new_name}"
                self.file_listbox.insert(tk.END, display)

    def get_student_id(self):
        selected = self.student_var.get()
        for student_id, student_name in self.students.items():
            if student_name == selected:
                return student_id
        return 'unknown'

    def clear_list(self):
        self.file_listbox.delete(0, tk.END)
        self.selected_files = []

    def save_files(self):
        if not hasattr(self, 'selected_files') or not self.selected_files:
            messagebox.showwarning("경고", "먼저 파일을 선택해주세요!")
            return

        # 입력 검증
        student_id = self.get_student_id()
        date = self.date_entry.get()

        if not date or len(date) != 8 or not date.isdigit():
            messagebox.showerror("오류", "날짜는 YYYYMMDD 형식이어야 합니다!\n예: 20260610")
            return

        # picture 폴더 확인 및 생성
        if not os.path.exists(self.picture_dir):
            os.makedirs(self.picture_dir)

        # 파일 저장
        saved_count = 0
        errors = []

        for idx, source_file in enumerate(self.selected_files):
            try:
                # 원본 파일의 확장자 유지
                ext = os.path.splitext(source_file)[1].lower()

                # 새 파일명 생성
                new_filename = f"{student_id}_{date}_{idx + 1}{ext}"
                dest_path = os.path.join(self.picture_dir, new_filename)

                # 파일 복사
                shutil.copy2(source_file, dest_path)
                saved_count += 1

            except Exception as e:
                errors.append(f"{os.path.basename(source_file)}: {str(e)}")

        # 결과 표시
        if saved_count > 0:
            message = f"✅ {saved_count}개 파일이 저장되었습니다!\n\n"
            message += f"📁 저장 위치: {self.picture_dir}\n\n"

            if saved_count > 1:
                message += f"💾 다음 단계:\n"
                message += f"1. 'update_learning_files.py' 실행\n"
                message += f"2. Git 커밋 및 푸시\n"
                message += f"3. Netlify 자동 배포 ✨"

            messagebox.showinfo("완료", message)

            # 목록 초기화
            self.clear_list()

        else:
            messagebox.showerror("오류", "파일 저장에 실패했습니다.")

        if errors:
            error_msg = "다음 파일들에서 오류가 발생했습니다:\n\n"
            error_msg += "\n".join(errors)
            messagebox.showerror("오류", error_msg)

def main():
    root = tk.Tk()
    app = 학습자료업로더(root)
    root.mainloop()

if __name__ == "__main__":
    main()
