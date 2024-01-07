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
from threads import *
from instance import *
from helper import *
from image import *


import google_sheets as gs
import owner_loader as ol
import formatter as frmat
import discord
import time
import random

places = {}
characters = {}
owners = {}
bulletin_board = {}

instances = {'S1': None, 'S2': None, 'S3': None}

debugging = True

def parse_place(msg):
    new_place = None
    mm = msg.split("-")[1]

    if mm == "새벽녘마을":
        new_place = places['dawn']
    elif mm  == "본부":
        new_place = places['hq']

    return new_place

@client.event
async def on_ready():

    global places, characters, owners
    global debugging
    global restore_timer
    global bulletin_board

    print("starting time measuring thread...")
    restore_timer.start()

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
            print(str(ch.name) + " is in hq ")
    for o, ow in owners.items():
        if ow.main != None:
            ow.main = ow.character_list[ow.main]

    print("loading owners / characters complete")

    print("setting up instances...")
    instances['S1'] = Instance('S1')
    instances['S2'] = Instance('S2')
    instances['S3'] = Instance('S3')
    print("setting up instances complete")

    print("setting up bulletin board...")
    bulletin_board = init_bulletin()

    print(f'{client.user.name} -- Finished loading everything!')

@client.event
async def on_message(m):

    global places, characters, owners, instances
    global debugging
    global client
    global restore_timer
    global inst_one, inst_two, inst_three
  
    username = str(m.author)
    content = str(m.content)
    channel = str(m.channel)

    if channel == "커맨드" and (content == "q" or content == "ㅂ"):
        exit_event.set()
        restore_timer.join()
        await client.close()

    if content == "ㅁ":
        await make_testing_checkerboard(m.channel)
        return

    if "Direct Message" in channel and username in owners.keys():
        if "] " in content:
