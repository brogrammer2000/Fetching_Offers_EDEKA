# Managing imports
import requests
import json
import csv
import os
import pandas as pd
import numpy as np
from io import StringIO
import unicodedata

CWD = os.getcwd()
# creates the 'data' directory in the CWD
#os.makedirs("json_data", mode=0o777, exist_ok=True)

# intitializing required variables
market_dictionary = {}
market_ids = []
specials = ["Ã", "*", "¼", "Ã", "¤", "Ã", "¶"]

# function to clean accents from the data


def strip_accents(column):
    if column == "ä" or column == 'ü' or column == 'ö' or column == 'ß' or column == 'éè':
        return column
    else:
        return ''.join(c for c in unicodedata.normalize('NFD', column)
                       if unicodedata.category(c) != 'Mn')


# creating the arrays to loop through
search_terms = ["Löhne", "Herford-Deichkamp", "Bünde", "Espelkamp", "Minden",
                "Porta-Westfalica", "Belm", "Rinteln", "Bad Salzuflen", "Hameln-Wangelist"]
market_names = ["Marktkauf Löhne", "Marktkauf Herford", "Marktkauf Bünde", "Marktkauf Espelkamp", "EDEKA Center Minden",
                "EDEKA Center Porta Westfalica", "Marktkauf Belm", "Marktkauf Rinteln", "Marktkauf Bad Salzuflen", "Marktkauf Hameln-Wangelist"]

# working of the script
for (i, j) in zip(search_terms, market_names):  # loops through both the collections
    # making the API call
    req = requests.get(
        f"https://www.edeka.de/api/marketsearch/markets?searchstring={i}")
    data = req.json()  # converting from response to json
    if data['markets'][0]['name'] == j or data['markets'][1]['name'] == j or data['markets'][2]['name'] == j or data['markets'][4]['name'] == j:  # selecting the desired market
        # appending the market dictionary
        market_dictionary[j] = data['markets'][0]['id']

# appending market ids to the array
market_ids = list(market_dictionary.values())

for (x, y) in zip(market_ids, market_dictionary):  # looping through both the collections
    # making the API call
    res = requests.get(
        f"https://www.edeka.de/eh/service/eh/offers?marketId={x}&limit=99999")

    content = res.content  # getting the JSON data content

    '''cleaning = json.loads(content)
    cleaning = str(cleaning)
    cleaning.replace('ä', 'ae').replace('Ã¼', 'ue').replace('Ã¶', 'oe').replace('ÃŸ', 'ss').replace('Ã©Ã¨', 'e')
    cleaning = json.dumps(cleaning)'''

    with open(f"{y}.json", 'wb') as file:  # opening the file
        file.write(content)

'''for y in market_dictionary:
    with open(f"{y}.json", 'r+') as newfile:
        stuff = newfile.read()
        newfile.seek(0)
        stuff.replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('ß', 'ss').replace('éè', 'e')
        newfile.write(stuff)'''


# Code for JSON to CSV
for (m, n) in zip(market_dictionary, range(1, 11)):
    with open(f"{m}.json") as file:
        data = json.load(file)
    globals()[f"df{n}"] = pd.DataFrame(data['docs'])
    #globals()[f"df{n}"]['market_name'] = f"{m}"
#"Marktkauf Löhne", "Marktkauf Herford", "Marktkauf Bünde", "Marktkauf Espelkamp", "EDEKA Center Minden",
    # "EDEKA Center Porta Westfalica", "Marktkauf Belm", "Marktkauf Rinteln", "Marktkauf Bad Salzuflen", "Marktkauf Hameln-Wangelist"]'''
'''df1 = df1.append({'angebotid:': "Marktkauf Löhne"}, ignore_index = True)
df2 = df2.append({'angebotid:': "Marktkauf Herford"}, ignore_index = True)
df3 = df3.append({'angebotid:': "Marktkauf Bünde"}, ignore_index = True)
df4 = df4.append({'angebotid:': "Marktkauf Espelkamp"}, ignore_index = True)
df5 = df5.append({'angebotid:': "EDEKA Center Minden"}, ignore_index = True)
df6 = df6.append({'angebotid:': "EDEKA Center Porta Westfalica"}, ignore_index = True)
df7 = df7.append({'angebotid:':  "Marktkauf Belm"}, ignore_index = True)
df8 = df8.append({'angebotid:': "Marktkauf Rinteln"}, ignore_index = True)
df9 = df9.append({'angebotid:': "Marktkauf Bad Salzuflen"}, ignore_index = True)
df10 = df10.append({'angebotid:': "Marktkauf Hameln-Wangelist"}, ignore_index = True)'''

