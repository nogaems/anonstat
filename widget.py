#!/usr/bin/env python3
# coding: utf-8
import math

from PIL import Image, ImageDraw, ImageFont


class Context:
    base = {}
    font = {}

    def __init__(self):
        self.base['small'] = Image.open(
            'templates/counter-small.png').convert('RGBA')
        self.font['small'] = ImageFont.truetype(
            'templates/terminus-bold.ttf', 18)

    def draw_small(self, data,
                   template='{uday} {uweek} {umonth}\n{hday} {hweek} {hmonth}',
                   position=(22, 23),
                   color=(243, 108, 00, 255),
                   spacing=2):
        text = Image.new('RGBA', self.base['small'].size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(text)
        data = self.prepare_data(data)
        message = template.format(**data)
        draw.multiline_text(
            position,
            message,
            font=self.font['small'],
            fill=color,
            spacing=spacing
        )
        out = Image.alpha_composite(self.base['small'], text)
        return out

    def prepare_data(self, data):
        for key in data:
            try:
                data[key] = self.rjust(data[key])
            except ValueError:
                data[key] = str(data[key])[:3]
        return data

    def rjust(self, number):
        if number < 0:
            raise ValueError('\'number\' should be positive')
        if number < 10 ** 3:
            return str(number).rjust(4, ' ')
        if number < 10 ** 6:
            return self._with_letter(number, 'K')
        if number < 10 ** 9:
            return self._with_letter(number / 10 ** 3, 'M')

    def _with_letter(self, number, letter):
        t = str(number / 10 ** 3)
        if t.find('.') in (1, 3):
            return t[:3] + letter
        else:
            return ' ' + t.split('.')[0] + letter

# data = {
#     'uday': 1234,
#     'uweek': 1234,
#     'umonth': 1234,
#     'hday': 1234,
#     'hweek': 1234,
#     'hmonth': 1234
# }

# c = Context()
# img = c.draw_small(data)
# img.save('out.png')
