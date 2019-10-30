import urllib.request,json, time, os
from pprint import pprint


def getPosts(user):
    apiUrl = 'https://api.pushshift.io/reddit/search/'

    keyType = {'comment': ('id', 'created_utc', 'subreddit', 'body', 'score', 'permalink'),
               'submission': ('id', 'created_utc', 'subreddit', 'selftext', 'score', 'full_link', 'url')}
    
    allPosts = {}
    for postType in ['comment', 'submission']:
        before = int(round(time.time()))
        
        posts = []
        ct = 0

        while True: 
            url = f'{apiUrl}{postType}/?author={user}&size=2000&before={before}'            
            req = urllib.request.urlopen(url)
            response =  json.loads(req.read())
            data = response['data']
            
            for i in data:
                ourKeys = keyType[postType]
                apiKeys = i.keys()

                postDict = dict.fromkeys(ourKeys, None)
                for key in ourKeys:
                    if key in ourKeys and key in apiKeys:
                        postDict[key] = i[key]

                posts.append(postDict)

            before = posts[-1]['created_utc']

            capitalPost = postType[0].capitalize() + postType[1:]
            log = f'{" " * 4}- {capitalPost} request #{ct+1}, for {len(data)} {postType}(s) completed.'
            print(log)
            
            ct = ct+1
            
            if len(data)<1000:
                allPosts[postType] = posts
                print()
                break

    for i in allPosts['comment']:
        if i['permalink'] is not None:
            emptyLink = i['permalink']
            i['permalink'] = 'https://www.reddit.com' + emptyLink #Strange how this is different between comments and submissions.
    
    return allPosts

def countPosts(allPosts):
    postCounts = {}
    for postType, posts in allPosts.items():
        subreddits = [post['subreddit'] for post in posts]
        subredditSet = set(subreddits)

        counts = {}
        for subreddit in subredditSet:
            counts[subreddit] = subreddits.count(subreddit)
        
        sortedCounts = sorted(counts.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)
            

        postCounts[postType + 'Count'] = sortedCounts
        
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
        with open(jPath, 'w+') as f:
            json.dump(allPosts, f, indent=6)

        cFname = f'{user}_{newUtc} subreddit_count.json'
        cPath = os.path.join(userDir, cFname) 
        with open(cPath, 'w+') as g:
            json.dump(postCounts, g, indent=4)

        for fname in os.listdir(userDir):
            oldFname = os.path.join(userDir, fname)
            if oldFname not in (jPath, cPath):
                os.remove(oldFname)
    
def main():
    userIn = input('Enter a subreddit or the path of a line separated .txt containing reddit usernames >> ')
    print()
    
    if userIn.endswith('.txt'):
        users = open(userIn, 'r').read().splitlines()
        users = [i for i in users if not i.lower()=='automoderator']
    else:
        users = [userIn.lower()] #Just to use within the loop.
    
    #users = open('myUsers.txt', 'r').read().splitlines()

    print('='*100)
    for i, user in enumerate(users):
        start = time.time()
        
        print(f'{user} - User {i+1} of {len(users)}.')
        print(f'Gathering posts.')
        print()

        allPosts = getPosts(user)
        
        print(f'{len(allPosts["comment"])} comment(s).')
        print(f'{len(allPosts["submission"])} submission(s).')
        print()

        counts = countPosts(allPosts)
    
        writeFiles(allPosts, counts, user)

        end = time.time()
        print(f'{end-start} seconds.')
        print('='*100)    
        
main()
