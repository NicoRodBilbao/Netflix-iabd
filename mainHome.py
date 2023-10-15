from classes import *
from database.dbContext import *
from flask import Flask, render_template, request

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/getLogin', methods=['POST','GET'])
def getLogin():
    if request.method == "POST":
        username = request.form["uname"]
        password = request.form["passw"]
        flag = getUser(username,password)
        if flag:
            return render_template('moviesList.html')
        else:
            return render_template('login.html')
        
    
if __name__ == '__main__':
    app.run()
    
"""import webbrowser

def helloWorld():
    page = open(f"./Proyecto/Netflix-iabd/Login.html","w")
    
    content = 
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset='utf-8'>
            <title>Netflix - Log in</title>
            <link rel='stylesheet' type='text/css' media='screen' href='css.css'>
        </head>
        <body>
            <header class="headerStyle">
                <img src=".\logo.png" class="logo"/>
                <button>Pelis</button>
                <button>Listas</button>
                <img src="./pfp.png" class="pfp"/>
            </header>
            <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
            <div class="center">
                <form>
                    <h1>Iniciar sesión</h1>       <br/>
                        <input type="text" id="uname" name="uname" placeholder="Usuario">     <br/><br/>
                    <input type="password" id="passw" name="passw" placeholder="Contraseña"> <br/><br/><br/>
                    <button type="submit">Iniciar sesión</button>
                </form>
            </div>
        </body>
    </html>
    
    
    page.write(content)
    page.close()
    webbrowser.open_new_tab("./Proyecto/Netflix-iabd/Login.html")"""