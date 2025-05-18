# -*- coding: utf-8 -*-
"""
Created on Thu May 15 22:10:17 2025

@author: Hitriihoma (hitriihoma@gmail.com, https://github.com/Hitriihoma)
"""

import requests

response_structure_1_base = requests.post(
    url="http://localhost:8000/ocr",
    json={"img_path": "./tests/examples/structure_1.jpg"}
          )
print('Full structure, just img_path')
print('Staus code', response_structure_1_base.status_code)
print(response_structure_1_base.json())  
# Output:
# {'1': {'value': '123.456', 'score': 0.9969, 'is_number': True}
# , '2': {'value': '123.456', 'score': 0.9997, 'is_number': True}
# , '3': {'value': '0.01', 'score': 0.9996, 'is_number': True}
# , '4': {'value': '0.01', 'score': 0.9997, 'is_number': True}
# , '5': {'value': '3456789012', 'score': 0.9996, 'is_number': True}
# , '6': {'value': '4567890123', 'score': 0.9993, 'is_number': True}
# , '7': {'value': '5678901234', 'score': 0.9993, 'is_number': True}
# , '8': {'value': '6789012345', 'score': 0.9992, 'is_number': True}
# , '9': {'value': '7890123456', 'score': 0.999, 'is_number': True}
# , '10': {'value': '8901234567', 'score': 0.9991, 'is_number': True}
# , 'h1': '1234567890', 'h2': '2345678901'}

response_structure_1 = requests.post(
    url="http://localhost:8000/ocr",
    json={"img_path": "./tests/examples/structure_1.jpg"
          , "structure": {"skiprows": 2
                          , "num_col": 3
                          , "key_col": 1
                          , "h1": [2,1]
                          , "h2": [2,2]
                          }
         , "result_info": "values"
          })
print('Full structure with all arguments')
print('Staus code', response_structure_1.status_code)
print(response_structure_1.json())  
# Output:
# {'1': '123.456', '2': '123.456', '3': '0.01', '4': '0.01', '5': '3456789012', '6': '4567890123', '7': '5678901234', '8': '6789012345', '9': '7890123456', '10': '8901234567', 'h1': '1234567890', 'h2': '2345678901'}

response_hw_1 = requests.post(
    url="http://localhost:8000/ocr",
    json={"img_path": "./tests/examples/hw_1.jpg"
          , "structure": {"skiprows": 0
                          , "num_col": 2
                          , "key_col": None
                          , "h1": [None,None]
                          , "h2": [None,None]
                          }
          , "result_info": "values"
          })
print('Simple structure with a;; arguments, handwritten text')
print('Staus code', response_hw_1.status_code)
print(response_hw_1.json())  
# Output: 
# {0: '1234567890', 1: '3456789012', 2: '123.456', 3: '123.456', 4: '0.01', 5: '0.01', 6: '1234567890', 7: '1234567890', 8: '1234567890', 9: '1234567890'}

