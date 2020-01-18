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

x = 1
toaster = win10toast.ToastNotifier()


# constant stream of submissions (gets previous 100 posts too)
def stream():
    for submission in subreddit.stream.submissions():  # (pause_after=0)
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                global x
                print("---" + str(x) + "---")
                print(submission.title)
                print("https://reddit.com" + submission.permalink)
                print(submission.url)
                # data for csv file
                parsed_date = datetime.fromtimestamp(submission.created_utc)
                parsed_date_date = parsed_date.date()
                parsed_date_time = parsed_date.time()
                print(parsed_date_date)
                print(parsed_date_time)
                # get last number which should be chap # otherwise default
                try:
                    if "Oneshot" in submission.title:
                        chapter = "Oneshot"
                    elif "Doujinshi" in submission.title:
                        chapter = "Doujinshi " + re.findall(r'[\d\.\d]+', submission.title)[-1]
                    else:
                        chapter = re.findall(r'[\d\.\d]+', submission.title)[-1]
                except IndexError:
                    chapter = "Other"
                # checks if submission is already in filler.csv and adds if not
                with open('filler.csv', 'a+') as f:
                    f.seek(0)  # reads from end of file without (but should?)
                    history = f.read()
                    # loop is to print out manga.json title, not whole title
                    if (title + "," + chapter) not in history:
                        f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "\n")
                        # local notifier test
                        toaster.show_toast("GASGASGAS", f"{submission.title}", duration=3)
                x += 1


old_stack = []


# gets previous 640 posts in case i missed some
def old_posts():
    for submission in subreddit.new(limit=640): # ~3 days back
        '''parsed_date1 = datetime.fromtimestamp(submission.created_utc)
        print(submission.title)
        print(parsed_date1)'''
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                parsed_date = datetime.fromtimestamp(submission.created_utc)
                parsed_date_date = parsed_date.date()
                parsed_date_time = parsed_date.time()
                try:
                    if "Oneshot" in submission.title:
                        chapter = "Oneshot"
                    elif "Doujinshi" in submission.title:
                        chapter = "Doujinshi " + re.findall(r'[\d\.\d]+', submission.title)[-1]
                    else:
                        chapter = re.findall(r'[\d\.\d]+', submission.title)[-1]
                except IndexError:
                    chapter = "Other"
                with open('filler.csv', 'r') as f:
                    history = f.read()
                    if (title + "," + chapter) not in history:
                        old_stack.append(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "\n")
    # if old stack isnt empty, pop everything into csv for correct order
    if old_stack:
        with open('filler.csv', 'a') as f:
            while old_stack:
                last = old_stack.pop()
                print(last)
                f.write(last)


if __name__ == "__main__":
    start = time.time()
    print("Loading...")
    old_posts()
    end = time.time()
    print("Loaded in " + str(end - start) + " seconds")
    stream()

# TODO connect to mangaplus /chart of upload dates
# TODO other: windows task manager to run on login (bat)
# TODO x familt error (Ch.19 returns .19 grr)
