from classes import *
from database.dbContext import *
from flask import Flask, render_template, request
from database.parser import *

app = Flask(__name__)

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
            elif curUser.role == "accountant": # Insert accountability role
                return accounting()   # Return accountability html
        else:
            return render_template('login.html')

# Route to display the list of movies
@app.route('/movies')
def movieList():
    return render_template('moviesList.html',movies=getMovies(),userId=curUser.id)

# Route to display details of a specific movie
@app.route("/movie/<int:movieId>")
def movieData(movieId):
    return render_template('movieData.html',movie=getMovieById(movieId),lists=getLists(),movieRating=getMovieRating(movieId))

# Route to add a movie to a playlist
@app.route("/addMovieToPlaylist/<int:playlistId>", methods=['POST'])
def addMovieToPlaylist(playlistId):
    movieId = request.form.get("movieId")
    insertMovieList(playlistId,movieId)
    return movieData(movieId)

# Route to set a rating for a movie
@app.route("/setRating/<int:movieId>", methods=['POST'])
def setRating(movieId):
    rating = request.form.get("rating")
    insertRating(movieId,rating)
    return movieData(movieId)

@app.route('/playlists')
def playlists():
    context = dbContext('playlists')
    resultPlaylists = context.selectByInt("user_id",curUser.id)
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
    context.insert([str(curUser.id),"\'"+playlistName+"\'"])
    return playlists()

# Route to display accounting information
@app.route('/accounting')
def accounting():
    myMovies = getMovies()
    mySubs = getSubs() 
    myMoviesCost = sum(movie.cost for movie in myMovies)
    myMoviesEarnings = sum(movie.earnings for movie in myMovies)
    myMoviesProfit = sum(movie.profit for movie in myMovies)
    mySubsQuantity = sum(sub.quantity for sub in mySubs)
    mySubsEarnings = sum(sub.earnings for sub in mySubs)
    myTotalEarnings = myMoviesEarnings + mySubsEarnings
    myTotalProfit = myTotalEarnings - myMoviesCost
    for movie in myMovies:
        movie.cost = f"{round(movie.cost,2):,}"
        movie.earnings = f"{round(movie.earnings,2):,}"
        movie.profit = f"{round(movie.profit,2):,}"
    for sub in mySubs:
        sub.earnings = f"{round(sub.earnings,2):,}"
    return render_template('accounting.html',movies=myMovies,subscriptions=mySubs,
                           tMoviesCost=f"{round(myMoviesCost,2):,}",tMoviesEarnings=f"{round(myMoviesEarnings,2):,}",tMoviesProfit=f"{round(myMoviesProfit,2):,}",
                           tSubsQuantity=f"{round(mySubsQuantity,2):,}",tSubsEarnings=f"{round(mySubsEarnings,2):,}",
                           totalEarnings=f"{round(myTotalEarnings,2):,}",totalProfit=f"{round(myTotalProfit,2):,}")

# Function to get the list of movies
def getMovieRating(movieId):
    try:
        context = dbContext('users_movies')
        return context.selectTwoConditions("rating",["user_id","movie_id"],[curUser.id,movieId])[0]
    except Exception as error:
        logging.error(error)
 
# Function to get the list of movies
def getMovies():
    try:
        context = dbContext('movies')
        resultMovies = context.selectAllColumns()
        movies = []
        for movie in resultMovies:
            movies.append(parser.parseMovie(movie))
        return movies
    except Exception as error:
        logging.error(error)

# Function to get the list of subscriptions
def getSubs():
    try:
        context = dbContext()
        resultSubs = context.selectSubsCount()
        subs = []
        for sub in resultSubs:
            subs.append(parser.parseSub(sub))   
        return subs
    except Exception as error:
        logging.error(error)

# Function to get the list of playlists for a specific user
def getLists():
    try:
        context = dbContext("playlists")
        resultLists = context.selectByInt("user_id",curUser.id)
        lists = []
        for list in resultLists:
            lists.append(parser.parsePlaylist(list))
        return lists
    except Exception as error:
        logging.error(error)

# Function to get details of a movie by its ID
def getMovieById(movieId):
    try:
        context = dbContext('movies')
        return parser.parseMovie(context.selectById(movieId))
    except Exception as error:
        logging.error(error)

def getUser(username,password):
    try:
        context = dbContext("users")
        result = context.selectAllColumns("username",username)
        user = parser.parseUser(result[0])
        if(password == user.password):
            global curUser
            curUser = user
            return True
        else:
            return False
    except:
        return False
    
# Function to insert or update an user's rating for a movie
def insertRating(movieId,rating):
    try:
        context = dbContext('users_movies')
        context.insert([f"{curUser.id}",f"{movieId}",f"{rating}"])
    except Exception as error:
        logging.error(error)  

# Function to insert a movie into a playlist
def insertMovieList(playlistId,movieId):
    try:
        context = dbContext('movies_playlists')
        context.insert([f"{movieId}",f"{playlistId}"])
    except Exception as error:
        logging.error(error)

if __name__ == '__main__':
    app.run()