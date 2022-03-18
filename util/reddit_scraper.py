import random
import config
import asyncpraw

# Gets a random post from POST_LIMIT posts on hot
POST_LIMIT = 15
USER_AGENT = 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'

async def get_aita():
    r = asyncpraw.Reddit(user_agent=USER_AGENT, 
                    client_id=config.REDDIT_ID, 
                    client_secret=config.REDDIT_SECRET)
    aita = await r.subreddit('AmItheAsshole')
    posts = [post async for post in aita.hot(limit=POST_LIMIT)]
    post = posts[random.randint(0, POST_LIMIT)]
    while (post.stickied): post = posts[random.randint(0, POST_LIMIT)]

    post.comment_sort = "top"
    await post.load()
    await post.comments.replace_more(limit=0)
    comments = post.comments.list()

    decisions = ['YTA', 'NTA', 'ESH', 'INFO']
    for top_comment in filter(lambda c: not c.stickied, comments):
        decision = f"The top-level-comment with {top_comment.score} upvotes made the decision: "
        single_decision = "None"
        for i in decisions:
            if i in top_comment.body: 
                if single_decision != "None":
                    single_decision = "None"
                    break
                decision = decision + i + "."
                single_decision = i

        if (single_decision != "None"):
            decision = decision + "\n\n>>> " + top_comment.body
            break

    description = post.selftext.replace("*", "\*").replace("_", "\_").replace("~", "\~")
    submission = {
        "title": post.title,
        "author": post.author,
        "upvotes": post.score,
        "desc": description,
        "link": post.permalink,
        "decision": decision,
        "sdec": single_decision
    }

    await r.close()
    return submission

async def get_subreddit_drama():
    r = asyncpraw.Reddit(user_agent=USER_AGENT,client_id=config.REDDIT_ID,client_secret=config.REDDIT_SECRET)
    subreddit_drama = await r.subreddit('SubredditDrama')
    posts = [post async for post in subreddit_drama.hot(limit=POST_LIMIT)]
    post = posts[[random.randint(0, POST_LIMIT)]]
    while (post.stickied): post = posts[random.randint(0, POST_LIMIT)]

    post.comment_sort = "top"
    await post.load()
    await post.comments.replace_more(limit=0)