import json
import praw
from datetime import datetime
import win10toast
import re
import time


# loads reddit API login info from json file
with open('credentials.json') as f:
    params = json.load(f)
# loads manga list with aptly named list
with open('manga.json') as f2:
    manga_list = json.load(f2)
    listed_manga_list = list(manga_list.keys())
# logs into reddit
reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['client_secret'],
                     username=params['username'],
                     password=params['password'],
                     user_agent=['user_agent'])

# pick a subreddit (technically not necessary here)
subreddit = reddit.subreddit('manga')


# constant stream of submissions (gets previous 100 posts too)
def stream():
    toaster = win10toast.ToastNotifier()
    for submission in subreddit.stream.submissions():  # (pause_after=0)
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                # print info for .bat window 
                x = 1
                print("---" + str(x) + "---")
                print(submission.title)
                print("https://reddit.com" + submission.permalink)
                print(submission.url)
                # data for csv file
                parsed_date_date, parsed_date_time, chapter, skip = process_data(submission)
                print(parsed_date_date)
                print(parsed_date_time)
                # continue didn't work in def() because not in loop so here we are
                if skip is True:
                    continue
                # checks if submission is already in filler.csv and adds if not
                with open('filler.csv', 'a+') as f:
                    f.seek(0)  # a+ does not read from start (?)
                    history = f.read()
                    # adding only new data to csv file and notifying
                    if (title + "," + chapter) not in history:
                        f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "\n")
                        # notifier
                        toaster.show_toast("GASGASGAS", f"{submission.title}", duration=3)
                x += 1


old_stack = []


# gets previous 640 posts in case i missed some
def old_posts():
    for submission in subreddit.new(limit=640): # ~3 days back
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                parsed_date_date, parsed_date_time, chapter, skip = process_data(submission)
                if skip is True:
                    continue
                with open('filler.csv', 'r') as f:
                    history = f.read()
                    # adds posts into stack to reverse order
                    if (title + "," + chapter) not in history:
                        old_stack.append(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "\n")
    # if old stack isnt empty, pop everything into csv for correct order
    if old_stack:
        with open('filler.csv', 'a') as f:
            while old_stack:
                last = old_stack.pop()
                print(last)
                f.write(last)


def process_data(submission):
    # ignore submission initialize
    skip = False
    # mandatory chapter initialize
    chapter = None
    # split datetime into date and time
    parsed_date = datetime.fromtimestamp(submission.created_utc)
    parsed_date_date = parsed_date.date()
    parsed_date_time = parsed_date.time()
    # chapter numbering with special cases
    try:
        if "Oneshot" in submission.title:
            chapter = "Oneshot"
        elif "Doujinshi" in submission.title:
            chapter = "Doujinshi " + re.findall(r'[\d\.\d]+', submission.title)[-1]
        elif "RAW" in submission.title:
            skip = True
        else:
            chapter = re.findall(r'[\d\.\d]+', submission.title)[-1]
    except IndexError:
        chapter = "Other"
    return parsed_date_date, parsed_date_time, chapter, skip


if __name__ == "__main__":
    # run main functions with a timer for old posts
    start = time.time()
    print("Loading...\n")
    old_posts()
    end = time.time()
    print("Loaded in " + str(round((end - start), 2)) + " seconds\n")
    stream()

# TODO connect to mangaplus /chart of upload dates
# TODO other: windows task manager to run on login (bat)
# TODO x familt error (Ch.19 returns .19 grr)
