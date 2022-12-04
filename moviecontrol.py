from moviemodel import conn_mysqldb


class search():

    @staticmethod
    def find(movieName):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM save_movie_info WHERE movieName = '" + \
            str(movieName) + "'"
        db_cursor.execute(sql)
        movieOne = db_cursor.fetchone()
        if not movieOne:
            print("movieName없음")
            return None
        else:
            movie = movieOne[0]
            print("movieName = ", movie)
            return movie

    @staticmethod
    def getMovieInfo(movieName):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM save_movie_info WHERE movieName = '" + \
            str(movieName) + "'"
        db_cursor.execute(sql)
        movieOne = db_cursor.fetchone()
        if not movieOne:
            print("movieName없음")
            return None
        else:
            movieTitle = movieOne[0]
            movieNation = movieOne[1]
            movieTime = movieOne[2]
            movieCoach = movieOne[3]
            movieActor = movieOne[4]
            movieText = movieOne[5]
            movieGenre = movieOne[6]
            movieEng = movieOne[7]
            movieDetail = [movieTitle, movieNation, movieTime,
                           movieCoach, movieActor, movieText, movieGenre, movieEng]
            return movieDetail


class movieSession():
    @staticmethod
    def save_movie_info(movieName, movieNation, movieTime, movieCoach, movieActor, movieText, movieGenre, movieEng):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "INSERT INTO save_movie_info (movieName, movieNation, movieTime, movieCoach, movieActor, movieText, movieGenre, movieEng) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            str(movieName), str(movieNation), int(movieTime), str(movieCoach), str(movieActor), str(movieText), str(movieGenre), str(movieEng))
        save = db_cursor.execute(sql)
        mysql_db.commit()
        return save
