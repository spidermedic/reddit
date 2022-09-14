# scrubby

Scrubby is a Reddit bot that will delete posts and comments  based on date and/or a maximum number of posts. 

  if max_posts >= 30 or comment_age > 21:
    comment.edit(body=comment)
    comment.delete()  

usage: python scrubby.py [a|c|p|s|sc|sp]
    
OPTIONS:
c  = deletes comments
p  = deletes posts
a  = deletes all comments and posts
s  = list subreddits with posts or comments
sc = deletes all comments in a subreddit (opt: subreddit)
sp = deletes all posts in a subreddit    (opt: subreddit)
 
