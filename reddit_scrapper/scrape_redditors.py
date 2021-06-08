import asyncpraw
import json
import time
import asyncio



async def test():
    reddit = asyncpraw.Reddit(
        client_id="83adArc_D-RzLA",
        client_secret="sYyJyc67NIeGvOu5Aenq-nVr3hZbrw",
        user_agent="My test something")

    subreddit = await reddit.subreddit("Polska")
    async for submission in subreddit.new(limit=25):
        comments = await submission.comments()
        comments.replace_more(limit=None)
        all_comments = await comments.list()
        for comment in all_comments:
            print(comment.body)
            # try:
            #     print(comment.body)
            # except AttributeError:
            #     print("SHIEEEEEEEEET")


    await reddit.close()


if __name__ == "__main__":
    asyncio.run(test())
