import arxivscraper
import pandas as pd
from gtts import gTTS
import os


def astroph(date):
    language = 'en'
    scraper = arxivscraper.Scraper(category='physics:astro-ph', date_from='2021-12-01',date_until='2021-12-02')
    output = scraper.scrape()
    cols = ('created', 'id', 'title', 'categories', 'abstract', 'authors')
    df = pd.DataFrame(output, columns=cols)
    # print(df)
    new = df[df['created'] >= '2021-11-30']
    # print(new['id'])
    # quit()
    want = new[new['id'] == '2112.00012']
    mytext = want['title'][314] + '. ' + want['abstract'][314]
    print(mytext)
    # quit()
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("astroph.mp3")
    os.system("afplay astroph.mp3")

if __name__ == "__main__":
    astroph()

