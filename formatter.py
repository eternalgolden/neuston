"""

    formatter.py

    for all formatting type functions
    returns strings only -- doesn't print anything


    state formatters

    - choice_formatter
    - content_formatter


"""

DIVIDE = ".\t\t--------------\t\t."

def wrong_command(msg):
    global DIVIDE
    return_string = f"[{msg}] <- 명령어나 캐릭터의 이름이 올바르지 않습니다.\n"
    return_string += "혹시 모를 일을 대비해 이 뒤의 명령어는 전부 무효화됩니다. 다시 정확히 써주세요.\n" + DIVIDE + "\n\n" 
    return return_string
 
def choice_formatter(c):

    cs = ""
    for choice in c:
        cs = cs + "\\> " + choice + "\n"
    
    if cs != "":
        cs += "\n\n"
    return cs

def content_formatter(character):
    search_num = character.stats['AQU'] - character.search_count
    cs = (f":mag: 탐색 진행 현황 ({search_num}/{character.stats['AQU']})\n"
          f"> 현재 구역: {character.place.name}\n"
          f"> 인원: {character.name}\n")
    cs += f"{character.state.content}\n"
    cs += choice_formatter(character.state.choices)
    return cs

def content_formatter_plus(character, others, search_count):
    search_num = search_count
    cs = (f":mag: 탐색 진행 현황 ({search_num})\n"
          f"> 현재 구역: {character.place.name}\n"
          f"> 인원: {character.name}")
    
    for c in others:
        if character.name != c.name:
            cs += f", {c.name}"

    cs += f"\n{character.state.content}\n"
    cs += choice_formatter(character.state.choices)
    return cs

def place_formatter(place):
    return f"> 현재 지역: {place.name}\n{place.desc}"

def roll_formatter(aspect, self_stat, filt, self_filt, roll_20, min_succ, succ):
    ret_str = f"> **{aspect}** 판정\n목표: {aspect} {min_succ} | 기본 스탯: {self_stat}\n난이도 보정값: {filt}\n"

    if self_stat >= min_succ:
        ret_str += f"*판정 자동 성공*\n\n"
    else:
        ret_str += f"판정을 진행합니다...\n보정값 : {filt} + 스탯 보정 : {self_filt} + 1D20 : {roll_20}\n최종 판정값: {filt+self_filt+roll_20}"
        if succ:
            ret_str += f" > {min_succ}\n-> 판정 성공 !\n\n"
        else:
            ret_str += f" < {min_succ}\n-> 판정 실패 !\n\n"
    return ret_str

def character_formatter(ch):
    ret = f"**알티 아스테레스 토벌대원 정보**\n\n{ch.name}\t[HP] 00/00\t[SAN] 00/00\t{ch.money} C\nHP 상세▼\n"
    ret += f"[머리] 00/00\t[몸통] 00/00\t[팔] 00/00\t[다리] 00/00\n\n현위치: {ch.place.name}\n"
    #    ret += "[머리] 00/00 [몸통] 00/00 [팔] 00/00 [다리] 00/00\n\n현위치: {ch.place.name} 날씨:날씨\n"
    ret+= f"[TRS] {ch.stats['TRS']}\t[ETH] {ch.stats['ETH']}\t[AQU] {ch.stats['AQU']}\t[KIN] {ch.stats['KIN']}\n\n" 
    # ret += "[디버프][버프]\n"
    ret += "소지품 ▼\n"
    for i,j in ch.bag.items():
        ret += f"{i}({j}), "
    ret = ret[:len(ret)-2]
    return ret

