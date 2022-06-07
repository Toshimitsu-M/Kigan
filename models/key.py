#どちらも任意の文字列で大丈夫です
class key():
    SECRET_KEY = "g8wkf0pvje6m2unhgt3o"
    SALT = "762ifuw9fj5wxjkeu0de"

    def __init__(self, SECRET_KEY=None, SALT=None):
        self.SECRET_KEY = SECRET_KEY
        self.SALT = SALT
