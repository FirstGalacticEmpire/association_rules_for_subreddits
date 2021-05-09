import json


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    data = json.load(open("test.json", "r"))
   #print(list(data.keys()))
    # with open("list_of_visited_redditors.json", "w+") as outfile:
    #     json.dump(list(data.keys()), outfile, cls=SetEncoder)

    list_of_unique_subreddits = set()
    for a in [list(x.keys()) for x in data.values()]:
        list_of_unique_subreddits.update(a)
    print(list_of_unique_subreddits)
    print(len(list_of_unique_subreddits))
    with open("list_of_unique_subreddits.json", "w+") as outfile:
        json.dump(list_of_unique_subreddits, outfile, cls=SetEncoder)
    #print([list(x.keys()) for x in data.values()])
