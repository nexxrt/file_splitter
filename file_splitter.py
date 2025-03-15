import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Splitter")
        self.root.geometry("550x450")
        self.root.configure(bg="#f0f0f0")

        # Переменные
        self.file_path = tk.StringVar()
        self.parts_count = tk.IntVar(value=2)
        self.status = tk.StringVar(value="Ready to work")

        # Основной фрейм
        main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(expand=True)

        # Заголовок
        tk.Label(
            main_frame, 
            text="File Splitter",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        ).pack(pady=(0, 20))

        # Фрейм для выбора файла
        file_frame = tk.LabelFrame(
            main_frame,
            text="Select File",
            bg="#ffffff",
            padx=10,
            pady=10,
            fg="#666666"
        )
        file_frame.pack(fill="x", pady=5)

        tk.Entry(
            file_frame,
            textvariable=self.file_path,
            width=35,
            bg="#f9f9f9",
            state='readonly',
            relief="flat"
        ).pack(side="left", padx=5)
        
        tk.Button(
            file_frame,
            text="Select",
            command=self.select_file,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            activebackground="#45a049",
            cursor="hand2"
        ).pack(side="right")

        # Фрейм для количества частей
        parts_frame = tk.LabelFrame(
            main_frame,
            text="Settings",
            bg="#ffffff",
            padx=10,
            pady=10,
            fg="#666666"
        )
        parts_frame.pack(fill="x", pady=5)

        tk.Label(
            parts_frame,
            text="Parts:",
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=5)
        
        tk.Spinbox(
            parts_frame,
            from_=2,
            to=100,
            textvariable=self.parts_count,
            width=10,
            relief="flat",
            bg="#f9f9f9"
        ).pack()

        # Кнопка разделения
        tk.Button(
            main_frame,
            text="Split file",
            command=self.split_file,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            activebackground="#1e88e5",
            cursor="hand2"
        ).pack(pady=20)

        # Статус
        tk.Label(
            main_frame,
            textvariable=self.status,
            bg="#f0f0f0",
            fg="#666666",
            font=("Arial", 9, "italic")
        ).pack()

    def select_file(self):
        """Функция выбора файла"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.file_path.set(file_path)
            self.status.set(f"Selected File: {os.path.basename(file_path)}")

    def split_file(self):
        """Функция разделения файла с учетом строк"""
        if not self.file_path.get():
            messagebox.showerror("Error", "Please, select file")
            return

        self.status.set("Working....")
        self.root.update()

        try:
            input_file = self.file_path.get()
            parts = self.parts_count.get()
            file_size = os.path.getsize(input_file)
            part_size = file_size // parts
            
            if part_size < 1:
                messagebox.showerror("Error", "The file is too small for splitting!")
                self.status.set("Ready to work")
                return

            file_name, file_ext = os.path.splitext(os.path.basename(input_file))
            output_dir = os.path.join(os.path.dirname(input_file), file_name)
            os.makedirs(output_dir, exist_ok=True)

            # Читаем файл как текст
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                total_length = len(content)
                ideal_part_size = total_length // parts
                split_points = []

                # Находим точки разделения с учетом переносов строк
                current_pos = 0
                for i in range(parts - 1):
                    target_pos = ideal_part_size * (i + 1)
                    # Ищем ближайший перенос строки после целевой позиции
                    while target_pos < total_length and content[target_pos] != '\n':
                        target_pos += 1
                    if target_pos >= total_length:
                        target_pos = total_length - 1
                    split_points.append(target_pos)
                    current_pos = target_pos + 1

                # Разделяем содержимое
                start_pos = 0
                for i, end_pos in enumerate(split_points + [total_length]):
                    part_content = content[start_pos:end_pos].strip()
                    if part_content:  # Пишем только непустые части
                        output_file = os.path.join(output_dir, f"{file_name}_part{i+1}{file_ext}")
                        with open(output_file, 'w', encoding='utf-8') as out:
                            out.write(part_content)
                    start_pos = end_pos + 1

            messagebox.showinfo("Success", f"The file has been successfully split into {parts} parts!\nThe result is in the folder: {output_dir}")
            self.status.set("Ready to work")

        except Exception as e:
            messagebox.showerror("Error", f"There's been a mistake: {str(e)}")
            self.status.set("Ready to work")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSplitterApp(root)
    root.mainloop()