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

# pick a subreddit
subreddit = reddit.subreddit('all')

# new_python = subreddit.new(limit=500)  # limit of 984(max?)(5ish days ago)(replaced by stream() but need a way to get old posts(or host online))

x = 1
for submission in subreddit.stream.submissions(): #constant stream of submissions
    if any(_ in submission.title for _ in ["MangaDex", "[ART] Fubuki", "a Legend", "Black ",'What']):  # case sensitive(might want lower method)(also use list(?) to do multi)
        print(submission.title)
        print(x)
        x += 1

# TODO priority: get links for notifier
# TODO pick manga/ connect to mangaplus /chart of upload dates/notify you dum
# TODO other: windows task manager to run on login
# maybe get avg num of posts daily for predicting limit
