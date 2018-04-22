#!/usr/bin/env python3
# coding: utf-8
import math

from PIL import Image, ImageDraw, ImageFont


class Template:

    def __init__(self, renderer, extractors):
        self.renderer = renderer
        self.extractors = extractors

    def render(self, data):
        return self.renderer(data)
