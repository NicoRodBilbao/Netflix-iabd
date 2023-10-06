import webbrowser

class movieData:
    def __init__(self,movie):
        self.movie = movie
        
    def initializePage(self):
        page = open(f"{self.movie.title.replace(' ', '')}Data.html","w")
        content = f"""<!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8"/>
                <link rel="stylesheet" href="netflixStyleSheet.css"/>
                <title>{self.movie.title}</title>
            </head>
            <body>
                <div id="mdContainer" style="background-image: url('./multimedia/{self.movie.movie_image}')">
                    <div id="dataContainer">
                        <p id="title">{self.movie.title}</p>
                        <p id="dataText">{self.movie.release_date} &#160-&#160 {self.movie.duration}min &#160-&#160 {self.movie.rating} <img src="./multimedia/star.png" width="18px"/></p>
                        <p id="descriptionText">
                            {self.movie.description}
                        </p>    
                    </div>
                </div>
            </body>
        </html>
        """
        page.write(content)
        page.close()
        webbrowser.open_new_tab(f"{self.movie.title.replace(' ', '')}Data.html")