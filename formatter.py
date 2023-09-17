"""

    formatter.py

    for all formatting type functions
    returns strings only -- doesn't print anything


    state formatters

    - choice_formatter
    - content_formatter


"""


def choice_formatter(c):

    cs = ""
    for choice in c:
        cs = cs + "\\> " + choice + "\n"
    
    if cs != "":
        cs += "\n\n"
    return cs

def content_formatter(character, isContent):
    search_num = 5-character.search_count
    cs = (f":mag: 탐색 진행 현황 ({search_num}/5)\n"
          f"> 현재 구역: {character.location}\n"
          f"> 인원: {character.name}\n")
    if isContent:
        cs += f"{character.state.content}\n"
        cs += choice_formatter(character.state.choices)
    return cs

def place_formatter(place):
    return f"> 현재 지역: {place.name}\n> {place.desc}"