#df1.insert(0, "angebotid","Marktkauf Löhne")
'''with open("Marktkauf Löhne.json") as file1:
    data1 = json.load(file1)
df1 = pd.DataFrame(data1['docs'])
df1 = df1.append({'angebotid': 'Marktkauf Löhne'}, ignore_index = True)

with open("Marktkauf Herford.json") as file2:
    data2 = json.load(file2)
df2 = pd.DataFrame(data2['docs'])
df2 = df2.append({'angebotid': 'Marktkauf Herford'}, ignore_index = True)


with open("Marktkauf Bünde.json") as file3:
    data3 = json.load(file3)
df3 = pd.DataFrame(data3['docs'])
df3 = df3.append({'angebotid': 'Marktkauf Bünde'}, ignore_index = True)


with open("Marktkauf Espelkamp.json") as file4:
    data4 = json.load(file4)
df4 = pd.DataFrame(data4['docs'])
df4 = df4.append({'angebotid': 'Marktkauf Espelkamp'}, ignore_index = True)


with open("EDEKA Center Minden.json") as file5:
    data5 = json.load(file5)
df5 = pd.DataFrame(data5['docs'])
df5 = df5.append({'angebotid': 'EDEKA Center Minden'}, ignore_index = True)


with open("EDEKA Center Porta Westfalica.json") as file6:
    data6 = json.load(file6)
df6 = pd.DataFrame(data6['docs'])
df6 = df6.append({'angebotid': 'EDEKA Center Porta Westfalica'}, ignore_index = True)


with open("Marktkauf Belm.json") as file7:
    data7 = json.load(file7)
df7 = pd.DataFrame(data7['docs'])
df7 = df7.append({'angebotid': 'Marktkauf Belm'}, ignore_index = True)


with open("Marktkauf Rinteln.json") as file8:
    data8 = json.load(file8)
df8 = pd.DataFrame(data8['docs'])
df8 = df8.append({'angebotid': 'Marktkauf Rinteln'}, ignore_index = True)


with open("Marktkauf Bad Salzuflen.json") as file9:
    data9 = json.load(file9)
df9 = pd.DataFrame(data9['docs'])
df9 = df9.append({'angebotid': 'Marktkauf Bad Salzuflen'}, ignore_index = True)


with open("Marktkauf Hameln-Wangelist.json") as file10:
    data10 = json.load(file10)
df10 = pd.DataFrame(data10['docs'])
df10 = df10.append({'angebotid': 'Marktkauf Hameln-Wangelist'}, ignore_index = True)'''


df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10])

#df.to_csv("EDEKA_Offers_Raw.csv", index=False)
#cleaned_df = df[["angebotid", "titel", "preis", "beschreibung", "basicPrice"]]
#df[["angebotid", "titel", "preis", "beschreibung", "basicPrice"]] = df[["angebotid", "titel", "preis", "beschreibung", "basicPrice"]].str.replace('Ã¤', 'ae').replace('Ã¼', 'ue').replace('Ã¶', 'oe').replace('ÃŸ', 'ss').replace('Ã©Ã¨', 'e')
#df['titel'] = df['titel'].str.replace('Ã¤', 'ae').replace('Ã¼', 'ue').replace('Ã¶', 'oe').replace('ÃŸ', 'ss').replace('Ã©Ã¨', 'e')
#df["beschreibung"] = df["beschreibung"].str.replace('Ã¤', 'ae').replace('Ã¼', 'ue').replace('Ã¶', 'oe').replace('ÃŸ', 'ss').replace('Ã©Ã¨', 'e')
df_cleaned = df[["angebotid", "titel", "preis",
                 "beschreibung", "basicPrice"]].copy()
df_cleaned['titel'] = df_cleaned['titel'].apply(strip_accents)
df_cleaned['beschreibung'] = df_cleaned['beschreibung'].apply(strip_accents)
df_cleaned.to_csv('testing.csv', index=False)

df_new = pd.read_csv('testing.csv')

df_new['titel'] = df_new['titel'].str.replace('A¤', 'ae', regex=True).replace('A¼', 'ue', regex=True).replace('A¶', 'oe', regex=True).replace('AY', 'ss', regex=True).replace(
    'A©A¨', 'e', regex=True).replace('^[A-Z0-9]+((,\s|-)[A-Z0-9]+)*[A-Z0-9]+$', '', regex=True).replace('œ', 'oe', regex=True).replace('â€', 'oe', regex=True)
df_new['beschreibung'] = df_new['beschreibung'].str.replace('A¤', 'ae', regex=True).replace('A¼', 'ue', regex=True).replace('A¶', 'oe', regex=True).replace(
    'AY', 'ss', regex=True).replace('A©A¨', 'e', regex=True).replace('^[A-Z0-9]+((,\s|-)[A-Z0-9]+)*[A-Z0-9]+$', '', regex=True).replace('œ', 'oe', regex=True).replace('â€', 'oe', regex=True)

df_new.to_csv('EDEKA_Offers.csv', index=False)

#dfstr = df_new.to_string().replace('Ã¤', 'ae').replace('Ã¼', 'ue').replace('Ã¶', 'oe').replace('ÃŸ', 'ss').replace('Ã©Ã¨', 'e')
#df_final = pd.read_csv(StringIO(dfstr), sep='\s+')
#dfstr.to_csv("EDEKA_Offers_Processed.csv", index=False)
# print(dfstr)
#final_df = pd.read_csv(StringIO(df_new))
# final_df.to_csv('EDEKA_Offers.csv')

'''# Code for Cleaning the scraped data.
# opening the file to be read and the file to be written to
with open(f"EDEKA_Offers_Processed.csv", "r") as infile, open("EDEKA_Offers_Cleaned.csv", "w") as outfile:
    reader = csv.reader(infile)  # creating the csv reader obj
    writer = csv.writer(outfile)  # creating the csv writer obj
    # setting the special characters to be excluded
    conversion = set("Ã*¼Ã¤Ã¶Âƒ")
    for row in reader:  # looping throw all the rows found in the input file
        newrow = [''.join('' if c in conversion else c for c in entry)
                  for entry in row]  # excluding the characters found
        writer.writerow(newrow)  # writing the data to the file.
'''
# Deleting the unwanted files
for m in market_dictionary:
    os.remove(f"{m}.json")
# os.remove("EDEKA_Offers_Processed.csv")
os.remove("testing.csv")
