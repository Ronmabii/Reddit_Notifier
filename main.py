import json
import praw

# loads reddit API login info from json file
with open('credentials.json') as f:
    params = json.load(f)

# logs into reddit
reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['client_secret'],
                     username=params['username'],
                     password=params['password'],
                     user_agent=['user_agent'])

# reddit calls
subreddit = reddit.subreddit('manga')

new_python = subreddit.new(limit=10)  # limit of 984(max?)(5ish days ago) works but slight stutter every 100 posts

x = 1
for submission in new_python:
    if any(x in submission.title for x in ["Manga", "decent"]):  # case sensitive(might want lower method)(also use list(?) to do multi)
        print(submission.title)
        print(x)
        x += 1

# TODO priority: get links for notifier
# TODO pick manga/ connect to mangaplus /chart of upload dates/notify you dum
# TODO other: windows task manager to run on login
# maybe get avg num of posts daily for predicting limit
