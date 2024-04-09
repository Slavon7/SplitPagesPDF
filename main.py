import tkinter as tk
from tkinter import filedialog, messagebox, IntVar
import os
import PyPDF2
import customtkinter as ctk

language_dict = {
    "select_pdf_files": "Select PDF Files",
    "select_output_directory": "Select Output Directory",
    "add_pdf_files": "Add PDF Files",
    "error": "Error",
    "success": "Success",
    "pdf_processing_complete": "PDF processing complete.",
    "input_pdf": "Input PDF:",
    "browse": "Browse",
    "output_directory": "Result Directory:",
    "delete_blank_pages": "Delete Blank Pages",
    "begin": "Begin"
}

def is_blank(page):
    content = page.extractText().strip()
    return not content

def split_and_merge_pdf(input_pdf_path, output_pdf_path, delete_blank_pages):
    with open(input_pdf_path, 'rb') as input_file:
        reader = PyPDF2.PdfFileReader(input_file)
        writer = PyPDF2.PdfFileWriter()

        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            media_box = page.mediaBox
            mid_y = media_box.getUpperRight_y() / 2
            mid_x = media_box.getUpperRight_x() / 2

            top_left = PyPDF2.PageObject.createBlankPage(width=mid_x, height=mid_y)
            top_left.mergeTranslatedPage(page, 0, 0)

            top_right = PyPDF2.PageObject.createBlankPage(width=mid_x, height=mid_y)
            top_right.mergeTranslatedPage(page, -mid_x, 0)

            bottom_left = PyPDF2.PageObject.createBlankPage(width=mid_x, height=mid_y)
            bottom_left.mergeTranslatedPage(page, 0, -mid_y)

            bottom_right = PyPDF2.PageObject.createBlankPage(width=mid_x, height=mid_y)
            bottom_right.mergeTranslatedPage(page, -mid_x, -mid_y)

            # Check for blank pages if delete_blank_pages is True
            if delete_blank_pages:
                # Check if any of the four resulting pages are blank
                blank_pages = [is_blank(top_left), is_blank(top_right), is_blank(bottom_left), is_blank(bottom_right)]
                if not all(blank_pages):  # If any of the pages is not blank, add them to the output
                    writer.addPage(top_left)
                    writer.addPage(top_right)
                    writer.addPage(bottom_left)
                    writer.addPage(bottom_right)
            else:
                writer.addPage(top_left)
                writer.addPage(top_right)
                writer.addPage(bottom_left)
                writer.addPage(bottom_right)

        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

def select_input_files():
    try:
        input_file_paths = filedialog.askopenfilenames(title=language_dict["select_pdf_files"])
        input_files_string = "\n".join(input_file_paths)
        app.input_entry.delete(0, tk.END)
        app.input_entry.insert(0, input_files_string)
    except Exception as e:
        messagebox.showerror(language_dict["error"], str(e))

def select_output_directory():
    try:
        output_directory = filedialog.askdirectory(title=language_dict["select_output_directory"])
        app.output_entry.delete(0, tk.END)
        app.output_entry.insert(0, output_directory)
    except Exception as e:
        messagebox.showerror(language_dict["error"], str(e))

def process_pdf():
    try:
        input_pdf_paths = app.input_entry.get().split("\n")
        output_directory = app.output_entry.get()

        for input_pdf_path in input_pdf_paths:
            output_pdf_path = os.path.join(output_directory, os.path.basename(input_pdf_path)[:-4] + "_output.pdf")
            delete_blank_pages = app.delete_blank_pages_var.get()
            split_and_merge_pdf(input_pdf_path, output_pdf_path, delete_blank_pages)

        messagebox.showinfo(language_dict["success"], language_dict["pdf_processing_complete"])
    except Exception as e:
        messagebox.showerror(language_dict["error"], str(e))

def add_files():
    try:
        additional_files = filedialog.askopenfilenames(title=language_dict["add_pdf_files"])
        current_files = app.input_entry.get().split("\n")
        all_files = list(current_files) + list(additional_files)
        input_files_string = "\n".join(all_files)
        app.input_entry.delete(0, tk.END)
        app.input_entry.insert(0, input_files_string)
    except Exception as e:
        messagebox.showerror(language_dict["error"], str(e))

