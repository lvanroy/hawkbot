import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import asyncio

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1bMQz0UdDuLjCz_SLSy6VnuD3V8HOFAMTt2xTrGuk7SU'
RANGE = 'A1:C1000'

COLUMNS = ['Family name', 'Current activity', 'Past activity']


class Activity:
    def __init__(self):
        self.df = None

        self.update_df()

    def update_df(self):
        cred = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                cred = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(cred, token)

        service = build('sheets', 'v4', credentials=cred)

        sheet = service.spreadsheets()
        result_input = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
        values_input = result_input.get('values', [])

        if not values_input:
            print('No data found.')

        self.df = pd.DataFrame(values_input[1:], columns=values_input[0])
        self.df['Family name'] = self.df['Family name'].astype(str)
        self.df['Current activity'] = self.df['Current activity'].astype(int)
        self.df['Past activity'] = self.df['Past activity'].astype(int)

    def write_df(self):
        cred = None
        self.df = self.df.sort_values(['Family name'])

        if os.path.exists('token_write.pickle'):
            with open('token_write.pickle', 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                cred = flow.run_local_server(port=0)

            with open('token_write.pickle', 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build('sheets', 'v4', credentials=cred)
            service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                valueInputOption='RAW',
                range=RANGE,
                body=dict(
                    majorDimension='ROWS',
                    values=self.df.T.reset_index().T.values.tolist()
                )
            ).execute()
            print('Sheet successfully updated')
        except Exception as e:
            print(e)

    def compute_payout_values(self):
        min_act = None
        max_act = None
            
        for _, row in self.df.iterrows():
            dif = row['Current activity'] - row['Past activity']
            if min_act is None:
                min_act = dif
                max_act = dif
            if dif < min_act:
                min_act = dif
            if dif > max_act:
                max_act = dif
        
        output = ""
        for _, row in self.df.iterrows():
            dif = int(row['Current activity']) - int(row['Past activity'])
            if min_act != max_act:
                if dif < 0.05 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 1)
                elif dif < 0.1 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 2)
                elif dif < 0.2 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 3)
                elif dif < 0.3 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 4)
                elif dif < 0.4 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 5)
                elif dif < 0.5 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 6)
                elif dif < 0.6 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 7)
                elif dif < 0.7 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 8)
                elif dif < 0.8 * max_act:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 9)
                else:
                    output += "{} gained {}, level {}\n".format(row['Family name'], dif, 10)
            else:
                output += "{} gained {}, level {}\n".format(row['Family name'], dif, 1)

        return output

    def add_activity(self, family, current_activity, channel):
        if family not in self.df['Family name'].tolist():
            self.df = self.df.append(
                pd.DataFrame([[family, current_activity, current_activity]], columns=COLUMNS),
                ignore_index=True
            )
            self.write_df()
        else:
            asyncio.ensure_future(channel.send('Error: this family already exists'))

    def register_renewal(self, family, current_activity, channel):
        if family in self.df['Family name'].tolist():
            self.df.loc[(self.df['Family name'] == family)].replace(
                {
                    int(self.df.loc[(self.df['Family name'] == family)]['Past activity']): current_activity
                }
            )
            self.write_df()
        else:
            asyncio.ensure_future(channel.send('Error: this family does not exist'))

    def reset_tracker(self):
        self.df['Past activity'] = self.df['Current activity']
        self.write_df()
