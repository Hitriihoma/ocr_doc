# -*- coding: utf-8 -*-
"""
Created on Thu May 15 22:10:17 2025

@author: Hitriihoma (hitriihoma@gmail.com, https://github.com/Hitriihoma)
"""

import requests
import time

time_start = time.perf_counter()
test_filename = 'structure_2_1_1.jpg'
test_response = requests.post(
    url="http://localhost:8000/ocr",
    json={"img_path": f"./tests/examples/{test_filename}"
          , "structure": {"skiprows": 3, "num_col": 3, "key_col": 1, "h1": [1,1], "h2": [1,2]}
          , 'result_info': 'value'
          }
          )
print(f'{test_filename}')
print('Status code:', test_response.status_code)
print(f"Execution time: {(time.perf_counter() - time_start)} seconds")
print(test_response.json())  

import json
import re
with open("./results/{}.json".format(re.search(r'\D+_\d+', test_filename)[0]), 'w') as f:
    json.dump(test_response.json(), f, ensure_ascii=False)

# structure
# hw_1: "structure": {"skiprows": 0, "num_col": 2, "key_col": None, "h1": [None,None], "h2": [None,None], 'result_info': 'value'}
# structure_1: "structure": {"skiprows": 2, "num_col": 3, "key_col": 1, "h1": [2,1], "h2": [2,2]}, 'result_info': 'value'
# structure_2: "structure": {"skiprows": 2, "num_col": 3, "key_col": 1, "h1": [1,1], "h2": [1,2]}, 'result_info': 'value'
# structure_3: "structure": {"skiprows": 3, "num_col": 3, "key_col": 1, "h1": [1,1], "h2": [1,2]}, 'result_info': 'value'
