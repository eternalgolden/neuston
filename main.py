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

from discord_auth import *
from google_sheets import *
from character import *
from setup import *


import search_event.giver as se


# basic python functionality imports =============================================================================================

import random


# helper functions ===============================================================================================================

"""
info

"""

def info():
   pass

"""
valid_char

valid char for owner to control?

"""

def verify_character_owner(user, char_name):
    char = get_character(char_name)

    if type(char) == type(characters[0]) and char.owner == user:
        return True
    else:
        return False

def name_index(n):

    for i in range(len(characters)):
        if characters[i].name == n:
            return i

    return -1



def move_location(ch, new_place):
    comp_msg = ""
    
    if(ch.location == new_place):
        comp_msg = f"[{ch.name}]은(는) 이미 {new_place}에 있습니다.\n\n"
    elif ch.location == "해변가" or ch.location == "새벽녘 마을":
        ch.location = new_place
        n_i = name_index(ch.name)
        range_calc = str(chr(ord('I') + n_i)) + "10"
        update_sheet("기본설정", range_calc, [new_place])
        comp_msg = f"[{ch.name}]은(는) {new_place}로 향합니다.\n\n"
    else:
        comp_msg = f"[새벽녘 마을]이나 [해변가]에서만 둘 중 하나로 움직일 수 있습니다.\n\n"

    return comp_msg


# python functions for discord =====================================================================================================

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(m):


    # basic modes

    debugging = False


    # return for any other channel/yourself
    if (str(m.channel) != "조사" and str(m.channel) != "디버깅") or m.author == client.user:
        return
    
    # strip message 
    username = str(m.author)
    content = str(m.content)
    channel = str(m.channel)

    #content = content[content.find('[')+1:content.find(']')]


    # quit button
    if content == 'q':
        exit()

    if channel == "[디버깅]":
        debugging = True

    # info 
    if content == "[정보]":

        c_m = ""
        user_index = usernames.index(m.author.name)

        if main_character[user_index] == "-":
            c_m += "[메인-(캐릭터이름)]으로 메인 캐릭터를 지정해주세요.\n"
        else:
            c_m += f"현재 [{m.author.name}]님의 설정된 메인 캐릭터는 [{main_character[user_index]}]입니다.\n"

        c_m += "[돈], [소지품], [위치], [이동-(장소)], [탐색]을 할 수 있습니다."

        await m.channel.send(c_m)
        return


    # setting main
    if content.find("[메인-") != -1:
        character_name = content.split("-")[1]
        character_name = character_name[:len(character_name)-1]

        if not verify_character_owner(m.author.name, character_name):
            await m.channel.send(f"당신은 [{character_name}]의 권한이 없습니다.")
    
        else:
            name_index = usernames.index(m.author.name)
            main_character[name_index] = character_name
            range_calc = str(chr(ord('I')+name_index)) + "13"

            update_sheet("기본설정", range_calc, [character_name])
            await m.channel.send(f"[{character_name}]을(를) 메인 캐릭터로 지정했습니다.")
        return


    compiled_message = ""

    parsed_message = content.split("\n\n")
        
    for parsed in parsed_message:

        msg = ""
        ch = -1
        if parsed.find('[') != -1 and parsed.find(']') != -1:
            msg = parsed[parsed.find('[')+1:parsed.find(']')]
        else:
            break
 

        # other than main --------------------------------------------------------------------
        colon_index = parsed.find(':')

        if colon_index != -1:

            # character name
            current_character = parsed[:colon_index]

            #verify owner - no access
            if not verify_character_owner(m.author.name, current_character):
                compiled_message += f"당신은 [{current_character}]의 권한이 없습니다.\n\n"

            #verify owner - access
            else: 
                # get character
                ch = get_character(current_character)
             


        # main character ----------------------------------------------------------------------------------------------- 
        else:

            if msg != "":
                current_character = main_character[usernames.index(m.author.name)]
                if(current_character == "-"):
                    compiled_message += "현재 설정된 메인 캐릭터가 없습니다.\n\n"
                    return
                else:
                    # get character
                    ch = get_character(current_character)
           
        # if we have character
        if type(ch) == type(characters[0]):
            if msg == "이동-해변가":
                compiled_message += move_location(ch, "해변가")
            elif msg == "이동-새벽녘 마을":
                compiled_message += move_location(ch, "새벽녘 마을")
            elif msg == "돈":
                compiled_message += f"[{ch.name}]의 지갑에는 {ch.money}원이 있습니다.\n\n"
            elif msg == "소지품":
                if ch.bag != "":
                    compiled_message += f"[{ch.name}]의 인벤토리에는 {ch.bag}(이)가 들어있습니다.\n\n"
                else:
                    compiled_message += f"[{ch.name}]의 인벤토리는 텅 비어있습니다.\n\n"
            elif msg == "위치":
                compiled_message += f"[{ch.name}]은(는) {ch.location}에 있습니다.\n\n"
            else:

                if msg == "탐색":
                    ch.search_amt -= 1

                if ch.search_amt >= 0 and ch.location == "해변가": 
                    compiled_message += se.event_giver(ch, msg)
                elif ch. search_amt >= 0 and ch.location == "새벽녘 마을":
                    compiled_message += se.event_giver(ch, msg)
                else:
                    compiled_message += f"[{ch.name}]은(는) 오늘 사용할 수 있는 서치 기회를 모두 소진했습니다. 내일 또 오세요.\n\n"
    


        
    if compiled_message != "":
        compiled_message = compiled_message[:len(compiled_message)-2]
        await m.channel.send(compiled_message)   



# run client =======================================================================================================================

client.run(TOKEN)




"""

notes=============================





getting channel without a message - through client

channel = discord.utils.get(client.get_all_channels(), guild__name='Neuston', name='조사')

-------------------------------------------------------------------------------------------------------------------------

deconstructing sheet attributes baybey

{'range': 'Sheet2!A4', 'majorDimension': 'ROWS', 'values': [['바닷바람이 불어온다...']]}

------------------------------------------------------------------------------------------------------------------------------
    from the guide for google sheets -- leaving this in just for future reference

    range_name = 'Sheet1!A1:D2'
    
    values = [
        ['a1', 'b1', 'c1', 123],
        ['a2', 'b2', 'c2', 456],
    ]

    data = {
        'values' : values 
    }

    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

--------------------------------------------------------------

    how to properly do update sheet -- you need await in the front

    await update_sheet('B3', [content])

"""










