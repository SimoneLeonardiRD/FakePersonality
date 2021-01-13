import requests


def resolve_url(url):
    '''
        Expand shortened url. Return url, longurl
    '''
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException:
        return (url, None)

    if r.status_code != 200:
        longurl = None
    else:
        longurl = r.url

    return (url, longurl)


def find_url(line):
    for word in line.split(" "):
        if word.startswith("http"):
            url = resolve_url(word.rstrip("\n"))
            if url[1] is not None:
                return url[1]
    return None


def parse_match_count(fake_news_list, users_id):
    counter_users = 1
    total = len(users_id)
    for user in users_id[:5]:
        print("Progress: " + str(counter_users) + "/" + str(total))
        print(str(user))
        counter_fake_tweets = 0.0
        counter_lines_checked = 0.0
        fin = open("data/tweet/"+str(user), "r")
        for line in fin.readlines():
            counter_lines_checked += 1
            url = find_url(line)
            if url is not None:
                if url in fake_news_list:
                    print(user, "fake link found\n")
                    print(line)
                    counter_fake_tweets += 1  # salvare per stance detection
        fin.close()
        print("fake tweet perc: " +
              str((counter_fake_tweets/counter_lines_checked)*100))
        counter_users += 1
