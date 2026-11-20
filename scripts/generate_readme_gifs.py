#!/usr/bin/env python3
"""PallTune's own lightweight animated README visuals.
All text/art/animation is original; no stock images, music or third-party GIFs.
"""
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("assets")
OUT.mkdir(exist_ok=True)
BG = (10, 12, 16)
INK = (242, 244, 248)
MUTED = (146, 153, 165)
SILVER = (204, 210, 219)
EDGE = (49, 55, 65)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(size, bold=False):
    path = BOLD if bold else FONT
    if os.path.exists(path):
        return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def backdrop(w, h):
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line((0, y, w, y), fill=(int(8 + 12*t), int(10 + 13*t), int(14 + 17*t)))
    for x in range(-h, w + h, 120):
        d.line((x, 0, x + h, h), fill=(30, 34, 42), width=1)
    d.rounded_rectangle((9, 9, w - 10, h - 10), radius=24, outline=EDGE, width=2)
    d.line((30, h-28, w-30, h-28), fill=(45, 50, 58), width=1)
    return im


def oval(d, x, y, rad, stroke=SILVER, width=2):
    d.ellipse((x-rad, y-rad, x+rad, y+rad), outline=stroke, width=width)


def wave(d, left, mid, amount, count, spacing, phase, width=7):
    for i in range(count):
        t = (i / max(count-1, 1)) * 2 * math.pi
        envelope = .25 + .75 * (math.sin(math.pi*i/max(count-1, 1))**2)
        height = max(4, int((amount * envelope) * (0.58 + 0.42 * math.sin(t*1.7 + phase)**2)))
        x = left + i*spacing
        color = (184 + int(30*envelope), 189 + int(27*envelope), 198 + int(26*envelope))
        d.rounded_rectangle((x, mid-height, x+width, mid+height), radius=width//2, fill=color)


def brand(d, x, y):
    oval(d, x+15, y+15, 14, stroke=(187, 194, 204), width=2)
    d.arc((x+7,y+6,x+23,y+24), 210, 480, fill=(232,234,238), width=3)
    d.text((x+43, y+14), "PALLTUNE", font=f(16, True), fill=INK, anchor="lm")


def hero(i, n):
    w, h = 1000, 328
    im = backdrop(w, h)
    d = ImageDraw.Draw(im)
    phase = math.tau*i/n
    brand(d, 43, 35)
    d.rounded_rectangle((755, 41, 951, 78), radius=18, fill=(34, 38, 46), outline=(68,74,83))
    d.text((853, 59), "ANDROID  /  FREE", font=f(12, True), fill=(206, 211, 218), anchor="mm")
    d.text((50, 136), "MUSIC IS", font=f(31, True), fill=(157, 164, 173))
    d.text((47, 221), "YOUR SPACE.", font=f(68, True), fill=INK, anchor="ls")
    d.text((50, 264), "MUSIKMU, SELERAMU.", font=f(19, True), fill=(188,194,205))
    for j in range(3):
        r = 92 + 13*j
        oval(d, 816, 200, r, stroke=(37 + j*13, 41 + j*13, 50 + j*12), width=2)
    # Orbit points provide quiet motion without flashy gradients.
    for j in range(3):
        ang = phase * (1 if j != 1 else -1) + j*math.tau/3
        rr = 104 + (j%2)*18
        x = 816 + rr*math.cos(ang)
        y = 200 + rr*math.sin(ang)
        d.ellipse((x-5,y-5,x+5,y+5),fill=(195,201,211))
    d.ellipse((745,129,887,271),fill=(19,22,28),outline=(106,112,123),width=2)
    d.ellipse((766,150,866,250),outline=(78,84,94),width=2)
    wave(d, 771, 200, 25, 11, 8, phase, width=4)
    d.text((50, 305), "A MUSIC EXPERIENCE, YOUR WAY", font=f(10, True), fill=(111,118,130))
    return im


def player(i, n):
    im = backdrop(560, 225)
    d = ImageDraw.Draw(im)
    phase = math.tau*i/n
    brand(d, 31, 26)
    d.text((33, 103), "PRESS PLAY.", font=f(32, True), fill=INK)
    d.text((34, 139), "Make every moment yours.", font=f(14), fill=MUTED)
    d.rounded_rectangle((34, 167, 310, 174),radius=4, fill=(62,69,79))
    d.rounded_rectangle((34, 167, 34 + int(276*(0.23 + .62*i/n)), 174), radius=4, fill=(209,216,227))
    d.ellipse((34 + int(276*(0.23 + .62*i/n)) - 5, 164, 34 + int(276*(0.23 + .62*i/n)) + 5, 177),fill=INK)
    oval(d, 423, 113, 77, stroke=(80,86,96), width=2)
    oval(d, 423, 113, 53, stroke=(49,55,66), width=2)
    wave(d, 365, 114, 26, 13, 9, phase, width=5)
    return im


def playlist(i, n):
    im = backdrop(560, 225)
    d = ImageDraw.Draw(im)
    brand(d, 31, 24)
    d.text((35, 80), "YOUR PLAYLIST.", font=f(25, True), fill=INK)
    names = ["01   NIGHT DRIVE", "02   SLOW MORNING", "03   AFTER HOURS"]
    selected = (i//7) % 3
    for j, label in enumerate(names):
        y = 100 + j*35
        if j == selected:
            d.rounded_rectangle((30,y,526,y+31), radius=9, fill=(55,61,71), outline=(98,104,113))
        d.text((46, y+15),label,font=f(13,True),fill=INK if j==selected else MUTED,anchor="lm")
        if j == selected:
            wave(d, 455, y+16, 7, 7, 7, i*.75, width=3)
        else:
            d.text((504,y+16),"···",font=f(16),fill=(105,111,122),anchor="mm")
    return im


def lyrics(i, n):
    im = backdrop(560, 225)
    d = ImageDraw.Draw(im)
    brand(d, 31, 24)
    d.text((35, 85), "SING ALONG.", font=f(25, True), fill=INK)
    lines = ["TURN UP THE FEELING", "FOLLOW THE WORDS", "OWN THE MOMENT"]
    selected = (i//7)%3
    for j, label in enumerate(lines):
        y = 119 + j*30
        fg = INK if j == selected else (87,92,101)
        d.text((38, y),label,font=f(16,True),fill=fg,anchor="lm")
        if j == selected:
            d.rounded_rectangle((34,y+13,34+int(220*((i%7)+1)/7),y+15), radius=2, fill=(190,197,207))
    return im


def together(i, n):
    im = backdrop(560, 225)
    d = ImageDraw.Draw(im)
    phase = math.tau*i/n
    brand(d,31,24)
    d.text((35,82),"LISTEN TOGETHER.",font=f(23,True),fill=INK)
    for x,name in [(120,"YOU"),(440,"FRIEND")]:
        oval(d,x,148,32,stroke=(161,169,182),width=3)
        d.ellipse((x-9,135,x+9,153),fill=(183,191,203))
        d.arc((x-16,145,x+16,174),180,360,fill=(183,191,203),width=3)
        d.text((x,194),name,font=f(11,True),fill=MUTED,anchor="mm")
    d.line((160,148,399,148),fill=(75,82,94),width=2)
    wave(d,191,148,18,24,7,phase,width=3)
    cx=280+int(103*math.sin(phase))
    d.ellipse((cx-4,144,cx+4,152),fill=INK)
    return im


def visualizer(i, n):
    im = backdrop(1000, 126)
    d = ImageDraw.Draw(im)
    phase = math.tau*i/n
    wave(d, 56, 61, 36, 89, 10, phase, width=4)
    d.rounded_rectangle((345,43,657,83),radius=18,fill=(17,20,25),outline=(53,59,68))
    d.text((501,62),"PALLTUNE  •  YOUR MUSIC.",font=f(14,True),fill=INK,anchor="mm")
    return im


def save(name, builder, count=21, duration=95):
    frames = []
    for i in range(count):
        frame = builder(i,count)
        frame = frame.convert("P",palette=Image.Palette.ADAPTIVE,colors=96,dither=Image.Dither.NONE)
        frames.append(frame)
    target = OUT / name
    frames[0].save(target,save_all=True,append_images=frames[1:],
                   duration=duration,loop=0,optimize=True,disposal=2)
    with Image.open(target) as gif:
        assert gif.n_frames > 1, name
    print(f"{target}: {target.stat().st_size:,} bytes, {count} frames")


if __name__=="__main__":
    save("palltune-hero.gif",hero,24,90)
    save("palltune-player.gif",player)
    save("palltune-playlist.gif",playlist)
    save("palltune-lyrics.gif",lyrics)
    save("palltune-together.gif",together)
    save("palltune-wave.gif",visualizer,24,90)