#            await m.channel.send(f"*[캐릭터이름](한칸띄우기)[메세지]의 양식에 맞춰 메세지를 등록하자.*")
            msgs = content.split("] ")
            ch_name = msgs[0][1:]
            if len(msgs) > 1 and ch_name in characters.keys():
                bulletin_board[ch_name] = msgs[1]
                # update bulletin
                said_character = characters[ch_name]
                gs.put_single(Sheet.CHARACTER.value, 'I' + str(int(said_character.bag_index[1])-1), msgs[1])
                await m.channel.send(f"*{SystemMessage.CONFIRM.value}*\n*\"{msgs[1]}\"*")
                return
        await m.channel.send("*{SystemMessage.WRONGFORM.value}*")
        return

    if debugging == True and (not channel in [e.value for e in M_Channel] and channel != "mock-본부" and channel != "mock-조사4" and channel != "커맨드"):
        return

    # all msgs stored in here
    msgs = []
    ret_str = ""

    # start splitting msg
    msg = content.split("[")
    if len(msg) == 1:
        return

    for a in msg:
        if "]" in a:
            msgs.append(a.split("]")[0])

    if not username in owners.keys():
        return

    curr_owner = owners[username]
    curr_char = curr_owner.main
    curr_instance = None

    set_character = False

    command_num  = 1

    # process all messages
    for msg in msgs:

        return_string = ""
                

        # switch characters
        if msg in characters.keys():
            ch = curr_owner.find_character(msg)
            if channel == "커맨드":
                print(str(ch))
                return
            if ch == None:
                return_string += f"*당신은 '{msg}'의 권한이 없다.*\n"
                await m.channel.send(return_string)
                return
            else:
                set_character = True
                curr_char = ch

        elif "메인" in msg:
            ch_name = msg.split("-")[1]
            return_string += curr_owner.set_main(ch_name) + "\n"
            curr_char = curr_owner.main

        elif "사용법" == msg:

            #return_string += f"[:mag: 알티 아스테레스 [본부]가 위치해있는 머큐리에서 탐색 가능한 구역 목록이다.\n"
            #for p, pl in places.items():
            #    return_string += f"> {pl.name}\n약칭 - {pl.kor_acr}\n{pl.desc}\n"
            #return_string += f"\n[이동-구역이름(약칭)] 으로 움직일 수 있다.]"
            
            await client.send_message(m.author, SystemMessage.INFO.value)
            return


        elif curr_char == None:
            return_string += f"*[{msg}] 전에 먼저 메인캐릭터를 설정하자.*\n{str(list(curr_owner.character_list.keys()))}중 선택 가능하다."
            await m.channel.send(return_string)
            return

        elif msg == "나":
            return_string += frmat.character_formatter(curr_char)
        
        elif "위치" == msg:
            return_string += frmat.place_formatter(curr_char.place)

        elif "날씨" == msg:
            pass

        else:   # actions depending on instance -- 이동, 탐색, -> / else: choice

            curr_instance = curr_char.instance

            # channel reference
            channel_pool = Channel
            if debugging:
                channel_pool = M_Channel
            all_channels = [channel_pool['S1'].value, channel_pool['S2'].value, channel_pool['S3'].value]

            # in hq, wants to join
            if curr_instance == None and curr_char.state == None and "참여" == msg:
                if not channel in all_channels: # not a good channel to join
                    return_string += f"*[{channel}]에 참여할 수 없다.*"
                elif curr_char.place.acr != "hq":
                    return_string += f"*[{channel}]에 참여할 수 없다.*\n*먼저 본부로 이동 후 참여하자.*"

                else:
                    # get the S1/S2/S3 from korean name
                    channel_name = channel_pool(channel).name

                    # append to instance
                    instances[channel_name].character_list.append(curr_char)
                    curr_char.instance = instances[channel_name]
                    curr_instance = channel_name

                    print(curr_char.search_count)
                    instances[channel_name].search_count += curr_char.search_count
                    curr_char.search_count = 0

                    # debug
                    for k,v in instances.items():
                        print (k + " " + str(v))
                    print(curr_instance)

                    return_string += f"*[{curr_char.name}](이)가 [{channel}]에 참여한다.*"

            elif "->" in msg and ", " in msg: # the give command
                # first slot item, second character, third amount
                # item->ch, amt
                splitted = msg.split("->")
                sp = splitted[1].split(", ")
                receiving = None

                item = splitted[0]
                if sp[0] in characters:
                    receiving = characters[sp[0]]
                else:
                    receiving= None

                amt = sp[1]

                if not amt.isdigit():
                    return_string += "*물건을 건넬 때에는 올바른 수치를 입력하자.*"

                elif receiving != None and receiving.instance == curr_char.instance and receiving.place == curr_char.place:
                    return_string += curr_char.give(receiving, item, int(amt))

                else:
                    return_string += f"*[{sp[0]}]은(는) 존재하지 않는 사람이다. 적어도, 이 공간에는.*"


                # wrong channels -- wrote in hq but in another instance (or search 4)
            elif(   (("본부" == channel or "mock-본부" == channel) and (curr_instance != None or curr_char.place.acr != "hq")) or\
                # wrong channels -- wrote in another instance but in another instance
                    (curr_instance != None and curr_instance != channel_pool(channel).name) or\
                # wrong channels -- wrote in search 4 but is at hq
                    (("개인조사-4" == channel or "mock-조사4" == channel) and (curr_instance != None or curr_char.place.acr == "hq"))):
                print("wrong channel")
                return_string += "채팅 권한이 없다. [이동]이나 [참여]를 통해 올바른 채널으로 이동하자.\n" +frmat.DIVIDE + "\n\n"
                break


            elif (curr_instance != None and msg != "참여"): # instance -- 이동, 탐색 / choice 
                if "이동" in msg:
                    going_to = parse_place(msg)
                    if going_to == None:
                        return_string += f"*올바른 장소가 아니다. 다른 장소를 선점하자.*"
                    else:
                        return_string += instances[curr_instance].move(curr_char, going_to)# left off here
                elif "탐색" == msg:
                    return_string += instances[curr_instance].search(curr_char)
                else: # choice
                    return_string += instances[curr_instance].choice(curr_char, msg)

            elif ("개인조사-4" == channel or "mock-조사4" == channel) and msg != "참여": # individual search -- 이동, 탐색 / choice
                if "이동" in msg:
                    going_to = parse_place(msg)
                    if going_to == None:
                        return_string += f"*올바른 장소가 아니다. 다른 장소를 선점하자.*"
                    else:
                        return_string += curr_char.move_places(going_to)
                        if curr_char.place.acr == "hq":
                            curr_char.instance = None
                            return_string += "\n*[본부]로 채널을 이동하자.*"
                elif "탐색" == msg:
                    curr_char.search_count -= 1
                    if (curr_char.search_count) < 0:
                        curr_char.search_count = -1
                        curr_char.state = None
                        return_string += "*오늘은 더이상 탐색을 진행할 수 없다.*"
                    else:
                        return_string += curr_char.search()
                else:
                    return_string += curr_char.choice(msg)[1]


            elif ("본부" == channel or "mock-본부" == channel) and (msg == "게시판" or "이동" in msg): # hq -- 게시판, 이동
                if "게시판" == msg:
                    bulletin_messages = [bulletin_board[character] for character in bulletin_board.keys()]
                    return_string += " === 본부 게시판 ===\n" 
                    random.shuffle(bulletin_messages)
                    for b in bulletin_messages:
                        return_string += f'"{b}"\n'
                    return_string = return_string[:len(return_string)-1]
                elif "이동" in msg:
                    going_to = parse_place(msg)
                    if going_to == None:
                        return_string += f"*올바른 장소가 아니다. 다른 장소를 선점하자.*"
                    else:
                        return_string += curr_char.move_places(going_to)
                        if curr_char.state == None:
                            curr_char.instance = None
                            return_string += "\n*[개인조사-4]로 이동해 탐색을 진행하자.*"
            else:
                return_string += frmat.wrong_command(msg)
                break



        if set_character:
            set_character = False
        else:
            #return_string += "\n" + frmat.DIVIDE + "\n\n"
            return_string += "\n\n"

            ret_str += f"[{command_num}] ------------------- {msg}\n"
            ret_str += return_string

        return_string = ""
        command_num += 1
           

    if return_string != "":
        ret_str += return_string
    if ret_str != "":
        ret_str = ret_str[:len(ret_str)-2]
        await m.channel.send(ret_str)
    return


client.run(TOKEN)
