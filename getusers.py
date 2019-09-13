import praw
import prawcore
from authenticate import authenticate #Module containing PRAW authentification info
from pprint import pprint             #Put this in the same folder as as this program, or just include it in this module.
import os

reddit = authenticate() #Authenticating reddit, you do can just authenticate it the normal way.
                        #I do this so I don't have to change anything when I update it. 

directory = 'C:\\Users\\' #Directory you want users.txt created in. 

subreddits = open(os.path.join(directory,'topsubs.txt'), 'r').read().splitlines() #Use the topsubs.txt in my reddit repository.
subreddits = [subreddit.split('/')[-1] for subreddit in subreddits if ('/') in subreddit]

userNames = []
for i, subreddit in enumerate(subreddits):
    subreddit = reddit.subreddit(subreddit)

    try:
        for submission in subreddit.hot(limit=None):
            userNames.append(str(submission.author))
        print(str(subreddit))
    except:
        continue

userNames = set([userName for userName in userNames])
print(len(userNames))

users = open(os.path.join(directory,'users.txt'), 'w')
for name in userNames:
    users.write(name + '\n')
users.close()
