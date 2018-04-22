# Default template file
from PIL import Image, ImageDraw, ImageFont

extractors = {
    'uday': '''
    SELECT COUNT(DISTINCT id)
    FROM stats
    WHERE datetime(ts, 'unixepoch', 'localtime')
    BETWEEN datetime('now', '-1 day','localtime' ) and datetime('now', 'localtime')
    ''',
    'uweek': '''
    SELECT COUNT(DISTINCT id)
    FROM stats
    WHERE datetime(ts, 'unixepoch', 'localtime')
    BETWEEN datetime('now', '-7 days','localtime' ) and datetime('now', 'localtime')
    ''',
    'umonth': '''
    SELECT COUNT(DISTINCT id)
    FROM stats
    WHERE datetime(ts, 'unixepoch', 'localtime')
    BETWEEN datetime('now', '-1 month','localtime' ) and datetime('now', 'localtime')
    ''',
    'hday': '''
    SELECT COUNT(id)
    FROM stats
    WHERE datetime(ts, 'unixepoch', 'localtime')
    BETWEEN datetime('now', '-1 day','localtime' ) and datetime('now', 'localtime')
    ''',
    'hweek': '''
    SELECT COUNT(id)
    FROM stats
    WHERE datetime(ts, 'unixepoch', 'localtime')
    BETWEEN datetime('now', '-7 days','localtime' ) and datetime('now', 'localtime')
    ''',
    'hmonth': '''
    SELECT COUNT(id)
    FROM stats
    WHERE datetime(ts, 'unixepoch', 'localtime')
    BETWEEN datetime('now', '-1 month','localtime' ) and datetime('now', 'localtime')
    ''',
}


def render(data):
    base = Image.open('templates/counter-small.png').convert('RGBA')
    font = ImageFont.truetype('templates/terminus-bold.ttf', 18)
    template_string = '{uday} {uweek} {umonth}\n{hday} {hweek} {hmonth}'
    position = (22, 23)
    color = (243, 108, 00, 255)
    spacing = 2
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text)
    data = prepare_data(data)
    message = template_string.format(**data)
    draw.multiline_text(
        position,
        message,
        font=font,
        fill=color,
        spacing=spacing
    )
    out = Image.alpha_composite(base, text)
    return out


def prepare_data(data):
    for key in data:
        try:
            if isinstance(data[key], str):
                continue
            data[key] = rjust(data[key])
        except ValueError:
            data[key] = str(data[key])[:3]
    return data


def rjust(number):
    number = int(number)
    if number < 0:
        raise ValueError('\'number\' should be positive')
    if number < 10 ** 3:
        return str(number).rjust(4, ' ')
    if number < 10 ** 6:
        return _with_letter(number, 'K')
    if number < 10 ** 9:
        return _with_letter(number / 10 ** 3, 'M')


def _with_letter(number, letter):
    t = str(number / 10 ** 3)
    if t.find('.') in (1, 3):
        return t[:3] + letter
    else:
        return ' ' + t.split('.')[0] + letter
