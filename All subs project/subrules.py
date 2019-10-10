import praw
import prawcore
import os
import json
from time import time
from pprint import pprint
from authenticate import authenticate

reddit = authenticate() #Put your reddit API authentification info here.

def getRules(path):
    with open(path) as f:
        subreddits = f.readlines()
        subreddits = [subreddit.strip() for subreddit in subreddits]

    rulesDict = {}
    for subreddit in subreddits:
        rulesDict[subreddit] = []

        try:
            subredditRules = reddit.subreddit(subreddit).rules()['rules']
        except Exception as e:
            print(e)
            print(subreddit)
            print()
            continue
            
        for subredditRule in subredditRules:
            rulesDict[subreddit].append({subredditRule['short_name'] : subredditRule['description'].strip()})
            
    return rulesDict
    
def writeJson():
    rules = getRules('top_1000_subs.txt') #I have files with 5, 100, and 1000 for testing before trying it on all of them.

    rulesPath = 'top_' + str(len(rules)) + '_rules.json'

    with open(rulesPath, 'w') as f:
        json.dump(rules, f, indent=4, sort_keys=True)
        
    print('Succesfully obtained the rules for ' + str(len(rules)) + ' subreddits.')
    print('File containing the rules is located at the path below.') 
    print(str(os.path.join(os.getcwd(), 'rules.json')))
    print()

    os.startfile(rulesPath)

if __name__ == '__main__':
    start = time()
    writeJson()
    end = time()
    print(str(end-start) + ' seconds.')
