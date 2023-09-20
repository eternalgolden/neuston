"""
      ___           ___           ___           ___                         ___           ___     
     /\  \         /\__\         /\  \         /\__\                       /\  \         /\  \    
     \:\  \       /:/ _/_        \:\  \       /:/ _/_         ___         /::\  \        \:\  \   
      \:\  \     /:/ /\__\        \:\  \     /:/ /\  \       /\__\       /:/\:\  \        \:\  \  
  _____\:\  \   /:/ /:/ _/_   ___  \:\  \   /:/ /::\  \     /:/  /      /:/  \:\  \   _____\:\  \ 
 /::::::::\__\ /:/_/:/ /\__\ /\  \  \:\__\ /:/_/:/\:\__\   /:/__/      /:/__/ \:\__\ /::::::::\__\
 \:\~~\~~\/__/ \:\/:/ /:/  / \:\  \ /:/  / \:\/:/ /:/  /  /::\  \      \:\  \ /:/  / \:\~~\~~\/__/
  \:\  \        \::/_/:/  /   \:\  /:/  /   \::/ /:/  /  /:/\:\  \      \:\  /:/  /   \:\  \      
   \:\  \        \:\/:/  /     \:\/:/  /     \/_/:/  /   \/__\:\  \      \:\/:/  /     \:\  \     
    \:\__\        \::/  /       \::/  /        /:/  /         \:\__\      \::/  /       \:\__\    
     \/__/         \/__/         \/__/         \/__/           \/__/       \/__/         \/__/    




Project Neuston

developed by E.G.B, script by 대표 

August 2023


"""
# other file imports

from shrine import *
from enums import *
from discord_auth import *
from discord.ext import commands
from place import *


import google_sheets as gs
import owner_loader as ol
import formatter as frmat
import discord

places = {}
characters = {}
owners = {}

blind = True

@client.event
async def on_ready():

    global places
    global characters
    global owners
    global blind

    # init places - hq(0), dawn(1)
    print("loading places ...")
    hq_desc = gs.get(Sheet.HQ.value, "D1:D2")
    hq_arrival = gs.get_single(Sheet.HQ.value, "D4")
    hq = Place("hq", hq_desc[0][0], hq_desc[1][0], hq_arrival)
    hq.kor_acr = "본부"
    places["hq"] = hq

    dawn_desc = gs.get(Sheet.DAWN.value, "D1:D2")       # official name and desc
    dawn_arrival = gs.get_single(Sheet.DAWN.value, "D4")
    dawn =  Place("dawn", dawn_desc[0][0], dawn_desc[1][0], dawn_arrival)   # auto loads the search thing 
    dawn.kor_acr = "새벽녘마을"
    places["dawn"] = dawn
    print("loading places complete")

    # init owners and characters
    print("loading owners / characters ...")
    unpack = ol.get_owners()
    characters = unpack[0]
    owners = unpack[1]

    for n, ch in characters.items():
        if ch.place == Dest.DAWN.value:
            ch.place = places["dawn"]
            print(str(ch.name) + " is in dawn")
        elif ch.place == Dest.HQ.value:
            ch.place = places["hq"]
            print(str(ch.name) + " is in hq")
    for o, ow in owners.items():
        if ow.main != None:
            ow.main = ow.character_list[ow.main]

    print("loading owners / characters complete")

    print(f'{client.user.name} -- Finished loading everything!')

@client.event
async def on_message(m):

    global places
    global characters
    global owners
    global blind
    global client

  
    username = str(m.author)
    content = str(m.content)
    channel = str(m.channel)

    if channel == "커맨드" and (content == "q" or content == "ㅂ"):
        await client.close()

    if (blind and (channel != "테스트")) or not username in owners:
        return

       # start splitting msg
    msg = content.split("[")
    if len(msg) == 1:
        return

    for a in msg:
        if "]" in a:
            msg = a
            break
    msg = msg.split("]")[0]

    curr_owner = owners[username]
    if curr_owner.main == None and not "메인" in msg:
        ret_str ="[먼저 메인 캐릭터를 설정해주시길 바랍니다.\n"
        ret_str += f"현재 {curr_owner.name} 님은 {str(list(curr_owner.character_list.keys()))}중 선택하실 수 있습니다.]"
        await m.channel.send(ret_str)
        return

    elif "메인" in msg:
        main_ch = msg.split("-")[1]
        return_msg = curr_owner.set_main(main_ch)
        await m.channel.send(return_msg)
        return

    elif "정보" == msg:
        ret_str = f"[:mag: 알티 아스테레스 [본부]가 위치해있는 머큐리에서 탐색 가능한 구역 목록입니다.\n\n"

        for p, pl in places.items():
            ret_str += f"> {pl.name}\n약칭 - {pl.kor_acr}\n{pl.desc}\n"

        ret_str += f"\n[이동-구역이름(약칭)] 으로 움직일 수 있습니다.]"
        await m.channel.send(ret_str)
        return

    elif "이동" in msg:
        new_place = None
        mm = msg.split("-")[1]

        if mm == curr_owner.main.place.kor_acr:
            await m.channel.send(f"[이미 {curr_owner.main.name}(은)는 {mm}에 있습니다.]")
            return
        elif mm == "새벽녘마을":
            new_place = places['dawn']
        elif mm  == "본부":
            new_place = places['hq']
        else:
            await m.channel.send(f"[해당 구역({mm})을 찾을 수 없습니다.]")
            return

        ret_str = curr_owner.main.move_places(new_place)
        await m.channel.send(ret_str)
        return

    elif "탐색" == msg:
        if curr_owner.main.search_count < -5:
            await m.channel.send("*오늘은 더이상 탐색을 진행할 수 없다.*")
        else:
            await m.channel.send(curr_owner.main.search())
        return

    elif "위치" == msg:
        await m.channel.send(frmat.place_formatter(curr_owner.main.place))
        return

    elif "나" == msg:
        await m.channel.send(frmat.character_formatter(curr_owner.main))
        return

    else: # choices!!
        if curr_owner.main.state != None:
            a = curr_owner.main.choice(msg)
            print(a)
            if a != "":
                await m.channel.send(a)
        return




client.run(TOKEN)
