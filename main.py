# -*- coding: utf-8 -*-
"""
Created on Sat May  3 15:08:35 2025

@author: Hitriihoma (hitriihoma@gmail.com, https://github.com/Hitriihoma)
"""

from ocr.ocr_module import OCR_doc, Table
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

class OcrInput(BaseModel):
    img_path: str
    structure: Optional[dict] = None
    result_info: Optional[str] = 'full'

@app.post("/ocr")
async def ocr_doc(insert_json: OcrInput):
    insert_image = insert_json.img_path
    # Check if there is optional field:structure in insert_json
    if insert_json.structure is not None:
        doc = Table(skiprows=insert_json.structure['skiprows']
                    , num_col=insert_json.structure['num_col']
                    , key_col=insert_json.structure['key_col']
                    , h1=insert_json.structure['h1']
                    , h2=insert_json.structure['h2'])
    else:
        # Base structure
        doc = Table().get_base_structure(struct_type='full')     
    doc.load_image(insert_image)
    ocr = OCR_doc()
    table = ocr.ocr_table(doc=doc, result_info=insert_json.result_info)
    
    return jsonable_encoder(table)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

