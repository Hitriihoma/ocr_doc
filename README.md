**HOCR**  
Apply OCR (Optical Character Recognition) for prited table with handwritten text
Применение OCR (Оптичепское Символьное распознавание) для распечатанной таблицы с рукописным текстом

# Intro


# Structure

main.py
ocr/ocr_app.py - class for OCR app, can get image and return formatted result
ocr/ocr_functions/load_image - load image to opencv (cv2) variable
ocr/ocr_functions/find_cells - find cell coordinates in table
ocr/ocr_functions/ocr_image - process OCR on image
ocr/ocr_functions/ocr_table - process pipeline of find_cells and ocr_image for table and return formatted table

# Планирование

- [x] Тестовые данные
- [x] Скользящее среднее левое
- [ ] Скользящее среднее с обработкой выбросов (IQR / дисперсия / обрезание )
- [ ] Двойное экспоненциальное сглаживание
- [ ] Скользящее двойное экспоненциальное сглаживание

# Использование

1. Создание объекта-сглаживателя определённого типа
2. Получение сглаженной выборки как результат вызова функции объект.обработка() с передачей выборки данных в качестве аргумента