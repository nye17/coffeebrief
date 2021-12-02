# 02 Dec 2021 15:32:14
# Written by Ying ZU (yingzu@sjtu.edu.cn).
import arxivscraper
import pandas as pd
from gtts import gTTS
import os, sys
import datetime
import requests
requests.packages.urllib3.disable_warnings()
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


""" Scrape arXiv for astro-ph papers that were submitted within the past N days.
"""

def astroph(nlastdays=1, txtout='coffeebrief_script.txt', mp3out='coffeebrief_audio.mp3', cats=['ga', 'co', 'sr', 'ep']):
    """
    nlastdays: integer (optional)
        How many days since the last date did you listen to the coffee brief? Shame! Shame! Shame! (default: 1)
    txtout: str (optional)
        txt filename for the script.
    mp3out: str (optional)
        mp3 filename for the audio.
    cats: list (optional)
        the astro-ph subcategories that you want.
    """
    tod = datetime.datetime.now()
    dd0 = datetime.timedelta(days=(nlastdays+1))
    dd1 = datetime.timedelta(days=nlastdays)
    d0 = (tod-dd0).strftime('%Y-%m-%d')
    d1 = (tod-dd1).strftime('%Y-%m-%d')
    d2 = tod.strftime('%Y-%m-%d')
    language = 'en'
    scraper = arxivscraper.Scraper(category='physics:astro-ph', date_from=d1,date_until=d2)
    output = scraper.scrape()
    cols = ('created', 'id', 'title', 'categories', 'abstract', 'authors')
    df = pd.DataFrame(output, columns=cols)
    new = df[df['created'] >= d0]
    text = ''
    npaper = 0
    for row in new.itertuples(index=False):
        adopted = False
        shelter = row.categories.split(" ")
        for cat in shelter:
            if cat[9:] in cats:
                adopted = True
                npaper += 1
        if adopted:
            mytext = 'Title: ' + row.title + '.\n Submitted by ' + row.authors[0] + ' et al.\n ' + row.abstract + '\n\n'
            text += mytext
        if npaper >= 1:
            break
    print(npaper)
    if txtout:
        print("exporting script to txt file")
        with open(txtout, 'w') as f:
            f.write(text)
    if mp3out:
        print("exporting audio to mp3 file")
        myobj = gTTS(text=text, lang=language, slow=False)
        myobj.save(mp3out)
        # os.system("afplay astroph.mp3")
    return()

if __name__ == "__main__":
    try:
        n = int(sys.argv[1])
    except IndexError:
        print("Usage: python brief.py nlastdays")
        quit()
    astroph(n, cats=['co'])