def change_language(selected_language):
    global language_dict
    if selected_language == "English":
        language_dict = {
            "select_pdf_files": "Select PDF Files",
            "select_output_directory": "Select Output Directory",
            "add_pdf_files": "Add PDF Files",
            "error": "Error",
            "success": "Success",
            "pdf_processing_complete": "PDF processing complete.",
            "input_pdf": "Input PDF:",
            "browse": "Browse",
            "output_directory": "Result Directory:",
            "delete_blank_pages": "Delete Blank Pages",
            "begin": "Begin"
        }
    elif selected_language == "Українська":
        language_dict = {
            "select_pdf_files": "Оберіть PDF файли",
            "select_output_directory": "Оберіть теку для збереження результату",
            "add_pdf_files": "Додати PDF файли",
            "error": "Помилка",
            "success": "Успіх",
            "pdf_processing_complete": "Обробка PDF завершена.",
            "input_pdf": "Вхідні PDF файли:",
            "browse": "Обрати",
            "output_directory": "Тека результату:",
            "delete_blank_pages": "Видалити порожні сторінки",
            "begin": "Виконати"
        }
    elif selected_language == "Русский":
        language_dict = {
            "select_pdf_files": "Выберите файлы PDF",
            "select_output_directory": "Выберите каталог для сохранения",
            "add_pdf_files": "Добавить файлы PDF",
            "error": "Ошибка",
            "success": "Успех",
            "pdf_processing_complete": "Обработка PDF завершена.",
            "input_pdf": "Входные PDF файлы:",
            "browse": "Выбрать",
            "output_directory": "Каталог результатов:",
            "delete_blank_pages": "Удалить пустые страницы",
            "begin": "Начать"
        }
    elif selected_language == "Қазақ":
        language_dict = {
            "select_pdf_files": "PDF файлдарды таңдаңыз",
            "select_output_directory": "Сақтау үшін каталогты таңдаңыз",
            "add_pdf_files": "PDF файлдарын қосыңыз",
            "error": "Қате",
            "success": "Сәттілік",
            "pdf_processing_complete": "PDF файлдарының өңдеуі аяқталды.",
            "input_pdf": "Кіру PDF файлдары:",
            "browse": "Көру",
            "output_directory": "Нәтиже каталогы:",
            "delete_blank_pages": "Бос беттерді жою",
            "begin": "Бастау"
        }
    update_language()

def update_language():
    input_label.configure(text=language_dict["input_pdf"])
    output_label.configure(text=language_dict["output_directory"])
    input_button.configure(text=language_dict["browse"])
    output_button.configure(text=language_dict["browse"])
    delete_blank_pages_checkbox.configure(text=language_dict["delete_blank_pages"])
    process_button.configure(text=language_dict["begin"])

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("660x260")
        self.title("PDF Split")

        # Language Selection
        languages = ["English", "Қазақ", "Українська", "Русский"]
        selected_language = tk.StringVar(value=languages[0])

        language_menu = ctk.CTkOptionMenu(self, values=languages, command=change_language, variable=selected_language)
        language_menu.grid(row=0, column=0, padx=10, pady=10)

        # Input PDF Selection
        global input_label, input_button, add_files_button
        input_label = ctk.CTkLabel(self, text="Input PDF:")
        input_label.grid(row=1, column=0, padx=10, pady=10)
        self.input_entry = ctk.CTkEntry(self, width=300)
        self.input_entry.grid(row=1, column=1, padx=10, pady=10)
        input_button = ctk.CTkButton(self, text="Browse", command=select_input_files, fg_color="#2F44C2", width=100)
        input_button.grid(row=1, column=2, padx=10, pady=10)

        # Add Files Button
        add_files_button = ctk.CTkButton(self, text="+", command=add_files, fg_color="#2F44C2", width=30)
        add_files_button.grid(row=1, column=3, padx=10, pady=10)

        # Output Directory Selection
        global output_label, output_button
        output_label = ctk.CTkLabel(self, text="Result Directory:", compound="left")
        output_label.grid(row=2, column=0, padx=10, pady=10)
        self.output_entry = ctk.CTkEntry(self, width=300)
        self.output_entry.grid(row=2, column=1, padx=10, pady=10)
        output_button = ctk.CTkButton(self, text="Browse", command=select_output_directory, fg_color="#2F44C2", width=100)
        output_button.grid(row=2, column=2, padx=10, pady=10)

        # CheckBox for Deleting Blank Pages
        global delete_blank_pages_checkbox
        self.delete_blank_pages_var = IntVar(value=1)
        delete_blank_pages_checkbox = ctk.CTkCheckBox(self, text="Delete Blank Pages", variable=self.delete_blank_pages_var)
        delete_blank_pages_checkbox.grid(row=3, column=1, padx=10, pady=10)

        # Process PDF Button
        global process_button
        process_button = ctk.CTkButton(self, text="Begin", command=process_pdf, fg_color="#2F44C2")
        process_button.grid(row=4, column=1, padx=10, pady=10)

app = App()
app.mainloop()