'''
    image.py

    testing image module

'''

from PIL import Image, ImageDraw, ImageFont
import discord
from io import BytesIO
import requests

def testing():
    cell_size = 100
    board_size = (cell_size*22)
    checker_board = Image.new(mode="RGB", size=(board_size, board_size), color=(255, 255, 255))

    vert_bar = Image.new(mode="RGB", size=(board_size, cell_size), color=(250, 200, 152))
    horiz_bar = Image.new(mode="RGB", size=(cell_size, board_size), color=(250, 200, 152))

    checker_board.paste(vert_bar, (0,0))
    checker_board.paste(vert_bar, (0, (cell_size*21)))
    checker_board.paste(horiz_bar, (0,0))
    checker_board.paste(horiz_bar, ((cell_size*21), 0))

    vert_line = Image.new(mode="RGB", size=(2,board_size), color=(0,0,0))
    horiz_line = Image.new(mode="RGB", size=(board_size, 2), color =(0,0,0))
    for i in range(1, 22):
        checker_board.paste(vert_line, ((cell_size*i), 0))
        checker_board.paste(horiz_line, (0, (cell_size*i)))

    checker_board.show()


'''
async def testing_image(channel):

    im = Image.new(mode="RGB", size=(40, 40), color=(0, 0, 0))
    # 추가할 다른 이미지 생성
    url = "https://pbs.twimg.com/media/F65aoyTaoAAvEbl.png"
    res = requests.get(url).content
    im2 = Image.open(BytesIO(res))
    im2 = im2.resize((100, 115))
    # (0, 0) 좌표에 이미지 붙여넣기
    im.paste(im2, (0, 0))

    # 텍스트 출력을 위한 ImageDraw.Draw
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("./IropkeBatangM/IropkeBatangM.ttf", 20)
    #font = ImageFont.truetype("Menlo.ttc", 20) #트루타입 폰트
    # (1, 1) 좌표에 'A' 텍스트 생성
    draw.text((150, 200), "이상헤브", font=font, fill=(255, 0, 0))

    with BytesIO() as image_binary:
        im.save(image_binary, "png")
        image_binary.seek(0)
        out = discord.File(fp=image_binary, filename = "image.png")
        await channel.send(file=out)
'''
