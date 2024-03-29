import json
import praw
from datetime import datetime
import win10toast
import re
import time
from collections import deque
import urllib


# loads reddit API login info from json file x
with open('credentials.json') as f:
    params = json.load(f)
# loads manga list with aptly named list
with open('manga.txt') as f2:
    listed_manga_list = [line.rstrip("\n") for line in f2]

# logs into reddit
reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['client_secret'],
                     username=params['username'],
                     password=params['password'],
                     user_agent=['user_agent'])

# pick a subreddit
subreddit = reddit.subreddit('manga')

# constant stream of submissions (gets previous 100 posts too)
def stream():
    # activate the notifier
    toaster = win10toast.ToastNotifier()
    x = 1
    for submission in subreddit.stream.submissions():
        for title in listed_manga_list:
            # prints info through my manga list only for DISC'S
            if title.lower() in submission.title.lower() and ("DISC" in submission.title or submission.link_flair_text == "DISC"):
                # data for csv file
                parsed_date_date, parsed_date_time, chapter, skip, shorter_site = process_data(submission)
                # continue didn't work in def process() because not in loop so here we are
                if skip is True:
                    break
                # print info for .bat window
                print("---" + str(x) + "---")
                x += 1
                print(submission.title)
                print("https://reddit.com" + submission.permalink)
                print(submission.url)           
                print(parsed_date_date)
                print(parsed_date_time)
                print(shorter_site)

                # checks if submission is already in filler.csv and adds if not
                with open('filler.csv', 'a+') as f:
                    f.seek(0)  # a+ does not read from start (?)
                    history = f.read()
                    # adding only new data to csv file and notifying
                    if (title + "," + chapter) not in history:
                        f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "," + shorter_site + "\n")
                        # notifier
                        toaster.show_toast("GASGASGAS", f"{submission.title}", duration=5)
                        print("***Added***\n")
                        break
                    # stops title search early to prevent repeats (ex. My Hero Academia vs My Hero Academia: Vigilantes)
                    else:
                        print("\n")
                        break


# gets previous 640 posts + timer
def old_posts():
    # temporary storage for old posts
    old_stack = deque()
    # start timer
    start = time.time()
    print("Loading...\n")
    for submission in subreddit.new(limit=640):  # ~3 days back
        for title in listed_manga_list:
            # matches lowercase only for input
            if title.lower() in submission.title.lower() and ("DISC" in submission.title or submission.link_flair_text == "DISC"):
                # had a random submission.url that didn't have a // so it broke so "try"
                try:
                    parsed_date_date, parsed_date_time, chapter, skip, shorter_site = process_data(submission)
                except:
                    print("Skipped " + submission.title)
                    pass
                if skip is True:
                    break
                with open('filler.csv', 'r') as f:
                    history = f.read()
                    # adds posts into stack to reverse order
                    if (title + "," + chapter) not in history:
                        # any() is to find substring in list/deque
                        if any(title + "," + chapter in i for i in old_stack):
                            break
                        else:
                            old_stack.append(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "," + shorter_site + "\n")
                        # breaks inner loop early to prevent repeats and go to next submission
                        break
                    # also breaks loop if post is already in
                    else:
                        break
    # if old stack isnt empty, pop everything into csv for correct order
    if old_stack:
        print("Added:\n\n")
        with open('filler.csv', 'a') as f:
            while old_stack:
                last = old_stack.pop()
                print(last)
                f.write(last)
    # stop timer
    end = time.time()
    print("\nLoaded in " + str(round((end - start), 2)) + " seconds\n\nStarting Stream:\n")
    # for the unit test
    


def process_data(submission):
    # initialize
    skip = False
    chapter = None
    # split datetime into date and time
    parsed_date = datetime.fromtimestamp(submission.created_utc)
    parsed_date_date = parsed_date.date()
    parsed_date_time = parsed_date.time()
    # Get basic site name (cut https then .com)
    site = submission.url.split('//')[1]
    shorter_site = site.split('.')[0].capitalize()
    if site[0:3] == 'www':
        shorter_site = site.split('.')[1].capitalize() #[www, website, com]
    # chapter numbering with special cases
    try:
        if "Oneshot" in submission.title:
            chapter = "Oneshot"
        elif "Doujinshi" in submission.title:
            chapter = "Doujinshi " + re.findall(r'[\d\.\-\d]+', submission.title)[-1]
        elif "WEBCOMIC" in submission.title:
            chapter = "Webcomic " + re.findall(r'[\d\.\-\d]+', submission.title)[-1]
        elif "RAW" in submission.title or "Is Shy" in submission.title:
            skip = True
        elif "final" in submission.title.lower():
            chapter = "FINAL"
        else:
            # find last number in post x.x (should be chap number) ^([a-zA-Z0-9_][a-zA-Z0-9_ ]*[a-zA-Z0-9_]$
            chapter = re.findall(r'[\d\.\-\d]+', submission.title)[-1]
            # bootleg "Chapter.15 = .15" fix - should use better regex
            if chapter[0] == ".":
                chapter = chapter[1:]
            # gets second last num if theres not a num ("-") at the end
            if is_number(chapter) is False:
                chapter = re.findall(r'[\d\.\-\d]+', submission.title)[-2]
    except IndexError:
        chapter = "Other"
    return parsed_date_date, parsed_date_time, chapter, skip, shorter_site


# quick check if its a float or int
def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False



if __name__ == "__main__":
    while True:
        try:
            old_posts()
            stream()
        except urllib.error.HTTPError as e:
            if e.code == 503:
                print("Error 503: Reconnecting...")
                stream()
            else:
                print("Error %s" % e.code)


# maybe TODO connect to mangaplus /chart of upload dates
