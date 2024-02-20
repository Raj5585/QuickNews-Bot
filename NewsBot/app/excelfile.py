# # import csv
csv_file = './excelfiles/Bankkeywords.csv'
Email_csv_file = './excelfiles/emails.csv'


import pandas as pd
def Englishkeywords():
    df = pd.read_csv(csv_file)
    keywords = df['English'].tolist()
   # keywords = ['Ncell','telecommunication' ,'Telecom']
    print(keywords)
    return keywords


def Nepalikeywords():
    df = pd.read_csv(csv_file)
    keywords = df['Nepali'].tolist()
   # keywords = ['Ncell','telecommunication' ,'Telecom']
    print(keywords)
    return keywords

def ReceiverSAddress():
    df = pd.read_csv(Email_csv_file)
    receivers = df['Emails'].tolist()
    return receivers