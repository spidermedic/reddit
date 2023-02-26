# scrubby

Scrubby is a Reddit bot that will delete posts and comments  based on date and/or a maximum number of posts. 

    if max_posts >= 30 or comment_age > 21:
      comment.edit(body=comment)
      comment.delete()  

usage: python scrubby.py [ls|a|c|p|sc|sp] {subreddit}
    
OPTIONS:  
 ls : list subreddits with posts or comments  
 a  : deletes all comments and posts  
 c  : deletes all comments older than x days
 p  : deletes all posts older than x days
 sc : deletes all comments in a subreddit (opt: subreddit)  
 sp : deletes all posts in a subreddit    (opt: subreddit)  
 
