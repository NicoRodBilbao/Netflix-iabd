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
        user = getUser(username,password)
        if user is None:
            return render_template('login.html')
        else:
            return movieList(user.id)

# Route to display the list of movies
@app.route('/movies')
def movieList(myUserId):
    return render_template('moviesList.html',movies=getMovies(),userId=myUserId)

# Route to display details of a specific movie
@app.route("/movie/<int:myUserId>/<int:movieId>")
def movieData(movieId,myUserId):
    return render_template('movieData.html',movie=getMovieById(movieId), lists=getLists(myUserId),userId=myUserId)

# Route to add a movie to a playlist
@app.route("/addMovieToPlaylist/<int:playlistId>", methods=['POST'])
def addMovieToPlaylist(playlistId):
    movieId = request.form.get("movieId")
    userId = request.form.get("userId")
    insertMovieList(playlistId,movieId)
    return movieData(movieId,userId)

# Route to set a rating for a movie
@app.route("/setRating/<int:movieId>", methods=['POST'])
def setRating(movieId):
    rating = request.form.get("rating")
    userId = request.form.get("userId")
    insertRating(userId,movieId,rating)
    return movieData(movieId,userId)

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
def getLists(userId):
    try:
        context = dbContext("playlists")
        resultLists = context.selectByInt("user_id",userId)
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
            return user
        else:
            return None
    except:
        return None
    
# Function to insert or update an user's rating for a movie
def insertRating(userId,movieId,rating):
    try:
        context = dbContext('users_movies')
        context.insert([f"{userId}",f"{movieId}",f"{rating}"])
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