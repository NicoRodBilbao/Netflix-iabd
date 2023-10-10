from classes import *
class parser:
    def parseMovie(resultMovie):
        return movie(resultMovie[0],resultMovie[1],resultMovie[2],resultMovie[3],resultMovie[4],resultMovie[5],resultMovie[8],resultMovie[6],resultMovie[7])
    
    def parsePlaylist(resultList):
        return playlist(resultList[0],resultList[1],resultList[2],None)