# https://github.com/Fitzy1293/reddit
## Random programs for reddit

**The programs**

Keep in my mind that everything but the All subs project gets as much as the reddit API allows. 
  - All subs project is a way to get a daily list of all subreddits and their subscriber count. 
  - All subs "DATE".zip contains a .txt with an ordered list of all subreddits with subscriber count as of that date.
  - getusers.py uses a list of subreddits to get an unordered list of users. users.txt is the result I got when I ran it. Useful if you     need random reddit usernames to analyze. topsubs.txt is the top 100 subreddits as of when it was uploaded. 
  - push.py gets posts going back to a specified number of years, weeks, days, hours, and minutes. Cool program.
  - reddituserkeyword.py was for someone who asked for a way to see if a redditor has mentioned a specified word. Whipped up very           quickly. 
  - reddituserposts.py gives you the subreddits a user posted and commented in, then allows you to pick one of those subreddits, and         look at their posts and comments. I like this one the most. 
  - submissionComments.py creates a .CSV of comments from a specified number of current posts in a subreddit. 
  
**Background on why this exists**

So what is this repository? 
It’s really just a jumbled mess of programs I’ve worked on for reddit.

I started using PRAW to mess around and improve my programming skills, as comp. sci. is not my main educational background.
I took some introduction comp. sci. classes my freshman year of college, but those classes did not get very in depth. The python and java courses I took taught almost the exact same material. 

I had an internship as a systems engineer dealing with hardware and software requirements for a legacy system.
We used a relational database - with upper level requirements linked to lower level requirements, which were in turn linked to test steps. Most of the work was to look for inconsistencies, which was done by filtering in excel.
Sometimes the tasks would be very tedious, so I started using python to make tasks easier as that was the programming language I was most comfortable with. 

My PRAW adventures started as a way for me to practice programming/data management outside of work. 

You can do a lot of neat things with PRAW, and it's a great way to make useful projects.

A problem I have with intro to programming classes is all of the skills you learn are correct, but the projects are usually unimportant.
A typical intro to programming project will be to make a dungeon. 
This will introduce students to 2-D lists/arrays for the floor map, and dictionaries/hash tables for the weapons. 
But it's useless! These projects feel as if you're accomplishing nothing real, tangible, or even remotely important. 
It's hard for a student to connect these projects - with what programming is actually useful for. 
But PRAW makes finding useful projects to connect learning simple.
Want to archive posts this week from your favorite subreddits that have more than 1k karma as a .CSV? You can!
Because programming is so hands on, finding projects that feel important to you is so important when you start programming. PRAW is a great way to do this. 
I feel that the irrelevance of most intro. to programming projects leads many people to label programming as boring.

**Problems**

PRAW limits you to a thousand posts in a response, but I've been recently learning how to use pushshift so there's that.

If you notice an issue or have a question please post it in issues. 
I am not a programming guru, so I may be doing things in not the most efficient way, and my code may not be the most "correct"!

A note on -

from authenticate import authenticate 
reddit = authenticate() 

I started to use a module I made that has one function that returns all of my reddit API authentification info and a link to my reddit repository on github. Here’s what it looks like - 

```
import praw
def authenticate():
reddit = praw.Reddit(client_id='YOUR CLIENT ID',
client_secret='YOUR CLIENT SECRET',
user_agent='URL OF YOUR SCRIPT',
username='/u/YOU')
return reddit
```

You must keep the API info secret or you can get banned from using it. 
This allows me to upload code without having to worry about changing the authentication info every time I upload. 
