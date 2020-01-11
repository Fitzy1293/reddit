import urllib.request
import json
import time
import os
from pprint import pprint

def getPosts(user):
    
    apiUrl = 'https://api.pushshift.io/reddit/search/'

    keyType = {'comment': ('id', 'created_utc', 'subreddit', 'body', 'score', 'permalink'),
               'submission': ('id', 'created_utc', 'subreddit', 'selftext', 'score', 'full_link', 'url')}
    
    allPosts = {}
    for postType in ['comment', 'submission']:
        before = int(round(time.time()))

        print(postType[0].capitalize() + postType[1:] + ' request log')
        
        ct = 0
        posts = []
        while True: 
            url = f'{apiUrl}{postType}/?author={user}&size=1000&before={before}'            
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())['data']
            
            for i in data:
                ourKeys = keyType[postType]
                apiKeys = i.keys()

                
                postDict = dict.fromkeys(ourKeys, None)
                for key in ourKeys:
                    if key in ourKeys and key in apiKeys:
                        postDict[key] = i[key]
                postDict['postType'] = postType
                        
                posts.append(postDict)
                
            if len(posts)!=0:
                before = posts[-1]['created_utc']

            
            log = f'#{ct+1} - {len(data)} completed.'
            print('\t' + log)
            ct = ct+1

            if len(data)<1000:
                allPosts[postType + 's'] = posts
                print()
                break
            
    return allPosts

def countPosts(allPosts):
    postCounts = {}
    for postType, posts in allPosts.items():
        subreddits = [post['subreddit'] for post in posts]
        subredditSet = set(subreddits)

        counts = {}
        for subreddit in subredditSet:
            if subreddit is not None:
                counts[subreddit] = subreddits.count(subreddit)
        
        sortedCounts = sorted(counts.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)

        postCounts[postType] = sortedCounts
        
    return postCounts
            
def writeFiles(allPosts, postCounts, user):
    usersDir = os.path.join(os.getcwd(), 'users') #New folder containing a folder for each user. 
    if not os.path.exists(usersDir):
        os.mkdir(usersDir)
        
    userDir = os.path.join(usersDir, user) #New folder containing a folder for each user. 
    if not os.path.exists(userDir):
        os.mkdir(userDir)
    
    if len(allPosts)!=0:
        newUtc = int(round(time.time()))

        jFname = f'{user}_{newUtc} user_info.json'
        jPath = os.path.join(userDir, jFname)
        with open(jPath, 'w+', newline='\n') as f:
            json.dump(allPosts, f, indent=4)
            
        cFname = f'{user}_{newUtc} subreddit_count.txt'
        cPath = os.path.join(userDir, cFname) 
        with open(cPath, 'w+') as g:
            for k,v in postCounts.items():
                postType = k[0].upper() + k[1:]
                g.write(postType + '\n')
                for i in v:
                    g.write('\t' + i[0] + ': ' + str(i[1]) + '\n')
                    
        for fname in os.listdir(userDir):
            oldFname = os.path.join(userDir, fname)
            if oldFname not in (jPath, cPath):
                os.remove(oldFname)
    
def main():
    
    print('A = Line separated .txt containing reddit usernames ')
    print('B =  reddit username')
    userIn = input('\n\tChoose option A or B >> ')
    
    if userIn.upper()=='A':
        usersPath = input('\tPath >> ')
        users = open(usersPath, 'r').read().splitlines()
        users = [i for i in users if not i.lower()=='automoderator']
    elif userIn.upper()=='B':
        user = input('\tUser >> ')
        users = [user.lower()] #Just to use within the loop.
    else:
        print('Enter valid input')
    
    #users = open('myUsers.txt', 'r').read().splitlines()

    print('='*100)
    for i, user in enumerate(users):
        if user=='automoderator':
            continue
        
        start = time.time()
        
        print(f'{user} - User {i+1} of {len(users)}.')
        print()

        allPosts = getPosts(user)
        
        print(f'Comments = {len(allPosts["comments"])}')
        print(f'Submissions = {len(allPosts["submissions"])}')
        print()

        counts = countPosts(allPosts)
    
        writeFiles(allPosts, counts, user)
        
        totalTime = round(time.time() - start, 1)
        print(f'{totalTime} seconds.')
        print('='*100)    
        
main()
