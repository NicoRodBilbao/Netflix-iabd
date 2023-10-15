from classes import *

 # The parser class provides methods to parse database query results into corresponding class objects.
class parser:
    # Function to parse a database result into a Movie object.(id|title|rating|description|cost|earnings|movieImage|releaseDate|duration)
    def parseMovie(resultMovie):
        return movie(resultMovie[0],resultMovie[1],resultMovie[2],resultMovie[3],resultMovie[4],resultMovie[5],resultMovie[8],resultMovie[6],resultMovie[7])
    
    # Function to parse a database result into a Playlist object.(id|userId|playlistName|movies)
    def parsePlaylist(resultList):
        return playlist(resultList[0],resultList[1],resultList[2],None)
    
    # Function to parse a database result into a Subscription object.(id|subscriptionName|price|duration|quantity)
    def parseSub(resultSubs):
        return subscription(resultSubs[0],resultSubs[1],resultSubs[2],resultSubs[3],resultSubs[4])
    
    # Function to parse a database result into an User object.(id|email|password|username|phoneNumber|movies|subscriptions)
    def parseUser(resultUser):
        return user(resultUser[0],resultUser[1],resultUser[2],resultUser[3],resultUser[4],resultUser[5],None,None)