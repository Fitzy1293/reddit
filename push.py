import os,urllib.request, json, time
from pprint import pprint
from datetime import datetime


def getIDs(userRangeSeconds, subreddit):
    beforeUTC = int(round(time.time())) 
    userRange = int(round(beforeUTC - userRangeSeconds))

    url = f'https://api.pushshift.io/reddit/search/submission?subreddit={subreddit}&before={beforeUTC}&size={1000}'

    IDs = []
    
    ct = 0
    doneFlag = False
    while True:
        req = urllib.request.urlopen(url)
        response =  json.loads(req.read())
        data = response['data']

        onekIDs = []
        for i in data:
            if i['created_utc'] < userRange:
                doneFlag = True
                break
            else:
                utc = i['created_utc']
                date = str(datetime.utcfromtimestamp(utc))
                
                onekIDs.append({'ID': i['id'],
                                'utc': utc,
                                'date': date,
                                'link': i['full_link']})

        IDs.append(onekIDs)

        print(url)
        print(f'Post list #{ct+1}, containing info on {len(onekIDs)} posts is complete.')
        print(f'{onekIDs[-1]["date"]} is where it is at.')
        print()

        if doneFlag:
            break
        
        else:
            newBefore = onekIDs[-1]['utc']
            url = f'https://api.pushshift.io/reddit/search/submission?subreddit={subreddit}&before={newBefore}&size={1000}'
            ct = ct+1

    postDict = [ID for IDSet in IDs for ID in IDSet]
    postDict.reverse()    
    
    return postDict

def writeFiles(postDict, subreddit):
    if len(postDict)!=0:
        earliestPost = postDict[-1]['utc']
        latestPost = postDict[0]['utc']

        fname = f'{subreddit}_{earliestPost}_{latestPost}.txt'
        with open(fname, 'w+') as f:
            for post in postDict:
                f.write(post['ID'] + '\n')

        jname = f'{subreddit}_{earliestPost}_{latestPost}.json'
        with open(jname, 'w+') as f:
            json.dump(postDict, f, indent=4, sort_keys=True)

        print(f'{len(postDict)} IDs retrieved.')

        os.startfile(jname)

def main():
    subreddit = input('Enter a subreddit >> ')
    
    print('\nNow enter a time range.')
    
    years = int(input('\nYears  >> '))
    weeks = int(input('Weeks  >> '))
    days = int(input('Days  >> '))
    hours = int(input('Hours  >> '))
    minutes = int(input('Minutes  >> '))

    userRangeSeconds =  years*365*86400 + weeks*7*86400 + days*3600*24 + hours*3600 + minutes*60
    
    print('\nGathering posts.')
    
    validDict = getIDs(userRangeSeconds, subreddit)
    
    writeFiles(validDict, subreddit)
        
main()
            
