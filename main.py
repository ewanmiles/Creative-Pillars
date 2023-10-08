import os, json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import eel

eel.init("web")

SHEETS_DIR = 'sheets'
SHEETS_REF = {}
URL_REF = ["Instagram URL", "Facebook permalink", "Tweet permalink"]
ER_REF = ["Engagement on reach", "engagement rate"]

def selectAndImport(platform):
    """
    Takes the selected platform and imports the correct spreadsheet for labelling; input

        - platform (str): Should be one of Instagram, Facebook, X, X sport.
    """
    if platform in SHEETS_REF.keys():
        print("Fetching from reference sheets")
        
        return SHEETS_REF[platform]

    else:
        assert platform in ['Instagram', 'Facebook', 'X', 'X sport'], f"Unrecognised platform: {platform}"
        fileName = f"{platform.lower().replace(' ','_')}.csv"

        print("Fetching from filesystem")

        df = pd.read_csv(os.path.join(SHEETS_DIR, fileName))
        df = df.rename(columns={f'{list(df.columns.intersection(URL_REF))[0]}':'URL'})
        df = df.rename(columns={f'{list(df.columns.intersection(ER_REF))[0]}':'ER'})
        df["Label"] = ""

        saveChanges(platform, df)

        return df

def saveChanges(key, df):
    """
    Simple function to save any dataframe changes to the reference dictionary; inputs

        - key (str): Key in SHEETS_REF dict to save to
        - df (Pandas DataFrame): Updated DF to save to key

    No outputs.
    """
    SHEETS_REF[key] = df

@eel.expose
def loadFirstPost(platform):
    """
    YADA YADA YADA
    """
    df = selectAndImport(platform)

    firstPostURL = df["URL"][0]
    firstPostCaption = df["Caption"][0]
    eel.loadInContent(firstPostCaption, firstPostURL)

@eel.expose
def loadPostIndex(platform, ind):
    """
    YADA YADA YADA
    """
    df = selectAndImport(platform)
    actualIndex = ind % (len(df)-1)

    eel.loadInContent(
        df["Caption"][actualIndex],
        df["URL"][actualIndex],
        df["Label"][actualIndex]
    )

@eel.expose
def py_labelPost(platform, ind, label):
    """
    YADA YADA YADA
    """
    df = SHEETS_REF[platform]
    df.at[ind % (len(df)-1), "Label"] = label

@eel.expose
def exportSheet(platform):
    """
    YADA YADA YADA
    """
    fileName = f"{platform.lower().replace(' ','_')}_labelled.csv"
    SHEETS_REF[platform].to_csv(os.path.join(SHEETS_DIR, fileName))

@eel.expose
def calculateRates(platform):
    """
    YADA YADA YADA
    """
    df = SHEETS_REF[platform]
    uniqueLabels = df['Label'].unique()
    results = dict.fromkeys(uniqueLabels, 0)

    for i in uniqueLabels:
        rates = [j for j in list(df.loc[df["Label"] == i]["ER"]) if str(j) != 'nan']
        results[i] = np.mean([float(i.strip('%')) for i in rates])

    with open('colors.json','r') as f:
        colDict = json.load(f)

    data = []
    for i in results.keys():
        data.append((
            360*results[i]/sum(results.values()), #Degrees on pie
            f"{results[i]:0.2f}%", #Label percentage
            colDict[i], #Colour by label
            i)) #Label

    plt.figure()
    wedges, texts = plt.pie([i[0] for i in data], startangle=90, labels=[i[1] for i in data], colors=[i[2] for i in data])

    plt.legend(wedges, [i[3] for i in data], loc='center right', bbox_to_anchor=(1.5, 0.5), ncol=1)
    plt.tight_layout()

    plt.show()

eel.start("index.html", size=(800,850))