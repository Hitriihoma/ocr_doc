# -*- coding: utf-8 -*-
"""
Created on Sat May  3 14:48:22 2025

@author: Hitriihoma (hitriihoma@gmail.com, https://github.com/Hitriihoma)
"""

import cv2
import numpy as np
import copy
from paddleocr import PaddleOCR

class OCR_doc():
    def __init__(self):
        pass
    
    def load_image(self, path):
        '''
        Load image to ndarray format

        Parameters
        ----------
        path : string
            Path to image file.

        Returns
        -------
        image : numpy.ndarray
            ndarray of image.

        '''
        # Load the image
        image = cv2.imread(path) # './examples/hw_all.jpg'
        return image
    
    def crop_image(self, image, percent=3):
        """
        Crop image from edges by <percent> percents

        Parameters
        ----------
        image : numpy.ndarray
            ndarray of image.
        percent : int, optional
            How much percents crop from each edge. The default is 3.

        Returns
        -------
        image_cropped : numpy.ndarray
            ndarray of image.

        """
        
        indent_x = int(round(image.shape[1]*percent/100, 0))
        indent_y = int(round(image.shape[0]*percent/100, 0))
        
        image_cropped = image[indent_y:image.shape[0]-indent_y, indent_x:image.shape[1]-indent_x]
        
        return image_cropped
    
    def find_cells(self, image, skiprows=0, num_col=1, key_col=None, h1=[None, None], h2=[None, None]):
        '''
        Find cells with numbers (by known column and rows)

        Parameters
        ----------
        image : numpy.ndarray
            ndarray of image.
        skiprows : integer, optional
            How many rows skip for header (not include in result). The default is 0.
        num_col : integer, optional
            Which column contains numbers. The default is 1.
        key_col : integer, optional
            Which column contains keys for values. The default is None.
        h1 : integer, optional
            Which cell contains header 1. The default is [None, None].
        h2 : integer, optional
            Which cell contains header 2. The default is [None, None].
        
        Returns
        -------
        cells : numpy.ndarray
            Array of cells coordinates.

        '''
        def visualize_cells(image, cells):
            '''
            Service functions for visualize cells on image with red rectangles

            Parameters
            ----------
            image : numpy.ndarray
                ndarray of image.
            cells : numpy.ndarray
                Array of cells coordinates.

            Returns
            -------
            None.

            '''
            # Draw cells
            for cells_row in cells:
                for cell in cells_row:
                    try:
                        (x_tl, y_tl), (x_tr, y_tr), (x_bl, y_bl), (x_br, y_br) = cell
                        cv2.line(image, (x_tl, y_tl), (x_tr, y_tr), (0, 0, 255), 2) # top edge
                        cv2.line(image, (x_bl, y_bl), (x_br, y_br), (0, 0, 255), 2) # bottom edge
                        cv2.line(image, (x_tl, y_tl), (x_bl, y_bl), (0, 0, 255), 2) # left edge
                        cv2.line(image, (x_tr, y_tr), (x_br, y_br), (0, 0, 255), 2) # right edge
                    except Exception as e:
                        print(e, 'in draw cell:', cell)
            cv2.imshow('Cells Detected', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        # Load the image
        #image = cv2.imread('./tests/examples/hw_1.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Apply Probabilistic Hough Line Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=200, maxLineGap=10)
        # Examples x1, y1, x2, y2: [[248 1245 248 5]] [[36 622 326 622]]
        # x1=x2, y1>y2; x1<x2, y1=y2
        if lines is None:
            return {'error': 'Not found suited lines on image'}
        # Find table borders: min adn max x,y
        # Maybe use collections.Counter if there are many border points
        min_x, max_x, min_y, max_y = image.shape[1], 0, image.shape[0], 0 # 923, 0, 1280, 0

        for line in lines:
            x1, y1, x2, y2 = line[0]
            if max(x1,x2) > max_x:
                max_x = max(x1,x2)
            if min(x1,x2) < min_x:
                min_x = min(x1,x2)
            if max(y1,y2) > max_y:
                max_y = max(y1,y2)
            if min(y1,y2) < min_y:
                min_y = min(y1,y2)
                
        # Extend all lines to table borders
        orientation_thjreshold = 10
        for line_index in range(len(lines)):
            line = lines[line_index]
            x1, y1, x2, y2 = line[0]
            if abs(x1 - x2) < orientation_thjreshold: # Vertical line
                if y1 > min_y:
                    lines[line_index][0][1] = min_y
                if y2 < max_y:
                    lines[line_index][0][3] = max_y
            if abs(y1 - y2) < orientation_thjreshold: # Horizontal line
                if x1 > min_x:
                    lines[line_index][0][0] = min_x
                if x2 < max_x:
                    lines[line_index][0][2] = max_x    
                    
        # Remove lines closer than threshold (choose median)
        close_threshold = 10
        lines_processed = np.array([[np.nan,np.nan,np.nan,np.nan]]) # Already processed lines
        lines_cleared = np.array([[np.nan,np.nan,np.nan,np.nan]])
        lines = np.unique(lines, axis=0)
        for line in lines:
            # If line were processed before, skip it
            if any(np.equal(line,lines_processed).all(1)):
                continue
            if np.isnan(lines_processed).all():
                lines_processed = line
            else:
                lines_processed = np.append(lines_processed, line, axis=0)
            x1, y1, x2, y2 = line[0]
            # Choose all lines where two ends are close enough
            # From all other lines that are not processed
            compare_lines = copy.copy(lines)
            compare_lines = [i for i in compare_lines if not any(np.equal(i,lines_processed).all(1))]
            lines_close = np.array([line[0]]) # Currently processed line
            for temp_line in compare_lines:
                xt1, yt1, xt2, yt2 = temp_line[0]
                if max(abs(xt1-x1), abs(yt1-y1), abs(xt2-x2), abs(yt2-y2)) <= close_threshold:
                    lines_close = np.append(lines_close, temp_line, axis=0)
                    # If temp_line is close and not in lines_processed:
                    if not any(np.equal(temp_line,lines_processed).all(1)):
                        lines_processed = np.append(lines_processed, temp_line, axis=0)
            if len(lines_close) > 1:
                # Found two or more similar lines
                x1_c = [] # Values of x1 coordinate
                y1_c = [] # Values of y1 coordinate
                x2_c = [] # Values of x2 coordinate
                y2_c = [] # Values of y2 coordinate
                for line_close in lines_close:
                    x1, y1, x2, y2 = line_close
                    x1_c.append(x1)
                    y1_c.append(y1)
                    x2_c.append(x2)
                    y2_c.append(y2)
                if np.isnan(lines_cleared).all():
                    lines_cleared = [line]
                else:
                    lines_cleared = np.append(lines_cleared, [[[np.median(x1_c), np.median(y1_c), np.median(x2_c), np.median(y2_c)]]], axis=0) # Median line
            else:
                if np.isnan(lines_cleared).all():
                    lines_cleared = [line]
                else:
                    lines_cleared = np.append(lines_cleared, [line], axis=0)
        # Lines variable is newly created lines array
        lines = copy.copy(lines_cleared).astype(int)
        
        # Make matrix, where cells filled by lines
        # y: len(image): 1280; x: len(image[0]): 923
        lines_matrix = np.zeros([len(image),len(image[0])]) # Zero matrix
        for line_index in range(len(lines)):
            line = lines[line_index]
            x1, y1, x2, y2 = line[0] # y is row index, x is element index in row
            if x1 == x2: # Вертикальная линия
                for y_index in range(y1,y2+1):
                    lines_matrix[y_index][x1] = 1 # Fill with ones
            if y1 == y2: # Горизонтальная линия
                for x_index in range(x1,x2+1):
                    lines_matrix[y1][x_index] = 1 # Fill with ones

        # Templates for corners, size 3х3
        top_right_corner_template = np.array([[1,1,1],[0,0,1],[0,0,1]])
        top_left_corner_template = np.array([[1,1,1],[1,0,0],[1,0,0]])
        bottom_right_corner_template = np.array([[0,0,1],[0,0,1],[1,1,1]])
        bottom_left_corner_template = np.array([[1,0,0],[1,0,0],[1,1,1]])
        corners_templates = {'top_right': top_right_corner_template, 
                             'top_left': top_left_corner_template, 
                             'bottom_right': bottom_right_corner_template, 
                             'bottom_left': bottom_left_corner_template}

        # Bypass matrix of lines with window 3х3
        top_right_corners = []
        top_left_corners = []
        bottom_right_corners = []
        bottom_left_corners = []
        for x, y in ((x,y) for x in range(1,len(lines_matrix[0])-1) for y in range(1,len(lines_matrix)-1)):
            # Get matrix 3х3 with center in x,y
            # In generator already made indent 1 from image borders
            # first y (row index), than x (index of element in row)
            # If lines_matrix[y-1:y+2, x-1:x+2], than empty array lines_matrix[990:100, 890:900]
            window = np.array([lines_matrix[y-1, x-1:x+2],
                                lines_matrix[y, x-1:x+2],
                                lines_matrix[y+1, x-1:x+2]])
            for name, template in corners_templates.items():
                if np.array_equal(window, template):
                    if name == 'top_right':
                        top_right_corners.append((x,y))
                    elif name == 'top_left':
                        top_left_corners.append((x,y))
                    elif name == 'bottom_right':
                        bottom_right_corners.append((x,y))
                    elif name == 'bottom_left':
                        bottom_left_corners.append((x,y))

        # Coordinates of cells. [0] row numbers (y), [1] column numbers (x), inside 4 corners coordinates
        # Calclulate amount of rows and columns
        cells_x = []
        cells_y = []
        cells_error = 10 # Presumable error in pixels
        for top_left_corner in top_left_corners:
            x_tl, y_tl = top_left_corner
            x_add = True
            y_add = True
            for cell_x in cells_x:
                if cell_x - cells_error < x_tl < cell_x + cells_error:
                    # Considering error this x_tl already in list
                    x_add = False
            for cell_y in cells_y:
                if cell_y - cells_error < y_tl < cell_y + cells_error:
                    # Considering error this y_tl already in list
                    y_add = False
            if x_add:
                cells_x.append(x_tl)
            if y_add:
                cells_y.append(y_tl)
        cells_rows = len(cells_y)    
        cells_columns = len(cells_x) 
        # Initialize matrix with rows and columns to fill
        cells = np.empty((cells_rows, cells_columns), dtype=object) # 17 строк, 3 столбца
        cells[:] = np.nan
        for tlc_index in range(len(top_left_corners)):
            # Coordinates of top left corner
            x_tl, y_tl = top_left_corners[tlc_index]
            # Coordinates of top right corner with same <y> and greater <x> as top left corner
            for top_rigth_corner in top_right_corners:
                x_tr, y_tr = top_rigth_corner
                if y_tr == y_tl and x_tr > x_tl:
                    break
            # Coordinates of bottom left corner with same <x> and greater <y> as top left corner
            for bottom_left_corner in bottom_left_corners:
                x_bl, y_bl = bottom_left_corner
                if x_bl == x_tl and y_bl > y_tl:
                    break
            # Coordinates of bottom left corner by top right and bottom left corners
            x_br, y_br = x_tr, y_bl
            # Add cell coordinates to cell matrix
            cells[tlc_index % cells_rows, tlc_index // cells_rows] = ((x_tl, y_tl), (x_tr, y_tr), (x_bl, y_bl), (x_br, y_br))
        
        # Choose cell for header 1
        if h1[0] is not None and h1[1] is not None:
            h1_cell = cells[h1[1]-1,h1[0]-1]
        else:
            h1_cell = [None,None]
        # Choose cell for header 2
        if h2[0] is not None and h2[1] is not None:
            h2_cell = cells[h2[1]-1,h2[0]-1]
        else:
            h2_cell = [None,None]
        # Skip <skiprows> rows as table header
        cells = cells[skiprows:]
        # Choose columns <num_col>
        num_cells = cells[:,num_col-1]
        # Choose column <key_col>, where id located
        if key_col:
            key_cells = cells[:,key_col-1]
        else:
            key_cells = None
            
        return {'num_cells': num_cells, 'key_cells': key_cells, 'h1_cell': h1_cell, 'h2_cell': h2_cell}
        
    def ocr_image_number(self, image):
        '''
        OCR one image with number using Paddleocr
        Paddleocr supports Chinese, English, French, German, Korean and Japanese.
        You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
        to switch the language model in order.
        English model works better for recognising numbers in my tests.
        cls: use angle classifier or not. Default is True. If true, the text with rotation of 180 degrees can be recognized. 
        If no text is rotated by 180 degrees, use cls=False to get better performance. Text with rotation of 90 or 270 degrees can be recognized even if cls=False.

        Parameters
        ----------
        image : numpy.ndarray
            ndarray of image.

        Returns
        -------
        result_dict : dictionary
            values (text) of image with recognition scores.

        '''
        def comma_to_dot(input_value):
            '''
            If value contains ',', replace it to '.' for cast to number

            Parameters
            ----------
            input_value : string
                String, which may contain , like 123,456.

            Returns
            -------
            string
                String where , replaced with .

            '''
            if ',' in input_value and type(input_value) == str:
                return input_value.replace(',', '.')
            else:
                return input_value
        
        def check_number(input_value):
            '''
            Check if string is valid number

            Parameters
            ----------
            input_value : string
                String, whick need to check whether it is number.

            Returns
            -------
            Bool
                True if string is number, False if string is not number.

            ''' 
            if input_value[0] == '-': # If a negative number
                return input_value[1:].replace('.','',1).isdigit()
            else:
              return input_value.replace('.','',1).isdigit()
        
        my_rec_char_dict_path = './ocr/permitted_chars.txt' # , rec_char_dict_path=my_rec_char_dict_path
        ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log = False, rec_char_dict_path=my_rec_char_dict_path) # need to run only once to download and load model into memory
        result = ocr.ocr(image, cls=False)
        result_dict = {}
        if result == [None]:
            result_dict.update({'value': None, 'score': None, 'is_number': False})
        elif len(result) == 1:
            line = result[0][0]
            result_value = comma_to_dot(line[1][0])
            result_dict.update({'value': result_value, 'score': round(line[1][1],4), 'is_number': check_number(result_value)})
        else:
            for idx in range(len(result)):
                line = result[idx]
                result_value = comma_to_dot(line[1][0])
                result_dict.update({idx: {'value': result_value, 'score': round(line[1][1],4), 'is_number': check_number(result_value)}})
        
        return result_dict
    
    def ocr_cell(self, image, cell, indent):
        '''
        Make ocr_image on specific cell in image

        Parameters
        ----------
        image : numpy.ndarray
            ndarray of image.
        cell : list of int
            List of cell corners coordinates.
        indent : integer
            Indent for step inside cell from corners.

        Returns
        -------
        cell_chars : dictionary
            Dictionary of {value, score}. Values (text) of image with recognition scores.

        '''
        
        min_size = 10
        (x_tl, y_tl), (x_tr, y_tr), (x_bl, y_bl), (x_br, y_br) = cell
        if (y_bl - y_tl - 2*indent > min_size) and (x_tr - x_tl - 2*indent > min_size):
            cell_image = image[y_tl+indent:y_bl-indent, x_tl+indent:x_tr-indent]
            cell_chars = self.ocr_image_number(cell_image)
            return cell_chars
        else:
            # Cell too small to ocr
            return {'value': None, 'score': 0}

    def ocr_table(self, doc, result_info='full'):
        '''
        Process OCR on table

        Parameters
        ----------
        doc : Table()
            Object of class Table with structure and ndarray of image.
        result_info : string
            Whick information return in result. 'full' or 'value'

        Returns
        -------
        table_result : dictionary
            Values (text) in cells.

        '''
        image = doc.image
        image = self.crop_image(image, percent=3)
        skiprows = doc.skiprows
        num_col = doc.num_col
        key_col = doc.key_col
        h1 = doc.h1
        h2 = doc.h2
        cells = self.find_cells(image, skiprows, num_col, key_col, h1, h2)
        if 'error' in cells.keys():
            return {'error': cells['error']}
        num_cells = cells['num_cells']
        if cells['key_cells'] is not None:
            key_cells = cells['key_cells']
        else:
            key_cells = None
        if cells['h1_cell'][0] is not None and cells['h1_cell'][1] is not None:
            h1_cell = cells['h1_cell']
        else:
            h1_cell = None
        if cells['h2_cell'][0] is not None and cells['h2_cell'][1] is not None:
            h2_cell = cells['h2_cell']
        else:
            h2_cell = None
        indent = 10
        table_result = {}
        for cell_idx in range(len(num_cells)):
            if result_info == 'full':
                cell_chars = self.ocr_cell(image, num_cells[cell_idx], indent) # {'value': value, 'score': score, 'is_number': is_number} 
            elif result_info in ['value', 'values']:
                cell_chars = self.ocr_cell(image, num_cells[cell_idx], indent)['value'] # Only value 
            else:
                raise ValueError("Argument 'result_info' must be one of 'full', 'value' or 'values'")
            # OCR id for cell
            if key_cells is not None:
                key_chars = self.ocr_cell(image, key_cells[cell_idx], indent)['value'] # Only value
            else:
                key_chars = cell_idx
            table_result.update({key_chars: cell_chars})
        if h1_cell is not None:
            h1_chars = self.ocr_cell(image, h1_cell, indent)['value'] # Only value
            table_result.update({'h1': h1_chars})
        if h2_cell is not None:
            h2_chars = self.ocr_cell(image, h2_cell, indent)['value'] # Only value
            table_result.update({'h2': h2_chars})
        table_result.update({'error': False})
        
        return table_result
    
class Table():
    def __init__(self, skiprows=None, num_col=None, key_col=None, h1=[None,None], h2=[None,None]):
        self.skiprows = skiprows
        self.num_col = num_col
        self.key_col = key_col
        self.h1 = h1
        self.h2 = h2
        
    def load_image(self, path):
        '''
        Load image to ndarray format and set <image> attribute

        Parameters
        ----------
        path : string
            Path to image file.

        Returns
        -------
        image : numpy.ndarray
            ndarray of image.

        '''
        # Load the image
        self.image = cv2.imread(path) # './examples/hw_all.jpg'
    
    def get_image(self):
        return self.image
    
    def get_base_structure(self, struct_type='full'):
        '''
        Git basic table structure

        Parameters
        ----------
        struct_type : string, optional
            Description of table structure. The default is 'full'.

        Raises
        ------
        ValueError
            If struct_type not valid.

        Returns
        -------
        Table()
            Basic table structure.

        '''
        if struct_type == 'simple':
            return Table(skiprows=0, num_col=2, key_col=None, h1=[None, None], h2=[None, None])
        elif struct_type == 'full':
            return Table(skiprows=2, num_col=3, key_col=1, h1=[2, 1], h2=[2, 2])
        else:
            raise ValueError("Base structure type must be 'simple' or 'full'")
