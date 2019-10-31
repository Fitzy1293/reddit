import urllib.request,json, time, os, csv, io
from pprint import pprint
import pandas as pd 


apiUrl = 'https://api.pushshift.io/reddit/search'
subreddit = 'nosleep'

minScore = 5 #Minimum karma of posts we get &score>={minScore}.

before = int(round(time.time()))
ct = 0
posts = []
with io.open('nosleep posts.txt', 'w+', encoding='utf-8') as f:
    while True: 
        url = f'{apiUrl}/submission/?subreddit={subreddit}&before={before}&size=50'
        req = urllib.request.urlopen(url)
        data =  json.loads(req.read())['data']

        f.write('='*50 + '\n')
        for submission in data:
            if 'title' in submission.keys() and 'selftext' in submission.keys():
                if submission['selftext']== '[removed]':
                    continue
                
                title = submission['title'].strip()
                
                text = submission['selftext'].replace('&amp;#x200B','')
                text = text.split('\n')
                text = [i.strip() for i in text if i!=';']

                text = '\n\t' + '\n\t'.join(text)
        
                
                f.write(title + '\n\n')
                f.write(submission['url']+ '\n\n')
                f.write(text+ '\n')
                f.write('='*50 + '\n')
                
             
                posts.append([title, text])
                ct = ct + 1

        break
        before = data[-1]['created_utc']

os.startfile('nosleep posts.txt')
