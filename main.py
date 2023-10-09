from database.dbContext import *
from flask import Flask,render_template
from database.parser import *

#clase = myClass("Haizea")
#helloWorld(clase.name)
#openSignUp()

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()