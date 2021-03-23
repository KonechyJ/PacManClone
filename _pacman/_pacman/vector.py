from math import sqrt

#start of vector class and variables used in the functions below
class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.000001
    #Simply can add and subtract vectors
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    #functions to address a negative vector
    def __neg__(self):
        return Vector2(-self.x, -self.y)

    ##Simply can multiply and and divide vectors
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    #Python 3 uses trueDiv
    def __truediv__(self, scalar):
        return self.__div__(scalar)

    #This function allows us to say the two numbers that are extremely similar( but technically different) are actually the same
    # Ex.) 3 == 3.000000001 if the type of comparison this function would allow
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    #returns the hash Id to be used whenever needed
    def __hash__(self):
        return id(self)

    #This Function alternatively returns the length of the vector, without requiring a square root
    def magnitudeSquared(self):
        return self.x ** 2 + self.y ** 2

    # This functions allows us to return the actual length of a vector, while using the sqrt function
    def magnitude(self):
        return sqrt(self.magnitudeSquared())

    #This function takes the magnitude of a vector in order to return a normalized value
    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return self.__div__(mag)
        return None

    #this function returns the dot product of Vector Object
    def dot(self, other):
        return self.x * other.x, self.y * other.y

    #This method lets us make a copy of a vector and create a new instance of it
    def copy(self):
        return Vector2(self.x, self.y)

    #This function lets us convert our vectors into tuples
    def asTuple(self):
        return self.x, self.y

    #And this functions lets function lets us turn the function into an int tuple
    def asInt(self):
        return int(self.x), int(self.y)

    #This function is used to print out vectors for testing purpuses
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"