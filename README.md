**OCR_doc**  

# About The Project

Apply OCR (Optical Character Recognition) for printed table with handwritten text  
Применение OCR (Оптическое Символьное распознавание) для распечатанной таблицы с рукописным текстом

# Installation

Use [poetry](https://python-poetry.org/docs/) package manager with project `pyproject.toml` file

# Usage

## Run server

In command console, change directory to project, than run command
```bash
uvicorn main:app --reload
```

To kill server, use process manager

## Structure

main.py  
ocr/ocr_module.py - class for OCR module, can get image and return formatted result  
ocr/ocr_module/OCR().load_image() ot ocr/ocr_module Table().load_image() - load image to opencv (cv2) variable  
ocr/ocr_module/OCR().find_cells() - find cell coordinates in table  
ocr/ocr_module/OCR().ocr_image_number() - process OCR on image with number 
ocr/ocr_module/OCR().ocr_cell() - process OCR image for cell in image  
ocr/ocr_module/OCR().ocr_table() - process pipeline of find_cells and ocr_image for table and return formatted table  
ocr/tests/post.py - example post requests to server

# Contact

Hitriihoma - hitriihoma@gmail.com
Project Link: [https://github.com/Hitriihoma/ocr_doc](https://github.com/Hitriihoma/ocr_doc)