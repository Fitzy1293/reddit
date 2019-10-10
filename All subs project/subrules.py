import praw
import os
import json
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
        subredditRules = reddit.subreddit(subreddit).rules()['rules']
            
        for subredditRule in subredditRules:
            rulesDict[subreddit].append({subredditRule['short_name'] : subredditRule['description'].strip()})
            
    return rulesDict
    
def writeJson():
    rules = getRules('top_100_subs.txt')
    with open('rules.json', 'w') as f:
        json.dump(rules, f, indent=4, sort_keys=True)
        
    print('Succesfully obtained the rules for ' + str(len(rules)) + ' subreddits.')
    print('File containing the rules is located at the path below.') 
    print(str(os.path.join(os.getcwd(), 'rules.json')))

    os.startfile('rules.json')

if __name__ == '__main__':
    writeJson()
