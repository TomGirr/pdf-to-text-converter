## PDF & Image to Text Converter

This application allows you to extract text from images and PDFs using Tesseract OCR.

### Prerequisites
- Python 3.x

- Tesseract OCR (See installation instructions below)

### Installation Instructions

#### Installing Tesseract OCR

This project uses Tesseract OCR to convert images or PDFs into text. Follow the steps below to

install Tesseract:

### For Windows:
1. Download the Tesseract installer from the official repository:
[Tesseract OCR Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install Tesseract.
3. Add the path to ‘tesseract.exe’ to your system's environment variables, or set the

* TESSERACT_PATH’ environment variable.

### For macOS:

You can install Tesseract using Homebrew:
```
brew install tesseract
```

### For Linux:
Tesseract can be installed using the package manager:
	```bash
	sudo apt-get install tesseract-ocr
	```

### Setting the Tesseract Path
You can set the path to Tesseract on your machine by adding it to your system's environment variables.

### Running the Application

1. Clone the repository or download the source code.
2. Install the required Python packages with the following command:

```bash
pip install -r requirements. txt
```
3. Run the program:
```bash
python main.py
```

4. Select an image or PDF, and the extracted text will appear. You can save the output as a 
* .txt’,
* .json, or 
* .csv’ file.

### Troubleshooting
If Tesseract OCR is not found, ensure that it is installed and that the path to ‘tesseract.exe’ is added

to the system's ~PATH’ or *TESSERACT_PATH’ environment variable.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.


