import praw
import json
import time
import multiprocessing as mp

reddit = praw.Reddit(
    client_id="83adArc_D-RzLA",
    client_secret="sYyJyc67NIeGvOu5Aenq-nVr3hZbrw",
    password="rosjia@3",
    user_agent="testscript by u/fakebot3",
    username="hushjeee",
)
client_id = "e6le3_23q8ii8w"
client_secret = "tW9zxvnfZmux9Ca2bCFb13eW8yQ"
reddit1 = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent="USERAGENT")


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def query_comments_of_user(username, list_of_unique_subreddits, how_deep=50):
    redditor = reddit.redditor(username)
    dictionary_of_subreddits = {}
    for comment in redditor.comments.new(limit=how_deep):
        list_of_unique_subreddits.add(comment.subreddit.display_name)
        try:
            dictionary_of_subreddits[comment.subreddit.display_name] += 1
        except KeyError:
            dictionary_of_subreddits[comment.subreddit.display_name] = 1
    return dictionary_of_subreddits


def my_func(lock, list_of_visited_redditors, list_of_unique_subreddits, subreddit_name="Polska",
            reddit=reddit, how_deep=2):
    name = mp.current_process().name
    for submission in reddit.subreddit(subreddit_name).hot(limit=how_deep):
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]
        print(name, submission.title)
        while comment_queue:
            comment = comment_queue.pop(0)
            author = comment.author.name
            comment_queue.extend(comment.replies)

            lock.acquire()
            if author not in list_of_visited_redditors:
                list_of_visited_redditors.add(comment.author.name)
                dictionary_of_subreddits = query_comments_of_user(author, list_of_unique_subreddits)

                with open("test.json", "a") as outfile:
                    outfile.write(
                        "\t" + str(f'\"{str(author)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")
                lock.release()
                print(name, author, dictionary_of_subreddits)
            else:
                lock.release()




if __name__ == "__main__":
    # with open("list_of_visited_redditors.json", "r") as input_file:
    #     list_of_visited_redditors = json.load(input_file)
    # list_of_visited_redditors = set(list_of_visited_redditors)
    time1 = time.time()

    list_of_visited_redditors = set()
    list_of_unique_subreddits = set()

    with open("test.json", "w+") as outfile:
        outfile.flush()
        outfile.write("{\n")

    lock = mp.Lock()
    # my_func(outfile, lock, list_of_visited_redditors, list_of_unique_subreddits)

    p1 = mp.Process(name="1: ", target=my_func, args=(
        lock,
        list_of_visited_redditors,
        list_of_unique_subreddits, "Polska", reddit))

    p2 = mp.Process(name="2: ", target=my_func, args=(
        lock,
        list_of_visited_redditors,
        list_of_unique_subreddits, "AskReddit", reddit1))
    p2.start()
    p1.start()

    while p1.is_alive(): #or p2.is_alive():
        pass

    with open("test.json", "a") as outfile:
        #print("Im here!")
        # outfile.seek(outfile.tell() - 3, os.SEEK_SET)  # Removing last comma; closing the dictionary
        outfile.write("\t" + str(f'\"{str("nie_nie_nie")}\"') + ": " + str({}) + "\n")
        outfile.write("}")

    with open("list_of_visited_redditors.json", "w+") as outfile:
        json.dump(list_of_visited_redditors, outfile, cls=SetEncoder)

    print("Elapsed:", time.time() - time1)