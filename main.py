import re
import string
import csv
import tweepy as tw


# https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


def strip_all_entities(text):
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def media_to_csv(tweet_input):
    copy_url = ""
    tweet_media_count = 0

    if 'media' in tweet_input.entities:
        for media in tweet_input.entities.get('media', [{}]):
            copy_url += media['media_url'] + ","
            tweet_media_count += 1

    # print(tweet_input.text + "\n")
    # print(copy_url + "\n")
    # print(str(tweet_media_count) + "\n")

    return tweet_media_count, copy_url


def hastags_to_text(tweet_input):
    copy_hashtags = ""

    if 'hashtags' in tweet_input.entities:
        for hashtags in tweet_input.entities.get('hashtags', [{}]):
            copy_hashtags += "#" + hashtags['text'] + ", "

    return copy_hashtags


def just_text(tweet_input):
    return tweet_input.text


# dev keys for twitter
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# authenticating/establishing access to twitter
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# opening and writing to csv file
csvFile = open(r".\data\tweet_data.csv", 'a', encoding='utf-8-sig')
csvWriter = csv.writer(csvFile)

# defining ---------> search query <-----------
search_words = "#fortnite" + "-filter:retweets"

# OR cash OR vbucks OR item OR shop"

date_since = "2020-1-01"

# setting test counters
count_media = 0
total = 1

# Collect tweets
tweets = tw.Cursor(api.search,
                   q=search_words,
                   lang="en",
                   since=date_since, result_type='top').items()

while True:
    try:
        tweet = tweets.next()

        # transfer media
        media_links_and_info = media_to_csv(tweet)

        # Insert into csv
        # tweet.text.encode('utf-8', 'ignore')
        # https://stackoverflow.com/questions/13896056/how-to-remove-user-mentions-and-urls-in-a-tweet-string-using-python
        # tempString = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())

        strippedInput = strip_all_entities(strip_links(tweet.text))
        tempHashTags = hastags_to_text(tweet)

        print(tweet.text + "\n")

        csvWriter.writerow([tweet.created_at, tweet.id, tweet.id_str, strippedInput, tempHashTags,
                            tweet.source, tweet.truncated, tweet.user.screen_name, tweet.user.location,
                            media_links_and_info[0], media_links_and_info[1], tweet.favorite_count,
                           tweet.retweet_count])

    except tw.TweepError:
        # time.sleep(60 * 15)
        print("Error")
        break
    except StopIteration:
        break

print("\n")
print(count_media)
print(total)

percentage = count_media / total
print(percentage)

# -------------------------------- extra code snippets below -------------------------------#
# api.update_status("Look, I'm tweeting from #Python in my #earthanalytics class! @EarthLabCU")

# Iterate and print tweets
# for tweet in tweets:
#    print(tweet.text)
#    print(tweet.user.screen_name)
#    print(tweet.user.friends_ids)
#   print(count_media)

# getting MEDIA from tweets
# for tweet in tweets:
#     for media in tweet.entities.get("media", [{}]):
#         if media.get("type", None) == "photo":
#             print(tweet.text)
#             count_media += 1
#     total += 1
