'''
    helper.py

    has a bunch of helper functions
    that don't belong anywhere particularly

'''



def parse_place(msg):
    new_place = None
    mm = msg.split("-")[1]

    if mm == "새벽녘마을":
        new_place = places['dawn']
    elif mm  == "본부":
        new_place = places['hq']

    return new_place

