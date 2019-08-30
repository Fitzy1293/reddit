from lxml import html, etree
import requests
from pprint import pprint
import os



def getInfo(url):
    page = requests.get(url)
    htmlContent = html.fromstring(page.content)

    body = htmlContent[1]
    body = etree.tostring(body)
    body = body.decode('UTF-8')


    body = body.split('\n')
    body = [line for line in body if '<td class="tod"' in line]

    subredditInfo = []
    for i in range(0, len(body), 3):
        subredditInfo.append(body[i:i+3])  

    formatSubreddit = []
    for subreddit in subredditInfo:
        formatAttribute = []
        for j, attribute in enumerate(subreddit):
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
    path = 'C:\\Users\\Owen\\Documents\\Python Scripts\\reddit\\subs.txt'
    f = open(path, 'w')
    top100 = getInfo('https://redditmetrics.com/top')
    
    for subreddit in top100:
        f.write(subreddit + '\n')
    
    url = 'https://redditmetrics.com/top/offset/'
    for i in range(100, 2000000, 100):
        try:
            subreddits = getInfo(url + str(i))
            for subreddit in subreddits:
                f.write(subreddit + '\n')
        except:
            break
            
    f.close()
    os.startfile(path)

main()
