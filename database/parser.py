from classes import *
class parser:
    def parseMovie(resultMovie):
        return movie(resultMovie[0],resultMovie[1],resultMovie[2],resultMovie[3],resultMovie[4],resultMovie[5],resultMovie[8],resultMovie[6],resultMovie[7])
    
    def parseUser(resultUser):
        return user(resultUser[0],resultUser[1],resultUser[2],resultUser[3],resultUser[4],resultUser[5],None,None)
    
    def parsePlaylist(resultPlaylist):
        return playlist(resultPlaylist[0],resultPlaylist[1],resultPlaylist[2],None)