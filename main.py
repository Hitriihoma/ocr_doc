# -*- coding: utf-8 -*-
"""
Created on Sat May  3 15:08:35 2025

@author: Hitriihoma (hitriihoma@gmail.com, https://github.com/Hitriihoma)
"""

from ocr.ocr_module import OCR_doc

def main(insert_image, skiprows, column):
    HOCR = OCR_doc()
    image = HOCR.load_image(insert_image)
    table = HOCR.ocr_table(image, skiprows, column)
    
    return table
    
if __name__ == "__main__":
    insert_image = input('Insert path to image: ') # './tests/examples/hw_1.jpg'
    skiprows = int(input('How many rows to skip: ')) # 0
    column = int(input('Which column contains numbers, start with 1: ')) # 2
    table = main(insert_image, skiprows, column)
    print(table)