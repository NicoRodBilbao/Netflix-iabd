# Generic class template

class movie:
    def __init__(self,id,title,rating,description,cost,earnings,movieImage,releaseDate,duration):
        self.id = id
        self.title = title
        self.rating = rating
        self.description = description
        self.cost = cost
        self.earnings = earnings
        self.movieImage = movieImage
        self.releaseDate = releaseDate
        self.duration = duration
        self.profit = earnings - cost
        
class playlist:
    def __init__(self,id,userId,playlistName,movies):
        self.id = id
        self.userId = userId
        self.playlistName = playlistName
        self.movies = movies
        
class subscription:
    def __init__(self,id,subscriptionName,price,duration,quantity):
        self.id = id
        self.subscriptionName = subscriptionName
        self.price = price
        self.duration = duration
        self.quantity = quantity
        self.earnings = price*quantity
        
class user:
    def __init__(self,id,email,password,username,phoneNumber,role,movies,subscriptions):
        self.id = id
        self.email = email
        self.password = password
        self.username = username
        self.phoneNumber = phoneNumber
        self.role = role
        self.movies = movies
        self.subscriptions = subscriptions