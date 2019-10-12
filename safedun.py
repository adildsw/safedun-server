# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 00:24:26 2019

@author: AdilDSW
"""

import os
import sys
import cv2
import numpy

class safedun:
    def __init__(self):
        
        return
    
    def sanityCheck(self, mode, key, path, threshold):
        
        return True
    
    def encode(self, path, key, threshold):
        img = cv2.imread(path)
        encoded_img_b = numpy.copy(img[:, :, 0])
        encoded_img_g = numpy.copy(img[:, :, 1])
        encoded_img_r = numpy.copy(img[:, :, 2])
        height, width, channel = img.shape
        
        encoded_img = numpy.zeros((height, width, channel))
        
        key_length = len(key)
        
        
        for i in range(threshold):
            key_idx = 0
            shift_direction = 0
            
            for row in range(height):
                for ch in range(channel):
                    roll_unit = ord(key[key_idx]) if shift_direction%2 == 1 else ((-1) * ord(key[key_idx]))
                    key_idx = (key_idx + 1)%key_length
                    shift_direction += 1
                    if ch == 0:
                        encoded_img_b[row] = numpy.roll(encoded_img_b[row], roll_unit)
                    elif ch == 1:
                        encoded_img_g[row] = numpy.roll(encoded_img_g[row], roll_unit)
                    else:
                        encoded_img_r[row] = numpy.roll(encoded_img_r[row], roll_unit)
            
            key_idx = 0
            shift_direction = 0
            
            for column in range(width):
                for ch in range(channel):
                    roll_unit = ord(key[key_idx]) if shift_direction%2 == 1 else ((-1) * ord(key[key_idx]))
                    key_idx = (key_idx + 1)%key_length
                    shift_direction += 1
                    if ch == 0:
                        encoded_img_b[:, column] = numpy.roll(encoded_img_b[:, column], roll_unit)
                    elif ch == 1:
                        encoded_img_g[:, column] = numpy.roll(encoded_img_g[:, column], roll_unit)
                    else:
                        encoded_img_r[:, column] = numpy.roll(encoded_img_r[:, column], roll_unit)
        
        encoded_img[..., 0] = encoded_img_b
        encoded_img[..., 1] = encoded_img_g
        encoded_img[..., 2] = encoded_img_r
        
        if not path.find('.decoded.png') == -1:
            save_file = path.replace('.decoded.png', '.encoded.png')
        else:
            save_file = os.path.splitext(path)[0] + '.encoded.png'
            
        cv2.imwrite(save_file, encoded_img)
        
        return
    
    def decode(self, path, key, threshold):
        img = cv2.imread(path)
        encoded_img_b = numpy.copy(img[:, :, 0])
        encoded_img_g = numpy.copy(img[:, :, 1])
        encoded_img_r = numpy.copy(img[:, :, 2])
        height, width, channel = img.shape
        
        encoded_img = numpy.zeros((height, width, channel))
        
        key_length = len(key)
        
        for i in range(threshold):
            key_idx = 0
            shift_direction = 0
            
            for column in range(width):
                for ch in range(channel):
                    roll_unit = ord(key[key_idx]) if shift_direction%2 == 0 else ((-1) * ord(key[key_idx]))
                    key_idx = (key_idx + 1)%key_length
                    shift_direction += 1
                    if ch == 0:
                        encoded_img_b[:, column] = numpy.roll(encoded_img_b[:, column], roll_unit)
                    elif ch == 1:
                        encoded_img_g[:, column] = numpy.roll(encoded_img_g[:, column], roll_unit)
                    else:
                        encoded_img_r[:, column] = numpy.roll(encoded_img_r[:, column], roll_unit)
              
            key_idx = 0
            shift_direction = 0
            
            for row in range(height):          
                for ch in range(channel):
                    roll_unit = ord(key[key_idx]) if shift_direction%2 == 0 else ((-1) * ord(key[key_idx]))
                    key_idx = (key_idx + 1)%key_length
                    shift_direction += 1
                    if ch == 0:
                        encoded_img_b[row] = numpy.roll(encoded_img_b[row], roll_unit)
                    elif ch == 1:
                        encoded_img_g[row] = numpy.roll(encoded_img_g[row], roll_unit)
                    else:
                        encoded_img_r[row] = numpy.roll(encoded_img_r[row], roll_unit)
            
        
        encoded_img[..., 0] = encoded_img_b
        encoded_img[..., 1] = encoded_img_g
        encoded_img[..., 2] = encoded_img_r
        
        if not path.find('.encoded.png') == -1:
            save_file = path.replace('.encoded.png', '.decoded.png')
        else:
            save_file = os.path.splitext(path)[0] + '.decoded.png'
            
        cv2.imwrite(save_file, encoded_img)
        
        return
    
    def run(self, mode, key, path, threshold):
        if mode.upper() == "ENCODE":
            self.encode(path, key, threshold)
        elif mode.upper() == "DECODE":
            self.decode(path, key, threshold)
        
        return

if __name__ == "__main__":
    arguments = sys.argv
    if not len(arguments) == 4 and not len(arguments) == 5:
        print('[ERROR] Incorrect number of arguments. Terminating program.')
        quit()
    
    mode = arguments[1]
    key = arguments[2]
    path = arguments[3]
    
    if key == "":
        print('[ERROR] Key missing. Terminating program.')
        quit()
    
    if mode.upper() == "ENCODE" or mode.upper() == "DECODE":
        if not os.path.isfile(path):
            print('[ERROR] Incorrect file. Terminating program.')
            quit()
    else:
        print('[ERROR} Incorrect mode. Terminating program.')
        quit()
    
    if len(arguments) == 3:
        threshold = 5
    else:
        threshold = arguments[4]
        if threshold.isnumeric():
            threshold = int(threshold)
        else:
            print('[ERROR} Invalid threshold value. Terminating program.')
            quit()
    
    sn = safedun()
    sn.run(mode, key, path, threshold)
    