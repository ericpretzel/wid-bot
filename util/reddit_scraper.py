import random
import config
import asyncpraw

POST_LIMIT = 10
USER_AGENT = 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'

async def get_aita():
    r = asyncpraw.Reddit(user_agent=USER_AGENT, 
                    client_id=config.REDDIT_ID, 
                    client_secret=config.REDDIT_SECRET)
    aita = await r.subreddit('AmItheAsshole')
    posts = [post async for post in aita.hot(limit=POST_LIMIT)]
    post = posts[random.randint(0, POST_LIMIT)]

    submission = {
        "title": post.title,
        "author": post.author,
        "upvotes": post.score,
        "desc": post.selftext,
        "link": post.permalink
    }

    return submission
