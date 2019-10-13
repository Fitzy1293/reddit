from lxml import html, etree
from pprint import pprint
import os, time, requests, threading
from multiprocessing import Pool

#createList(chunk) does pretty much everything.
#I didn't want it to be this long.
#Because you have to run this asynchronous with multiple processes or it'll take 6 hours, it's difficult to separate into smaller functions.
#Takes ~1 hour 40 minutes to successfully do every subreddit. 
def createList(chunk):
    temp = [] 
    for url in chunk:
        page = requests.get(url)
        htmlContent = html.fromstring(page.content)
        htmlContent = htmlContent[1]
        
        byteTree = etree.tostring(htmlContent)
        body = byteTree.decode('UTF-8') #Decode bitecode into a string.
        body = body.split('\n')
        temp.append(body)

    contents = [j for i in temp for j in i]
        
    attributeLines = [line.strip() for line in contents if '<td class="tod"' in line] #'<td class="tod"' is where the info about the subs is.
    subreddits = [attributeLines[i:i+3] for i in range(0, len(attributeLines), 3)]
    
    rows = []
    for i, subreddit in enumerate(subreddits):
        rank = subreddit[0].split('<')[-2]
        rank = rank.split('>')[-1]
        if ',' in rank:
            rank = rank.replace(',', '')
            
        try:
            subredditName = subreddit[1].split('<td class="tod"><a href="/r/')[1]
            subredditName = subredditName.split('"')[0]
        except IndexError as e:
            print(subreddit)
            print(e)

        subscribers = subreddit[2].split('</td>')[-2]
        subscribers = subscribers.split('>')[-1]

        row = rank + '\t' + subredditName + '\t' + subscribers + '\n'
        rows.append(row)

    #Write new file because async and multiple processes stuff, can't really test results easily while the program is running.
    #Writing a new file and using pool.map_async(), then combining at the end was by far the fastest.
    fname = rows[0].split('\t')[0] + '_chunk' + '.txt' #e.g 1_chunk.txt
    with open(fname, 'w+') as f:
        for row in rows:
            f.write(row)

    return rows


#Using .txt conatining redditmetrics.com urls.
#I manually update this based on however many subs redditmetrics.com says.
#Those urls contain the info for 100 subreddits.
#I sub divide these urls to use later with with pool.map_async()
def chunkUrls():
    urls = open('redditmetrics urls.txt', 'r').read().splitlines() #List of redditmetrics urls, each url has info on 100 subreddits.
    chunkSize = 5
    chunks = [urls[i : i + chunkSize] for i in range(0, len(urls), chunkSize)]

    return chunks

#Fastest way I found to deal with the huge amount of requests, and data manipulation into a usable form
def createTemp():
    pool = Pool(processes=10)
    pool.map_async(createList, chunkUrls())
    pool.close()
    pool.join()

def main():
    createTemp()

    #async stuff may not return things in the order you want, sorting files by first char of filename.
    files = []
    for file in os.listdir():
        if file.endswith('_chunk.txt'):
            files.append(file.split('_'))

    files.sort(key=lambda x:int(x[0]))
    files = ['_'.join(file) for file in files]
  
    
    
    with open('subs.txt', 'w+') as new:
        new.write('Rank' + '\t' + 'Subreddit Name' + '\t' + 'Subscriber count\n')
        for file in files:
            rows = open(file, 'r').read().splitlines() 
            for row in rows:
                new.write(row + '\n')
            

    subsTxtPath = os.path.join(os.getcwd(),'subs.txt')
    
    print(f'Text file containing the subreddits - {subsTxtPath}')
    print('Press enter to open this.')
    input()

    os.startfile('subs.txt')

if __name__ == '__main__':
    start = time.time()
    main()
    end = (time.time())
    print(f'Run time: {end-start} seconds')
    
