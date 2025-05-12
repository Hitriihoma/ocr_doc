# -*- coding: utf-8 -*-
"""
Created on Sat May  3 15:08:35 2025

@author: Hitriihoma (hitriihoma@gmail.com, https://github.com/Hitriihoma)
"""

from ocr.ocr_module import OCR_doc, Table

def main(doc, insert_image):
    doc.load_image(insert_image)
    HOCR = OCR_doc()
    table = HOCR.ocr_table(doc)
    
    return table
    
if __name__ == "__main__":
    '''
    Examples 
    hw_1: 
        doc = Table(skiprows=0, num_col=2, key_col=None, h1=[None,None]
        insert_image = './tests/examples/hw_1.jpg'
    structure_1:
        doc = Table(skiprows=2, num_col=3, key_col=1, h1=[2,1], h2=[2,2])
        insert_image = './tests/examples/structure_1.jpg'
    '''
    doc = Table(skiprows=0, num_col=2, key_col=None, h1=[None,None], h2=[None,None])
    insert_image = input('Insert path to image: ') # './tests/examples/hw_1.jpg'
    ocr_table = main(doc, insert_image)
    print(ocr_table)