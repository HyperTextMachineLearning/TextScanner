# TextScanner
Handy Light-Weight Desktop Application to scan text from image while being offline

![Working](media/working.gif)

## Setup

>Note: Currently this only works on Windows; support for others will others added later

- Clone the repo
- Create Virtual Environment (Optional but **strongly** recommended)
    - Create it using `venv` module:
        ```
        python -m venv .venv
        ```
    - After creating, activate using (enter following in CMD):
        ```
        .venv\scripts\activate
        ```
- Install the dependencies using:

    ```
    pip install -r requirements.txt
    ```

- Now install Tesseract on your system from [here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe). 
Install with default options (side note: currently only English is supported.)

- Go to `logic.py` and on line `12` set `pytesseract.pytesseract.tesseract_cmd` to the path where your `tesseract.exe` is
If you installed using default settings then set it to `'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'`
- Now with the virtual environment activated run the following to run the app:

    ```
    python app.py
    ```

## Issues 

- Other Languages, extraordinary fonts are currently not supported.
- A LOT of code restructuring, refactoring is needed.
- Except the core functionality of extracting the text, some functionalities might not work
