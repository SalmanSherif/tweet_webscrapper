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

import csv

csvFile = open("C:\Users\Salman\PycharmProjects\testpy\tweetDataforAnalysis.csv", 'r')
csv_reader = csv.reader(csvFile, delimiter=',')