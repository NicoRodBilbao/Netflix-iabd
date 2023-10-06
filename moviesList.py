import webbrowser
from database.dbContext import *
from database.parser import *
class moviesList:
    def __init__(self):
        pass
    
    def initializePage(self):
        movieList = ""
        page = open(f"MoviesList.html","w")
        context = dbContext('movies')
        resultMovies = context.selectAllColumns()
        
        for resultMovie in resultMovies:
            movie = parser.parseMovie(resultMovie)
            movieList += f"""<div class="movie">
                        <img src="./multimedia/{movie.movie_image}Bg.png" alt="movie" class="image">
                        <div class="overlay">
                            <span class="text">{movie.title}</span>
                        </div>
                </div>"""
            
        content = f"""<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8" />
                    <link rel="stylesheet" href="netflixStyleSheet.css" />
                    <title>Movies</title>
                </head>
                <header class="headerStyle">
                    <img src="./multimedia/logo.png" class="logo"/>
                    <button>Pelis</button>
                    <button>Listas</button>
                    <img src="./multimedia/pfp.jpg" class="pfp"/>
                </header>
                <body>
                    <div id="moviesContainer">
                        {movieList}
                    </div>
                </body>
            </html>
        """
        page.write(content)
        page.close()
        webbrowser.open_new_tab("MoviesList.html")