import urllib.request,json, time, os
from pprint import pprint
from datetime import datetime

def getComments(user):
    author = user
    url = f'https://api.pushshift.io/reddit/search/comment/?author={author}&size=1000'
    
    IDs = []
    ct = 0
    while True:
        req = urllib.request.urlopen(url)
        response =  json.loads(req.read())
        data = response['data']

        onekIDs = []
        for i in data:
            commentDict = ({'ID': i['id'],
                            'type': 'comment',
                            'subreddit': i['subreddit'],
                            'utc': i['created_utc'],
                            'date': str(datetime.utcfromtimestamp(i['created_utc'])),
                            'body': i['body']})
                            
            
            if 'permalink' in i.keys():
                commentDict['link'] = 'https://www.reddit.com' + i['permalink']
            
            onekIDs.append(commentDict)
    
        IDs.append(onekIDs)
        if len(onekIDs)==0:
            break
        
        print(url)
        print(f'Comment list #{ct+1}, containing info on {len(onekIDs)} comments is complete.')
        print()
        
        newBefore = onekIDs[-1]['utc']
        url = f'https://api.pushshift.io/reddit/search/comment/?author={author}&size=1000&before={newBefore}'
        ct = ct+1

    postDict = [ID for IDSet in IDs for ID in IDSet]
    postDict.reverse()    
    
    return postDict

def getSubmissions(user):
    author = user
    url = f'https://api.pushshift.io/reddit/search/submission/?author={author}&size=1000'
    
    IDs = []
    ct = 0
    while True:
        req = urllib.request.urlopen(url)
        response =  json.loads(req.read())
        data = response['data']

        onekIDs = []
        for i in data:
            submissionDict = ({'ID': i['id'],
                               'type': 'submission',
                               
                               'utc': i['created_utc'],
                               'date': str(datetime.utcfromtimestamp(i['created_utc']))})
            
            if 'permalink' in i.keys():
                submissionDict['link'] = 'https://www.reddit.com' + i['permalink']
            if 'subreddit' in i.keys():
                submissionDict['subreddit'] = i['subreddit']

            onekIDs.append(submissionDict)
    
        IDs.append(onekIDs)

        if len(onekIDs)==0:
            break
        
        print(url)
        print(f'Submission list #{ct+1}, containing info on {len(onekIDs)} submissions is complete.')
        print()
        
        newBefore = onekIDs[-1]['utc']
        url = f'https://api.pushshift.io/reddit/search/submission/?author={author}&size=1000&before={newBefore}'
        ct = ct+1

    postDict = [ID for IDSet in IDs for ID in IDSet]
    postDict.reverse()    
    
    return postDict

def writeFiles(postDict, user):
    if len(postDict)!=0:
        earliestPost = postDict[-1]['utc']
        latestPost = postDict[0]['utc']

        jname = f'{user}_posts.json'
        with open(jname, 'w+') as f:
            json.dump(postDict, f, indent=4, sort_keys=True)

        print(f'{len(postDict)} IDs retrieved.')

def main():
    users = input('Enter the path of a line separated .txt containing reddit usernames >> ')
    users = open(users, 'r').read().splitlines()
    #users = open('random users.txt', 'r').read().splitlines()
    
    for user in users:
        start = time.time()
        try:
            print('\nGathering comments by ' + user + '.\n')
            comments = getComments(user)
            
            print('\nGathering submissions by '+ user + '\n.')
            submissions = getSubmissions(user)

            postDic = submissions + comments
      
            writeFiles(postDic, user)
            end = time.time()
            print(f'\n{end-start} seconds to run.')

        except:
            continue
        
main()
            


