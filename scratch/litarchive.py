#litarchive.py
import urllib.request,json, time, os, csv
from pprint import pprint

apiUrl = 'https://api.pushshift.io/reddit/search'
subreddit = 'nosleep'
ourKeys = ('title', 'selftext')

minScore = 5 #Minimum karma of posts we get &score>={minScore}.

before = int(round(time.time()))
ct = 0
posts = []
while True: 
    url = f'{apiUrl}/submission/?before={before}&subreddit={subreddit}&size=20'
    req = urllib.request.urlopen(url)
    data =  json.loads(req.read())['data']

    
    for submission in data:
        if 'title' in submission.keys() and 'selftext' in submission.keys():
            if '&amp;#x200B;' in submission['selftext']:
                text = submission['selftext'].replace('&amp;#x200B;', '')
            else:
                text = submission['selftext']
            
                
            posts.append((submission['title'], text))
            ct = ct + 1
            
    break
    before = data[-1]['created_utc']

print(len(posts))
fname = 'nosleep posts' + str(time.time()) + '.csv'
f = open(fname, mode='w+', newline='', encoding='utf-8-sig')
    
writer = csv.writer(f)
    
writer.writerow(['Title', 'Post Text'])
for post in posts:
    writer.writerow(post)
f.close()

os.startfile(fname)
'
