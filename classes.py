# Generic class template
# !COMMENT WHEN CODING STARTS
"""class myClass:
    def __init__(self, name):
        self.name = name
        self.sample = "Text"
        
        # Here you add extra attributes
    def method(string):
        "".__add__(string,".")"""

# Here start the actual classes

class movie:
    def __init__(self,title,description,cost,earnings,movie_image):
        self.title = title
        self.description = description
        self.cost = cost
        self.earnings = earnings
        self.movie_image = movie_image
        
class playlist:
    def __init__(self,userId,playlistName,movies):
        self.userId = userId
        self.playlistName = playlistName
        self.movies = movies
        
class subscription:
    def __init__(self,subscriptionName,price,duration):
        self.subscriptionName = subscriptionName
        self.price = price
        self.duration = duration
        
class user:
    def __init__(self,email,password,username,phoneNumber,role,movies,subscriptions):
        self.email = email
        self.password = password
        self.username = username
        self.phoneNumber = phoneNumber
        self.role = role
        self.movies = movies
        self.subscriptions = subscriptions