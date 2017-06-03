#
# =====
# nOlaf
# =====
# 
# shifubear (Shion Fukuzawa) and Andrew Thomas

# PREMISE:
#   Someone reports malicious user
#   Track their tweets/convos. IF bad, ban and add to ban list
#       Track devices this user has used.
#   Waits around targeted user for other harassment
#   If something happens from there, compares language of user using watson with
#   original account.
#
# Shadow account is likely not connected to original account
#
# Reads tweets
# Detects malicious user.
# Saves user's info (userid/email/ipaddress) into database.
# If detects similar user, follows them closely.

# Comprehensive list of usernames/email that lean towards harrasment

import json
from watson_developer_cloud import ToneAnalyzerV3
import requests
import twitter

tone_analyzer = ToneAnalyzerV3(
   username='9a88a3d4-2eb0-4e85-afb3-9e4287fb73aa',
   password='3ArjEoVapu3A',
   version='2016-05-19')

api = twitter.Api(consumer_key='VuzcsX0hRpjuLo7jiYuBfnOwP',
                  consumer_secret='4j6B2bVxKn1BQsADAqsdvQCMnvAzhMv4TVccySmkQqGEf2EYd9',
                  access_token_key='771449996956893184-DKteQBZP4ByJ2CB8MYmg3fdqewG9c6L',
                  access_token_secret='wMyQixECraN5MjlEP2Lb8gkbMMW0dnzLacXZsR816zvVl')

userID1 = input('Please enter the user ID of the user you\'d like to search. ')
userID2 = input('Please enter the user ID of the user you\'d like to compare to. ')



"""
Pick a user.
Loop through each of the user's tweets in the existing for loop, generating a total score for the user.
"""
def analyzeTweets(userID, writeMode, max=None):

	listOfTweets = api.GetUserTimeline(user_id=userID, count=20, include_rts=False, max_id=max)
	userData = api.GetUser(user_id=userID)
	# NUMBER OF TWEETS
	tweet_count = len(listOfTweets)

	# USER'S OVERALL EMOTIONAL TONE
	u_anger = 0
	u_disgust = 0
	u_fear = 0
	u_joy = 0
	u_sadness = 0

	# USER'S OVERALL LANGUAGE TONE
	u_analytical = 0
	u_confident = 0
	u_tentative = 0

	# USER'S OVERALL SOCIAL TONE
	u_openness = 0
	u_conscientiousness = 0
	u_extraversion = 0
	u_agreeableness = 0
	u_emotionrange = 0

	for i in range(tweet_count):

		json_text = json.dumps(tone_analyzer.tone(text=listOfTweets[i].text), indent=2)
		parsed_json = json.loads(json_text)

		# EMOTIONAL TONE
		anger_name = parsed_json["document_tone"]["tone_categories"][0]['tones'][0]['tone_name']
		anger_score = parsed_json["document_tone"]["tone_categories"][0]['tones'][0]['score']
		u_anger += anger_score
		disgust_name = parsed_json["document_tone"]["tone_categories"][0]['tones'][1]['tone_name']
		disgust_score = parsed_json["document_tone"]["tone_categories"][0]['tones'][1]['score']
		u_disgust += disgust_score
		fear_name = parsed_json["document_tone"]["tone_categories"][0]['tones'][2]['tone_name']
		fear_score = parsed_json["document_tone"]["tone_categories"][0]['tones'][2]['score']
		u_fear += fear_score
		joy_name = parsed_json["document_tone"]["tone_categories"][0]['tones'][3]['tone_name']
		joy_score = parsed_json["document_tone"]["tone_categories"][0]['tones'][3]['score']
		u_joy += joy_score
		sadness_name = parsed_json["document_tone"]["tone_categories"][0]['tones'][4]['tone_name']
		sadness_score = parsed_json["document_tone"]["tone_categories"][0]['tones'][4]['score']
		u_sadness += sadness_score

		# LANGUAGE TONE
		analytical_name = parsed_json["document_tone"]["tone_categories"][1]['tones'][0]['tone_name']
		analytical_score = parsed_json["document_tone"]["tone_categories"][1]['tones'][0]['score']
		u_analytical += analytical_score
		confident_name = parsed_json["document_tone"]["tone_categories"][1]['tones'][1]['tone_name']
		confident_score = parsed_json["document_tone"]["tone_categories"][1]['tones'][1]['score']
		u_confident += confident_score
		tentative_name = parsed_json["document_tone"]["tone_categories"][1]['tones'][2]['tone_name']
		tentative_score = parsed_json["document_tone"]["tone_categories"][1]['tones'][2]['score']
		u_tentative += tentative_score

		# SOCIAL TONE
		openness_name = parsed_json["document_tone"]["tone_categories"][2]['tones'][0]['tone_name']
		openness_score = parsed_json["document_tone"]["tone_categories"][2]['tones'][0]['score']
		u_openness += openness_score
		conscientiousness_name = parsed_json["document_tone"]["tone_categories"][2]['tones'][1]['tone_name']
		conscientiousness_score = parsed_json["document_tone"]["tone_categories"][2]['tones'][1]['score']
		u_conscientiousness += conscientiousness_score
		extraversion_name = parsed_json["document_tone"]["tone_categories"][2]['tones'][2]['tone_name']
		extraversion_score = parsed_json["document_tone"]["tone_categories"][2]['tones'][2]['score']
		u_extraversion += extraversion_score
		agreeableness_name = parsed_json["document_tone"]["tone_categories"][2]['tones'][3]['tone_name']
		agreeableness_score = parsed_json["document_tone"]["tone_categories"][2]['tones'][3]['score']
		u_agreeableness += agreeableness_score
		emotionrange_name = parsed_json["document_tone"]["tone_categories"][2]['tones'][4]['tone_name']
		emotionrange_score = parsed_json["document_tone"]["tone_categories"][2]['tones'][4]['score']
		u_emotionrange += emotionrange_score
	
	
	with open('results.txt', writeMode) as f: 
		f.write(str(u_anger / tweet_count)) # Anger
		f.write('\n' + str(u_disgust / tweet_count)) # Disgust
		f.write('\n' + str(u_fear / tweet_count)) # Fear
		f.write('\n' + str(u_joy / tweet_count)) # Joy
		f.write('\n' + str(u_sadness / tweet_count)) # Sadness
		f.write('\n' + str(u_analytical / tweet_count)) # Analytical
		f.write('\n' + str(u_confident / tweet_count)) # Confident
		f.write('\n' + str(u_tentative / tweet_count)) # Tentative
		f.write('\n' + str(u_openness / tweet_count)) # Openness
		f.write('\n' + str(u_conscientiousness / tweet_count)) # Conscientiousness
		f.write('\n' + str(u_extraversion / tweet_count)) # Extraversion
		f.write('\n' + str(u_agreeableness / tweet_count)) # Agreeableness
		f.write('\n' + str(u_emotionrange / tweet_count)) # Emotion Range
		f.write("\n"+userData.screen_name+'\n') # Name
		
analyzeTweets(userID1, 'w')
analyzeTweets(userID2, 'a')	
print('Completed')		
