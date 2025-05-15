# -*- coding: utf-8 -*-
"""
Created on Thu May 15 22:10:17 2025

@author: Hitriihoma (hitriihoma@gmail.com, https://github.com/Hitriihoma)
"""

import requests


response_hw_1 = requests.post(
    url="http://localhost:8000/ocr",
    json={"img_path": "./tests/examples/hw_1.jpg"
          , "structure": {"skiprows": 0
                          , "num_col": 2
                          , "key_col": None
                          , "h1": [None,None]
                          , "h2": [None,None]
                          }
          })

print(response_hw_1.json())  
# Output: 
# {0: '1234567890', 1: '3456789012', 2: '123.456', 3: '123.456', 4: '0.01', 5: '0.01', 6: '1234567890', 7: '1234567890', 8: '1234567890', 9: '1234567890'}

response_structure_1 = requests.post(
    url="http://localhost:8000/ocr",
    json={"img_path": "./tests/examples/structure_1.jpg"
          , "structure": {"skiprows": 2
                          , "num_col": 3
                          , "key_col": 1
                          , "h1": [2,1]
                          , "h2": [2,2]
                          }
          })
print(response_structure_1.json())  
# Output:
# {'1': '123.456', '2': '123.456', '3': '0.01', '4': '0.01', '5': '3456789012', '6': '4567890123', '7': '5678901234', '8': '6789012345', '9': '7890123456', '10': '8901234567', 'h1': '1234567890', 'h2': '2345678901'}
