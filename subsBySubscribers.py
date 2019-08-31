from lxml import html, etree
import requests
from pprint import pprint
import os

def getSubs(url):
    page = requests.get(url)
    htmlContent = html.fromstring(page.content)

    body = htmlContent[1] 
    body = etree.tostring(body)
    body = body.decode('UTF-8') #Decode bitecode into a string.
    body = body.split('\n')
    body = [line for line in body if '<td class="tod"' in line] #'<td class="tod"' is where the info about the subs is. 

    subredditInfo = [] #2D list, 3 attributes in inner lists - Rank, Subreddit URL and sub count.
    for i in range(0, len(body), 3):
        subredditInfo.append(body[i:i+3])  

    formatSubreddit = []
    for subreddit in subredditInfo:
        formatAttribute = []
        for j, attribute in enumerate(subreddit): #Probably not the correct way to parse this but whatever.
            if j==0:
                rank = attribute.split('>')[-2]
                rank = rank.split('<')[0]
                formatAttribute.append(rank)
            if j==1:
                try:
                    sub = attribute.split('</a></td>')[-2]
                    sub = sub.split('>')[-1]
                    formatAttribute.append('\thttps://www.reddit.com' + sub)
                except IndexError:
                    print(attribute)
            if j ==2:
                subscribers = attribute.split('</td>')[-2]
                subscribers = subscribers.split('>')[-1]
                formatAttribute.append('\t' + subscribers)
                
        formatSubreddit.append(''.join(formatAttribute))

    return formatSubreddit
            
def main():
    path = 'C:\\Users\\You (YOU IS NOT MY REAL NAME)\\Documents\\Python Scripts\\reddit\\subs.txt'
    f = open(path, 'w')
    
    top100 = getSubs('https://redditmetrics.com/top') #First 100.
    for subreddit in top100:
        f.write(subreddit + '\n')
    
    url = 'https://redditmetrics.com/top/offset/' #Rest of them.
    for i in range(100, 2000000, 100): #Larger range than there are number of subs.
        try:                           #Will get an exception when it tries to reach a webpage for subs that don't exist and break.
            subreddits = getSubs(url + str(i))
            for subreddit in subreddits:
                f.write(subreddit + '\n')
        except: 
            break
            
    f.close()
    os.startfile(path)

main()
