import urllib.request,json, time, os
from pprint import pprint
from datetime import datetime


def getPosts(user):
    apiUrl = 'https://api.pushshift.io/reddit/search/'

    keyType = {'comment': ('id', 'created_utc', 'subreddit', 'body', 'score', 'full_link', 'url'),
               'submission': ('id', 'created_utc', 'subreddit', 'selftext', 'score', 'full_link', 'url')}
    
    allPosts = {}

    for postType in ['comment', 'submission']:

        before = int(round(time.time()))
        posts = []
        ct = 0
        while True:
            url = f'{apiUrl}{postType}/?author={user}&size=1000&before={before}'            
            req = urllib.request.urlopen(url)
            response =  json.loads(req.read())

            data = response['data']
            
            for i in data:
                validKeys = [ apiKey for apiKey in keyType[postType] if apiKey in i.keys()]
                
                postDict = {}
                for validKey in validKeys:
                    postDict[validKey] = i[validKey]
                
                posts.append(postDict)

                before = postDict['created_utc']
            
            print(f'{postType} list #{ct+1}, containing info on {len(data)} submissions is complete.')
            
            ct = ct+1
            
            if len(data)<1000:
                allPosts[postType] = posts
                break
        print()
                
    return allPosts

def countPosts(allPosts):
    print()

def writeFiles(postDict, user):
    if len(postDict)!=0:
        dateTime = time.strftime("%Y%m%d-%H.%M.%S")

        jname = f'{user}_{dateTime}.json'
        with open(jname, 'w+') as f:
            json.dump(postDict, f, indent=4)        
      
def main():
    #users = input('Enter the path of a line separated .txt containing reddit usernames >> ')
    #users = open(users, 'r').read().splitlines()
    users = open('myUsers.txt', 'r').read().splitlines()
    
    
    for user in users:
        if user=='automoderator':
            continue
        start = time.time()
        
        print('\nGathering posts by ' + user + '.\n')
        
            
        postDic = getSubmissions('markw3456')
        
        writeFiles(postDic, user)
        end = time.time()
        print(f'\n{end-start} seconds to run.')

       
        
        
main()
      


