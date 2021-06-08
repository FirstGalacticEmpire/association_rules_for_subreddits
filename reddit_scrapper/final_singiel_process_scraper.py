import praw
import json
import time

reddit = praw.Reddit(
    client_id="83adArc_D-RzLA",
    client_secret="sYyJyc67NIeGvOu5Aenq-nVr3hZbrw",
    password="rosjia@3",
    user_agent="testscript by u/fakebot3",
    username="hushjeee",
)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def query_comments_of_user(username, list_of_unique_subreddits, how_deep=50):
    redditor = reddit.redditor(username)
    dictionary_of_subreddits = {}
    # try:
    comments = redditor.comments.new(limit=how_deep)
    # except Exception as e:
    #     print(e)
    for comment in comments:
        list_of_unique_subreddits.add(comment.subreddit.display_name)
        try:
            dictionary_of_subreddits[comment.subreddit.display_name] += 1
        except KeyError:
            dictionary_of_subreddits[comment.subreddit.display_name] = 1
    return dictionary_of_subreddits


def my_func(list_of_visited_redditors, list_of_unique_subreddits, subreddit_name="Polska",
            reddit=reddit, how_deep=100, file_name="test.json"):
    for submission in reddit.subreddit(subreddit_name).hot(limit=how_deep):
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]
        print(submission.title)
        counter = 0
        while comment_queue:
            comment = comment_queue.pop(0)
            try:
                author = comment.author.name
            except AttributeError:
                continue
            comment_queue.extend(comment.replies)

            if author not in list_of_visited_redditors:
                list_of_visited_redditors.add(comment.author.name)
                try:
                    dictionary_of_subreddits = query_comments_of_user(author, list_of_unique_subreddits)
                except Exception as e:
                    counter += 1
                    if counter == 5:
                        raise e
                    time.sleep(5)
                    print(counter, e)
                    continue
                with open(file_name, "a") as outfile:
                    outfile.write(
                        "\t" + str(f'\"{str(author)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")

                print(author, dictionary_of_subreddits)


def start_file(file_name):
    with open(file_name, "w+") as outfile:
        outfile.flush()
        outfile.write("{\n")


def end_file():
    with open(file_name, "a") as outfile:
        # outfile.seek(outfile.tell() - 3, os.SEEK_SET)  # Removing last comma; closing the dictionary
        outfile.write("\t" + str(f'\"{str("nie_nie_nie")}\"') + ": " + str({}) + "\n")
        outfile.write("}")


if __name__ == "__main__":
    file_name = "a_test.json"
    # TODO http error handling
    start_time = time.time()

    with open("filename.json", "r") as outfile:
        most_popular_subreddits = json.load(outfile)

    # list_of_visited_redditors = set()
    with open("list_of_visited_redditors.json", "r") as outfile:
        list_of_visited_redditors = set(json.load(outfile))

    # list_of_unique_subreddits = set()
    with open("list_of_unique_subreddits.json", "r") as outfile:
        list_of_unique_subreddits = set(json.load(outfile))

    start_file(file_name)  # IMPORTANT DO NOT UNCOMMENT THIS!

    done_subreddits = []
    for subreddit in most_popular_subreddits:
        print(subreddit)
        try:
            my_func(list_of_visited_redditors, list_of_unique_subreddits, subreddit, how_deep=5, file_name=file_name)
            done_subreddits.append(subreddit)
        except Exception as e:
            print(e)
            break
    print(done_subreddits)

    # end_file(file_name)

    with open("list_of_visited_redditors.json", "w+") as outfile:
        json.dump(list_of_visited_redditors, outfile, cls=SetEncoder)

    with open("list_of_unique_subreddits.json", "w+") as outfile:
        json.dump(list_of_unique_subreddits, outfile, cls=SetEncoder)

    print("Elapsed:", time.time() - start_time)
