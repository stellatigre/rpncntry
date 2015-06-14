import tweepy, json, random
from time import sleep
 
config = json.load(open("config.json", "r+"))
phrases = ["this song is so good, tho: ",
		   "give this song a try, maybe : ",
		   "you know rap and country can both be really good ? give em' a shot: "]
		   
songs = ["https://www.youtube.com/watch?v=KSurzeGvPrQ",	# Accidental Racist
		 "https://www.youtube.com/watch?v=n3htOCjafTc"] # Over & Over

class TwitterAPI:
    def __init__(self):
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = config['access_token']
        access_token_secret = config['token_secret']
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
 
    def query(self, phrase):
        return [item for item in tweepy.Cursor(self.api.search, q=phrase).items(25)]
 
    def reply(self, message, reply_to):
        self.api.update_status(status=message, in_reply_to_status_id=reply_to)
 
if __name__ == "__main__":
	twitter = TwitterAPI()
	nerds = twitter.query("everything but rap and country")
	for nerd in nerds:
		#print nerd.text.encode("utf-8")
		if nerd.retweeted is False:
			response = random.choice(phrases) + random.choice(songs)
			reply_text = '@' + nerd.user.screen_name + " " + response
			print "Tweeting:"
			print reply_text
			twitter.reply(reply_text, nerd.id)
			sleep(config['delay'])
