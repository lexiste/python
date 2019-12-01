from twython import Twython
from twython import TwythonStreamer
import time, sys

# 
# cdate: 01-sept-2017
# mdate: 01-sept-2017
# notes: 
# 
# http://adilmoujahid.com/posts/2014/07/twitter-analytics/ as a basis
# http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
# https://dev.twitter.com/streaming/overview/request-parameters
#
#  - record all data when a tweet matches the track string
#  - work up to using the JSON strings to parse for meaningful data sets
#

from auth import (
   consumer_key,
   consumer_secret,
   access_token,
   access_token_secret
)

client_args = {
   "headers": {
      "accept-charset": "utf-8"
   }
}

# print the entire JSON string to stdout if the track string is found
class MyStreamer(TwythonStreamer):
   def on_success(self, data):
      if 'text' in data:
         #print all the data in JSON output
         #print data
         username = data['user']['screen_name'].encode('utf-8')
         postdate = data['created_at'].encode('utf-8')
         tweet = data['text'].encode('utf-8')
         print("@{}|{}|{}".format(username, postdate, tweet))

stream = MyStreamer(
   consumer_key,
   consumer_secret,
   access_token,
   access_token_secret
)

# create a unique string to post, sending the same message results in a 403 "Duplicate Message" response :(
#message = "HAL9000 " + time.strftime('%Y%m%d-%H%M%S')

# track can consist of multiple strings using ['str1', 'str2', 'str3']
# track is used for search "all" of twitter and looking for the specific string(s)
#stream.statuses.filter(track=['realDonaldTrump'])

# track a user(s) account ... 
# the follow param needs the actual Twitter UserID, not the screen name
#  use gettwitterid.com/?user_name=FOLLOW_ME&submit=GET+USER+ID to find the UserID
realDT = '25073877'
cnn = '759251'
msnbc = '2836421'
Hyde = '771124137024565249'

stream.statuses.filter(follow=Hyde)
