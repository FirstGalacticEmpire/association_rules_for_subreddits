# https://gist.github.com/tamj0rd2/6bd02b02d34bb4f124d9a1c3c6a614e7
# Copied from link above.
# Not any original code!

import json
import os
import requests
import time


def write_to_file(data, **kwargs):
    '''Writes a string to a file'''
    global json_file_path
    end = kwargs.pop('end', False)
    if end:
        # once we're at the end of the script, remove the trailing ", "
        with open(json_file_path, 'rb+') as f:
            f.seek(-2, os.SEEK_END)
            f.truncate()
    with open(json_file_path, 'a') as f:
        f.write(data)


def output_subreddits(num_of_subs):
    '''Writes the subreddits to the file you specified'''
    subreddits_url = "http://www.reddit.com/reddits"
    after = ""
    count = 0

    # required by reddit's API rules
    headers = {'User-agent': 'platform:appID:version (by u/username)'}

    while (after is not None) and count < num_of_subs:
        url = "%s.json?limit=100&after=%s" % (subreddits_url, after)
        response = requests.get(url, headers=headers)
        data = response.json()['data']

        for child in data['children']:
            subreddit = child['data']['display_name']
            write_to_file('"%s", ' % subreddit)

        count += 100

        # used to get the next page of subreddits
        after = data['after']
        # required by reddit's API rules
        time.sleep(2)


# ==== CONFIGURATION ==== #
# the path to your json file
json_file_path = "./filename.json"
# the number of subreddits you want
subreddit_cap = 10
if __name__ == "__main__":
    # ==== MAIN THINGY ==== #
    write_to_file("[")
    output_subreddits(subreddit_cap)
    write_to_file("]", end=True)
    print("DONE!")