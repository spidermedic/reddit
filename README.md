# scrubby

Scrubby is a Reddit bot that will delete posts and comments  based on date and/or a maximum number of posts.
To change the max number or max age, change the variables below.

    def scrub_comments(reddit):
        max_comments_allowed = 30  # limits the number comments to this number
        max_comment_age = 10       # deletes comments older than the specified number of days

    def scrub_posts(reddit):
        max_posts_allowed = 10  # limit the number of active posts
        max_post_age = 14       # delete posts older than the specified number of days

usage: python scrubby.py [ls|a|c|p|sc|sp] {subreddit}
    
OPTIONS:  
 ls : list subreddits with posts or comments  
 a  : deletes all comments and posts  
 c  : deletes all comments older than x days
 p  : deletes all posts older than x days
 sc : deletes all comments in a subreddit (opt: subreddit)  
 sp : deletes all posts in a subreddit    (opt: subreddit)  
 
Scrubby requires python 3.10 or higher as well as the praw and logging modules.