#!/usr/bin/env python

import sys
import praw
from datetime import datetime


def main():

    print()

    # just some variables
    usage = """OPTIONS:
    c  = comments
    p  = posts
    a  = all comments and posts
    ls  = list subreddits with posts or comments
    sc = all comments in a subreddit (opt: subreddit)
    sp = all posts in a subreddit    (opt: subreddit)
        """
    comment_results = ""
    post_results = ""

    # get oauth information from praw.ini
    try:
        reddit = praw.Reddit("oauth", config_interpolation="basic")
        print("Oauth Success")
    except:
        logger("Oauth Failed")

    # get the command argument and run the appropriate modules
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "c" | "comments":
                comment_results = scrub_comments(reddit)
            case "p" | "posts":
                post_results = scrub_posts(reddit)
            case "a" | "all":
                comment_results = scrub_comments(reddit)
                post_results = scrub_posts(reddit)
            case "sc":
                if len(sys.argv) > 2:
                    r = sys.argv[2]
                else:
                    r = input("Which subreddit? r/")
                comment_results = scrub_subreddit_comments(reddit, r)
            case "sp":
                if len(sys.argv) > 2:
                    r = sys.argv[2]
                else:
                    r = input("Which subreddit? r/")
                comment_results = scrub_subreddit_posts(reddit, r)
            case "ls":
                list_subs(reddit)
            case _:
                sys.exit(usage)
    else:
        sys.exit(usage)

    # print stats for this run to the screen and add to the log file
    logger(f"{comment_results}\n{post_results}")

    sys.exit(0)


def logger(log_data):
    try:
        with open("scrubby.log", "a+") as f:
            print(log_data)
            f.write(f"{datetime.now().strftime('%m-%d-%Y, %H:%m')}:\n{log_data}\n\n")
    except:
        print("Unable to write to log file")


def get_age(item):
    # get the date and age of the passed item
    d = datetime.fromtimestamp(item.created)
    item_date = d.strftime("%m/%d/%Y")
    item_age = (datetime.now() - datetime.fromtimestamp(item.created)).days
    return {"date": item_date, "age": item_age}


def list_subs(reddit):
    active_subs = set()
    for comment in reddit.user.me().comments.new(limit=None):
        active_subs.add(comment.subreddit.display_name)

    for post in reddit.user.me().submissions.new(limit=None):
        active_subs.add(post.subreddit.display_name)

    active_subs = sorted(active_subs)
    for s in active_subs:
        print(s)

    print()
    sys.exit(0)


def scrub_subreddit_comments(reddit, r):
    x, y = 0, 0

    # parse all comments
    for comment in reddit.user.me().comments.new(limit=None):

        # iterate, overwrite and delete any comments found in the subreddit
        if comment.subreddit == r:
            y += 1
            comment.edit(body=comment)
            comment.delete()
        x += 1

    # return the number of comments found and deleted
    return f"  Comments: {y}/{x}"


def scrub_subreddit_posts(reddit, r):
    x, y = 0, 0

    # parse all posts
    for post in reddit.user.me().submissions.new(limit=None):

        # iterate, overwrite and delete any posts found in the subreddit
        if post.subreddit == r:
            y += 1
            post_date = get_age(post)["date"]
            print(f"{post_date}, r/{post.subreddit}:\n{post.title}\n-----\n")
            post.delete()
        x += 1

    # return the number of comments found and deleted
    return f"  Posts: {y}/{x}"


def scrub_comments(reddit):
    x, y = 0, 0
    e_error, d_error = 0, 0

    # parse the comments, overwrite those older than specified days and delete
    for comment in reddit.user.me().comments.new(limit=None):

        # get the date and age of the comment
        a = get_age(comment)

        # comment_date = a["date"]
        comment_age = a["age"]

        # iterate all of the comments, overwrite and delete any comment over specified days old
        if x >= 25 or comment_age > 14:
            try:
                comment.edit(body=comment)
            except:
                e_error += 1
            try:
                comment.delete()
            except:
                d_error += 1
            y += 1

        x += 1

    # return the number of comments found and deleted
    return f"  Comments: {x}, Deleted: {y}, Edit errors: {e_error}, Delete errors: {d_error}"


def scrub_posts(reddit):
    x, y = 0, 0
    d_error = 0

    # get all of the submissions and display the title and date
    for post in reddit.user.me().submissions.new(limit=None):

        # get the date of the post
        a = get_age(post)

        # post_date = a["date"]
        post_age = a["age"]

        # iterate all of the comments, overwrite and delete any comment over specified days old
        if x >= 20 or post_age > 21:
            try:
                post.delete()
            except:
                d_error += 1

            y += 1

            print(f"\n{a['date']}, r/{post.subreddit}: {post.title}")
        x += 1

    # return the number of posts found and deleted
    return f"  Posts: {x}, Deleted {y}, Errors: {d_error}"


if __name__ == "__main__":
    main()
