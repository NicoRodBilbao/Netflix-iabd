from classes import *
from database.dbContext import *
from flask import Flask, render_template, request
from database.parser import *

app = Flask(__name__)

def getUser(username,password):
    try:
        context = dbContext("users")
        result = context.selectAllColumns("username",username)
        user = parseUser(result[0])
        print(user.username)
        print(user.password)
        if(password == user.password):
            return True
        else:
            return False
    except:
        return False
    
def parseUser(resultUser):
    return user(resultUser[1],resultUser[2],resultUser[3],resultUser[4],resultUser[5],None,None)
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
            return movieList()
        else:
            return render_template('login.html')
    
@app.route('/movies')
def movieList():
    context = dbContext('movies')
    resultMovies = context.selectAllColumns()
    myMovies = []
    for movie in resultMovies:
        myMovies.append(parser.parseMovie(movie))
    return render_template('moviesList.html',movies=myMovies)

@app.route("/movie/<int:movie_id>")
def movieData(movie_id):
    contextMovies = dbContext('movies')
    contextLists = dbContext('playlists')
    myMovie = parser.parseMovie(contextMovies.selectById(movie_id))
    resultLists = contextLists.selectAllColumns()
    myLists = []
    for list in resultLists:
        myLists.append(parser.parsePlaylist(list))
    return render_template('movieData.html',movie=myMovie, lists=myLists)

@app.route('/accounting')
def accounting():
    context = dbContext('movies')
    resultMovies = context.selectAllColumns()
    resultSubs = context.selectSubsCount()
    myMovies = []
    for movie in resultMovies:
        myMovies.append(parser.parseMovie(movie))
    mySubs = []
    for sub in resultSubs:
        mySubs.append(parser.parseSub(sub))    
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
    
if __name__ == '__main__':
    app.run()