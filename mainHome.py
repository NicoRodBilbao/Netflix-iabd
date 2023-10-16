from classes import *
from database.dbContext import *
from flask import Flask, render_template, request
from database.parser import *

app = Flask(__name__)


def getUser(username,password):
    try:
        context = dbContext("users")
        result = context.selectAllColumns("username",username)
        user = parser.parseUser(result[0])
        print(user.username)
        print(user.password)
        if(password == user.password):
            global curUser
            curUser = user
            return True
        else:
            return False
    except:
        return False
    

    # correo,pasw,uname,ntef,rol"""

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/getLogin', methods=['POST','GET'])
def getLogin():
    if request.method == "POST":
        username = request.form["uname"]
        password = request.form["passw"]
        flag = getUser(username,password)
        if flag:
            if   curUser.role == "user":
                return movieList()
            elif curUser.role == "": # Insert accountability role
                return movieList()   # Return accountability html
        else:
            return render_template('login.html')
    
@app.route('/movies')
def movieList():
    context = dbContext('movies')
    resultMovies = context.selectAllColumns()
    my_movies = []
    for movie in resultMovies:
        my_movies.append(parser.parseMovie(movie))
    return render_template('moviesList.html',movies=my_movies)

@app.route("/movie/<int:movie_id>")
def movieData(movie_id):
    context = dbContext('movies')
    my_movie = parser.parseMovie(context.selectById(movie_id))
    return render_template('movieData.html',movie=my_movie)

@app.route('/playlists')
def playlists():
    context = dbContext('playlists')
    resultPlaylists = context.selectByInt("user_id",curUser.user_id)
    my_playlists = []
    for playlist in resultPlaylists:
        my_playlists.append(parser.parsePlaylist(playlist))
    return render_template('lists.html',playlists=my_playlists)

@app.route('/playlists/<int:playlist_id>/movies')
def playlistMovies(playlist_id):
    context = dbContext('movies')
    resultMovies = context.selectAllPlaylistMovies(playlist_id)
    my_movies = []
    for movie in resultMovies:
        my_movies.append(parser.parseMovie(movie))
    return render_template('moviesList.html',movies=my_movies)
    
@app.route('/playlists/createPlaylist', methods=['POST'])
def createPlaylist():
    playlistName = request.form["playlistName"]
    context = dbContext('playlists')
    context.insert([str(curUser.user_id),"\'"+playlistName+"\'"])
    return playlists()
    
if __name__ == '__main__':
    app.run()