# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 00:24:26 2019

@author: AdilDSW
"""

import cv2
import numpy
import math

class safedun:
    def __init__(self, mode, key, cycle, path):
        self.mode = mode
        self.key = key
        self.cycle = cycle
        self.path = path
        
        self.MAX_MB = 5 #maximum megabyte filesize allowed
        self.PIXEL_LIMIT = self.MAX_MB * 1024 * 1024
        
        self.output_dir = 'temp/output.png'
        
        return
    
    def _preprocess(self):
        self.img = cv2.imread(self.path)
        self._height, self._width, self._channel = self.img.shape
        
        pixel_count = self._height * self._width * self._channel
        
        if pixel_count > self.PIXEL_LIMIT:
            self._resize()
        
        self._h_factor = math.ceil(self._height/1000)
        self._w_factor = math.ceil(self._width/1000)
        
        self._channel_b = numpy.copy(self.img[:, :, 0])
        self._channel_g = numpy.copy(self.img[:, :, 1])
        self._channel_r = numpy.copy(self.img[:, :, 2])
        
        self.processed_img = numpy.zeros((self._height, self._width, self._channel))
        
        self._key_length = len(self.key)
        
        return

    def _resize(self):
        if self._height > self._width:
            ratio = self._height/self._width
            self._height = math.sqrt((self.PIXEL_LIMIT * ratio)/3)
            self._width = self._height/ratio
        else:
            ratio = self._width/self._height
            self._width = math.sqrt((self.PIXEL_LIMIT * ratio)/3)
            self._height = self._width/ratio
        
        self._height = math.floor(self._height)
        self._width = math.floor(self._width)
        
        self.img = cv2.resize(self.img, (self._width, self._height))
            
        return
    
    def _encode(self):
        for i in range(self.cycle):
            key_idx = 0
            shift_direction = 0

            for row in range(self._height):
                for ch in range(self._channel):
                    asciiKey = ord(self.key[key_idx])
                    roll_unit = asciiKey if shift_direction%2 == 1 else ((-1) * asciiKey)
                    roll_unit *= self._h_factor
                    key_idx = (key_idx + 1)%self._key_length
                    shift_direction += 1
                    if ch == 0:
                        self._channel_b[row] = numpy.roll(self._channel_b[row], roll_unit)
                    elif ch == 1:
                        self._channel_g[row] = numpy.roll(self._channel_g[row], roll_unit)
                    else:
                        self._channel_r[row] = numpy.roll(self._channel_r[row], roll_unit)

            key_idx = 0
            shift_direction = 0

            for column in range(self._width):
                for ch in range(self._channel):
                    asciiKey = ord(self.key[key_idx])
                    roll_unit = asciiKey if shift_direction%2 == 1 else ((-1) * asciiKey)
                    roll_unit *= self._w_factor
                    key_idx = (key_idx + 1)%self._key_length
                    shift_direction += 1
                    if ch == 0:
                        self._channel_b[:, column] = numpy.roll(self._channel_b[:, column], roll_unit)
                    elif ch == 1:
                        self._channel_g[:, column] = numpy.roll(self._channel_g[:, column], roll_unit)
                    else:
                        self._channel_r[:, column] = numpy.roll(self._channel_r[:, column], roll_unit)

        return

    def _decode(self):
        for i in range(self.cycle):
            key_idx = 0
            shift_direction = 0

            for column in range(self._width):
                for ch in range(self._channel):
                    asciiKey = ord(self.key[key_idx])
                    roll_unit = asciiKey if shift_direction%2 == 0 else ((-1) * asciiKey)
                    roll_unit *= self._w_factor
                    key_idx = (key_idx + 1)%self._key_length
                    shift_direction += 1
                    if ch == 0:
                        self._channel_b[:, column] = numpy.roll(self._channel_b[:, column], roll_unit)
                    elif ch == 1:
                        self._channel_g[:, column] = numpy.roll(self._channel_g[:, column], roll_unit)
                    else:
                        self._channel_r[:, column] = numpy.roll(self._channel_r[:, column], roll_unit)

            key_idx = 0
            shift_direction = 0

            for row in range(self._height):
                for ch in range(self._channel):
                    asciiKey = ord(self.key[key_idx])
                    roll_unit = asciiKey if shift_direction%2 == 0 else ((-1) * asciiKey)
                    roll_unit *= self._h_factor
                    key_idx = (key_idx + 1)%self._key_length
                    shift_direction += 1
                    if ch == 0:
                        self._channel_b[row] = numpy.roll(self._channel_b[row], roll_unit)
                    elif ch == 1:
                        self._channel_g[row] = numpy.roll(self._channel_g[row], roll_unit)
                    else:
                        self._channel_r[row] = numpy.roll(self._channel_r[row], roll_unit)

        return
    
    def _saveResult(self):
        self.processed_img[..., 0] = self._channel_b
        self.processed_img[..., 1] = self._channel_g
        self.processed_img[..., 2] = self._channel_r

        cv2.imwrite(self.output_dir, self.processed_img)
        
        return
    
    def run(self):
        self._preprocess()
        
        if self.mode.upper() == "ENCODE":
            self._encode()
        elif self.mode.upper() == "DECODE":
            self._decode()
        
        self._saveResult()

        return
