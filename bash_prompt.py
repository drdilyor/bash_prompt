import os
from colorsys import hls_to_rgb

esc = '\033['
reset = esc+'0m'
back = esc+'48:2:{}:{}:{}m'
fore = esc+'38:2:{}:{}:{}m'

class BreadCrumb:
    def __init__(self, sep: str):
        self.items = []
        self.sep = sep

    def add(self, item: str, bg: tuple, fg: tuple) -> None:
        self.items.append((item, bg, fg))

    def __str__(self) -> str:
        result = []
        last_bg: tuple = None
        for item, bg, fg in self.items:
            if last_bg:
                result.extend([fore.format(*last_bg),
                               back.format(*bg),
                               self.sep])

            result.extend([back.format(*bg),
                           fore.format(*fg),
                           item])
            last_bg = bg
        result.append(reset)
        return ''.join(result)

class Exponention:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def get(self, fr):
        return self.start + fr ** 1.2 * (self.end - self.start)


def color_shade(hue: float, shade: int):
    return tuple(int(i * 255.9) for i in hls_to_rgb(hue, shade/100, 1))

path = os.getcwd()[1:].split('/')
last_path = path.pop()

if path[:2] == ['home', 'drdilyor']:
    path[:2] = ['~']

bread = BreadCrumb('▶')

hue_blue = .55
white = (255, 255, 255)
shade_start = 10
shade_end = 50
shade_points = Exponention(shade_start, shade_end if len(path) > 2 else 25)


fr = 0
fr_step = 1 / (len(path)-1) if len(path) > 1 else 1

for dir in map(lambda i: i + ' ', path):
    shade = shade_points.get(fr)
    bread.add(item=dir,
              bg=color_shade(hue_blue, shade),
              fg=white)

    last_shade = shade
    # print(int(shade*10)/10
    # exponential grow:
    #
    # |        *
    # |       /
    # |     _*
    # | _,-^
    # +-----------
    fr += fr_step

bread.add(last_path + ' ', color_shade(hue_blue, 85), color_shade(hue_blue, 20))

print(str(bread))
