import os
import pytesseract
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
from tkinter import Tk, filedialog, messagebox, Text, Button, Checkbutton, BooleanVar, Menu, Frame
import json
import csv
import webbrowser
import threading
import datetime



class TextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF & Image to Text Converter")

        # Menu bar setup
        self.menu_bar = Menu(root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.select_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Text box to display extracted text
        self.display_text = Text(root, wrap="word", height=20, width=60)
        self.display_text.pack(pady=10)

        # File format selection with checkboxes (horizontal layout)
        format_frame = Frame(root)
        format_frame.pack(pady=10)

        self.save_as_txt = BooleanVar()
        self.save_as_json = BooleanVar()
        self.save_as_csv = BooleanVar()

        self.txt_checkbox = Checkbutton(format_frame, text="Save as .txt", variable=self.save_as_txt)
        self.json_checkbox = Checkbutton(format_frame, text="Save as .json", variable=self.save_as_json)
        self.csv_checkbox = Checkbutton(format_frame, text="Save as .csv", variable=self.save_as_csv)

        # Pack checkboxes horizontally
        self.txt_checkbox.pack(side="left", padx=5)
        self.json_checkbox.pack(side="left", padx=5)
        self.csv_checkbox.pack(side="left", padx=5)

        # File selection button
        self.file_button = Button(root, text="Select Image/PDF", command=self.select_file)
        self.file_button.pack(pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image or PDF",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg"), ("PDF files", "*.pdf")]
        )
        if file_path:
            # Use threading to avoid GUI freezing during processing
            threading.Thread(target=self.process_file, args=(file_path,)).start()
        else:
            messagebox.showerror("File Error", "No file selected")

    def process_file(self, file_path):
        try:
            if file_path.endswith(".pdf"):
                extracted_text = self.extract_text_from_pdf(file_path)
            else:
                extracted_text = self.extract_text_from_image(file_path)

            self.display_text.delete(1.0, "end")
            self.display_text.insert("end", extracted_text)

            # Save in the selected formats
            self.save_output(extracted_text, os.path.basename(file_path))

        except pytesseract.pytesseract.TesseractError:
            self.show_tesseract_error()

    def preprocess_image(self, image):
        image = image.convert('L')  # Convert to grayscale
        image = ImageEnhance.Contrast(image).enhance(3)  # Increase contrast
        image = ImageEnhance.Sharpness(image).enhance(3)  # Sharpen image
        return image

    def extract_text_from_image(self, image_path):
        image = Image.open(image_path)
        processed_image = self.preprocess_image(image)
        return pytesseract.image_to_string(processed_image)

    def extract_text_from_pdf(self, pdf_path):
        images = convert_from_path(pdf_path, dpi=300)
        all_text = ''
        for page_num, image in enumerate(images):
            processed_image = self.preprocess_image(image)
            text = pytesseract.image_to_string(processed_image)
            all_text += f"--- Page {page_num + 1} ---\n{text}\n"
        return all_text

    def save_output(self, output_text, file_name):
        output_folder = f'output_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
        os.makedirs(output_folder, exist_ok=True)

        # Save as plain text
        if self.save_as_txt.get():
            text_file_path = os.path.join(output_folder, f'{file_name}.txt')
            with open(text_file_path, 'w', encoding='utf-8') as file:
                file.write(output_text)

        # Save as JSON
        if self.save_as_json.get():
            json_file_path = os.path.join(output_folder, f'{file_name}.json')
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump({"content": output_text}, json_file, indent=4)

        # Save as CSV
        if self.save_as_csv.get():
            csv_file_path = os.path.join(output_folder, f'{file_name}.csv')
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Text'])
                for line in output_text.splitlines():
                    writer.writerow([line])

        messagebox.showinfo("Save Complete", f"Text saved in selected formats in {output_folder}")

    def show_about(self):
        messagebox.showinfo("About", "PDF & Image to Text Converter v1.0\nCreated by Tom Gair")

    def show_tesseract_error(self):
        # Display error message with a prompt to check the README
        response = messagebox.askquestion(
            "Tesseract Not Found",
            "Tesseract OCR was not found. Please ensure it's installed and accessible.\n\n"
            "Would you like to view the Tesseract installation instructions in the README?"
        )
        if response == 'yes':
            self.open_readme()

    def open_readme(self):
        # Automatically open the README file (local or GitHub link)
        readme_path = os.path.join(os.getcwd(), "README.md")  # Adjust if necessary
        if os.path.exists(readme_path):
            webbrowser.open_new_tab(readme_path)
        else:
            webbrowser.open_new_tab('https://github.com/TomGirr/todolist#tesseract-ocr')  # Example GitHub README link


def main():
    root = Tk()
    app = TextExtractorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
