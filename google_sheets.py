'''

    [google_sheets.py]

    import as sheets
    
    inits everything about sheets

    functions
        - put (s, r, m)
        - get (s, r)
        - flatten (c)
        - get_single (s, r)



'''

# authorization for google sheets =================================================================================================

import httplib2
import pygsheets
import pandas as pd
import os

from apiclient import discovery
from google.oauth2 import service_account

try:
    scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
    secret_file = os.path.join(os.getcwd(), '.client_secret.json')

    spreadsheet_id = '1-_mze5cRMMc5tex04GLgXQVkcGZBNfpgRfcXAG_nVyo'

    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
    service = discovery.build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets().values()
    
   
except OSError as e:
    print(e)


"""

sheetrange

--creates the sheet range for you

@param r -- the sheet range 'A1:B2' or 'A1'

"""
def sheetRange(s, r):

    return s + '!' + r


"""
update & get sheet
-- updates sheets with given m (a list) and s, r for range 
-- gets from sheets with a given range s, r

@param m -- contents in a list form []
s -- sheet name
r -- range name (both in string)

"""

def put(s, r, m):

    values = [m]
    data = { 'values' : values }

    sheet.update(spreadsheetId=spreadsheet_id, body=data, range=sheetRange(s, r), valueInputOption='USER_ENTERED').execute()

def put_multiple(s, r, m):

    values = m
    data = { 'values' : values }

    sheet.update(spreadsheetId=spreadsheet_id, body=data, range=sheetRange(s, r), valueInputOption='USER_ENTERED').execute()

def get(s, r):
    return sheet.get(spreadsheetId=spreadsheet_id, range=sheetRange(s,r)).execute().get('values')

"""
flatten
--flattens array [ [1], [2] ] -> [1, 2]

"""

def flatten(a):
    arr = []
    for little in a:
        for item in little:
            arr.append(item)
    return arr

def get_single(s, r):
    return flatten(get(s, r))[0]

def put_single(s, r, m):
    put(s,r,[m])

def range_calc(cell, num_cells, horizontal):

    calc_range = ""
    
    # parse row and col from cell
    row = -1
    col = -1

    for i in range(len(cell)):
        if cell[i].isnumeric():
            row = cell[i:len(cell)]     # number part
            col = cell[0:i]             # alphabet part
            break

    # horizontal or not
    if not horizontal:
        return cell + ":" + col + str(int(row)+num_cells)

    else:
        new_col = ord(col) + num_cells
        if new_col <= 90: # goes up to z
            return cell + ":" + str(chr(new_col)) + row
        else:
            front_letter = chr(int((new_col-65)/26)+64)
            back_letter = chr(((new_col-65)%26)+64)
            return cell + ":" + str(front_letter) + str(back_letter) + row
            



