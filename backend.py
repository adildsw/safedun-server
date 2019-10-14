# -*- coding: utf-8 -*-
"""
safedun-server Backend

Created on Sun Oct 13 00:00:00 2019
Author: Adil Rahman
GitHub: https://github.com/adildsw/safedun-server

"""

import cv2
import numpy
import math

from io import BytesIO

class safedun:
    def __init__(self, max_size=5):
        """
        Parameters
        ----------
        max_size : int, optional
            Maximum size of the output file (in megabytes) (default: 5)
        """

        self.max_size = max_size #maximum megabyte filesize allowed
        self.PIXEL_LIMIT = self.max_size * 1024 * 1024

        return

    def _preprocess(self):
        """Loading image from buffer, checking for memory spills, splitting
        image channels, and calculating various factors for operation.
        """
        self._img = numpy.fromfile(self.file, numpy.uint8)
        self._img = cv2.imdecode(self._img, cv2.IMREAD_COLOR)

        self._height, self._width, self._channel = self._img.shape

        pixel_count = self._height * self._width * self._channel

        if pixel_count > self.PIXEL_LIMIT:
            self._resize()

        self._h_factor = math.ceil(self._height/1000)
        self._w_factor = math.ceil(self._width/1000)

        self._channel_b = numpy.copy(self._img[:, :, 0])
        self._channel_g = numpy.copy(self._img[:, :, 1])
        self._channel_r = numpy.copy(self._img[:, :, 2])

        self._processed_img = numpy.zeros((self._height, self._width, self._channel))

        self._key_length = len(self.key)

        return

    def _resize(self):
        """Resizing image."""
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

        self._img = cv2.resize(self._img, (self._width, self._height))

        return

    def _scramble(self):
        """Scrambling the channels of the image."""

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

    def _unscramble(self):
        """Unscrambling the channels of the image."""

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

    def _result(self):
        """Combines all the scrambled channels into one image matrix, converts
        the matrix into a BytesIO buffer and returns it.

        Returns
        -------
        BytesIO Buffer
            The image after scramble/unscramble operation stored in a BytesIO
            buffer
        """

        self._processed_img[..., 0] = self._channel_b
        self._processed_img[..., 1] = self._channel_g
        self._processed_img[..., 2] = self._channel_r

        _, processed_img_buffer = cv2.imencode(".png", self._processed_img)
        output_file = BytesIO(processed_img_buffer)

        return output_file

    def generate(self, mode, cycle, key, file):
        """Runs the pipeline to generate and return the resultant image in the
        form of a BytesIO buffer.

        Parameters
        ----------
        mode : str
            The operation mode chosen (scramble/unscramble)
        key : str
            The keyphrase used to scramble/unscramble the image
        cycle : int
            Number of scrambling/unscrambling iterations
        file : werkzeug.FileStorage
            Incoming file from the flask server for scrambling/unscrambling

        Returns
        -------
        BytesIO Buffer
            The image after scramble/unscramble operation stored in a BytesIO
            memory buffer
        """

        self.mode = mode
        self.cycle = cycle
        self.key = key
        self.file = file

        self._preprocess()

        if self.mode == "scramble":
            self._scramble()
        elif self.mode == "unscramble":
            self._unscramble()

        output_file = self._result()

        return output_file
