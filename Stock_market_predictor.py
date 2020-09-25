import csv
import tweepy 
import matplotlib.pyplot as plt
from textblob import TextBlob
from keras.models import Sequential
from keras.layers import Dense

#Accessing twitter API
consumer_key = '8hdf1xgTUc8hjVjMHeDK9EOEI'
consumer_key_secret = 'jwCNfbhyZZATWTxlLP4tSi1UG2j2jLS0rNQ8bvGE0JcO8xN63k'

access_token = '1292179748790194177-dcVvw8tVYfv3Is8HEeP3oMzqcvC8Iw'
access_token_secret = 'pMkgiW4jaJ44HqQAoDlKqrFDf7AJ9HsTFuVEBC79L61rA'

auth = tweepy.OAuthHandler(consumer_key,consumer_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

#Loading 'apple stock' tweets 
tweets = api.search('apple stock')

#Finding percentage of positive tweets 
polarities = [TextBlob(tweet.text).polarity for tweet in tweets]
NbPosTweets = sum([int(polarity>0) for polarity in polarities])
PosTweetPercentage = NbPosTweets/len(polarities)

#Input positive tweet percentage threshold
threshold = float(input("Provide a threshold for percentage of positive tweets as a number between 0 and 1: "))

#Terminate program if positive tweet percentage is less than threshold
if PosTweetPercentage<threshold:
	print("The percentage of positive tweets was less than {}".format(threshold))
	exit()

def get_data(filename):
	prices=[]
	nextDayPrices=[]
	with open(filename, 'r') as csvFile:
		csvReader = list(csv.reader(csvFile))[1:]
		csvFile.seek(0)
		csvReaderSize = len(list(csvFile))-1
		#for row in csvReader:
		for i in range(csvReaderSize-1):
			#Use only the open price
			prices.append(float(csvReader[i][1]))
			nextDayPrices.append(float(csvReader[i+1][1]))		
	return prices, nextDayPrices

#Setting Sequential model with two layers and 10 neurons
model = Sequential()
model.add(Dense(10,input_dim=1))#One dimensional input (stock price)
model.add(Dense(1))#One dimensional output (predicted stock price)

#Compiling model (I still don't know how to choose optimal loss or optimizer)
model.compile(loss='mean_squared_error', optimizer='adam')

#Generating data
prices, nextDayPrices = get_data('apple.csv')

#Training model (I still don't know how to choose optimal batch_size or epochs)
model.fit(prices, nextDayPrices, batch_size=10, epochs=1000, verbose=0)
	
#Predicting stock price for following day
lastPrice = nextDayPrices[-1]
nextDayPrice = model.predict([lastPrice]) #The input here must be a list

#Printing prediction for following day
print("The predicted price of Apple stock for tomorrow is {}".format(nextDayPrice[0][0]))
	
#Plotting the results
plt.plot(prices)
plt.show()

