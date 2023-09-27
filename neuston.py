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

places = {}
characters = {}
owners = {}
bulletin_board = {}

instances = {'S1': None, 'S2': None, 'S3': None}

debugging = True

@client.event
async def on_ready():

    global places, characters, owners
    global debugging
    global restore_timer

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
        if not "] " in content:
            await m.channel.send(f"*[캐릭터이름](한칸띄우기)[메세지]의 양식에 맞춰 메세지를 등록해주세요.*")
            return
        msgs = content.split("] ")
        ch_name = msgs[0][1:]
        if len(msgs) == 1:
            await m.channel.send(f"*메세지를 제대로 입력해주세요.*")
            return
        else:
            bullet_message = msgs[1]

        if ch_name in characters.keys():
            bulletin_board[ch_name] = bullet_message

            # update bulletin
            said_character = characters[ch_name]
            gs.put_single(Sheet.CHARACTER.value, 'I' + str(int(said_character.bag_index[1])-1), bullet_message)

            await m.channel.send(f"*성공적으로 게시판 메세지가 업데이트 되었습니다.*\n*[{bullet_message}]*")
            return
        else:
            await m.channel.send("*해당 캐릭터를 찾지 못했습니다.*")
            return

    if debugging == True and (not channel in [e.value for e in M_Channel] and channel != "mock-본부" and channel != "mock-조사4"):
        return

    # all msgs stored in here
    msgs = []
    return_string = ""

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

    # process all messages
    for msg in msgs:
        # switch characters
        if msg in characters.keys():
            ch = curr_owner.find_character(msg)
            if ch == None:
                return_string += f"*당신은 '{msg}'의 권한이 없습니다. 다시 설정해주십시오.*\n"
                await m.channel.send(return_string)
                return
            else:
                set_character = True
                curr_char = ch

        elif "메인" in msg:
            ch_name = msg.split("-")[1]
            return_string += curr_owner.set_main(ch_name) + "\n"
            curr_char = curr_owner.main

        elif "정보" == msg:
            return_string += f"[:mag: 알티 아스테레스 [본부]가 위치해있는 머큐리에서 탐색 가능한 구역 목록입니다.\n"
            for p, pl in places.items():
                return_string += f"> {pl.name}\n약칭 - {pl.kor_acr}\n{pl.desc}\n"
            return_string += f"\n[이동-구역이름(약칭)] 으로 움직일 수 있습니다.]"

        elif curr_char == None:
            return_string += f"*[{msg}] 전에 먼저 메인캐릭터를 설정해주세요.*\n현재 {curr_owner.name} 님은 {str(list(curr_owner.character_list.keys()))}중 선택하실 수 있습니다."
            await m.channel.send(return_string)
            return

        elif msg == "나":
            return_string += frmat.character_formatter(curr_char)
        
        elif "위치" == msg:
            return_string += frmat.place_formatter(curr_char.place)

        elif "날씨" == msg:
            pass

        else:   # actions depending on instance -- 이동, 탐색 / else -> choice

            # check if in instance first
            # S1, S2 or S3
            for k, v in instances.items():
                if curr_char in v.character_list:
                    curr_instance = k
                    break


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
                    curr_instance = channel_name

                    print(curr_char.search_count)
                    instances[channel_name].search_count += curr_char.search_count
                    curr_char.search_count = 0

                    # debug
                    for k,v in instances.items():
                        print (k + " " + str(v))
                    print(curr_instance)

                    return_string += f"*[{curr_char.name}](이)가 [{channel}]에 참여한다.*"


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
                            return_string += "\n*[개인조사-4]로 이동해 탐색을 진행하자.*"
               

            else:
                return_string += frmat.wrong_command(msg)
                break



        if set_character:
            set_character = False
        else:
            return_string += "\n" + frmat.DIVIDE + "\n\n"
           

    if return_string != "":
        return_string = return_string[:len(return_string) - 23]
        await m.channel.send(return_string)
    return


# ============================================================================================================================ 

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
