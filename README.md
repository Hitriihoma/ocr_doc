**OCR_doc**  
Apply OCR (Optical Character Recognition) for prited table with handwritten text  
Применение OCR (Оптичепское Символьное распознавание) для распечатанной таблицы с рукописным текстом

# Intro


# Structure

main.py  
ocr/ocr_module.py - class for OCR module, can get image and return formatted result  
ocr/ocr_module/load_image - load image to opencv (cv2) variable  
ocr/ocr_module/find_cells - find cell coordinates in table  
ocr/ocr_module/ocr_image - process OCR on image  
ocr/ocr_module/ocr_cell - process OCR image for cell in image  
ocr/ocr_module/ocr_table - process pipeline of find_cells and ocr_image for table and return formatted table  

# Run server

Change directory to project
```bash
uvicorn main:app --reload
```
