# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_cors import CORS
import requests
import json
import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib
from flask import url_for
import os
from moviecontrol import movieSession, search
import configparser

app = Flask(__name__)
CORS(app)
config = configparser.ConfigParser()
config.read("config.ini")

kobisSecret = config["SECRET"]["KOBIS_SECRET"]
kmdbSecret = config["SECRET"]["KMDB_SECRET"]

nows = datetime.datetime.now()
year = str(nows.year)
month = nows.month
day = str(nows.day-1)

if (day == "0"):
    month -= 1
    month = str(month)
    if (month == "1", "3", "5", "7", "9", "11"):
        day = 31
        day = str(day)
    elif (month == "2"):
        day = 28
        day = str(day)
    else:
        day = 30
        day = str(day)
else:
    month = str(month)
if (len(str(day)) == 1):
    day = "0" + day
if (len(str(month)) == 1):
    month = "0" + month
if (month == "00"):
    month = "12"
print(year, month, day)

kmdbLists = []
url = "http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=" + \
    kobisSecret + "&targetDt=" + year + month + day
html = requests.get(url).text
datas = json.loads(html)

movieAudiAcc = []
movies = [[], [], [], [], []]
kmdbTitles = []
searchMovie = []


for i in range(len(datas["boxOfficeResult"]["dailyBoxOfficeList"])):
    # movieList.append(datas["boxOfficeResult"]["dailyBoxOfficeList"][i]["movieNm"])
    movies[0].append(datas["boxOfficeResult"]
                     ["dailyBoxOfficeList"][i]["movieNm"])
    opendb = datas["boxOfficeResult"]["dailyBoxOfficeList"][i]["openDt"]
    if (opendb != " "):
        opendb = int(''.join(list(filter(str.isdigit, opendb))))
        movies[4].append(opendb)
    else:
        movies[4].append("%")
    movieAudiAcc.append(datas["boxOfficeResult"]
                        ["dailyBoxOfficeList"][i]["audiAcc"])

for i in range(len(movies[0])):
    title = movies[0][i]
    newTitle = title.replace(" ", "")
    newTitle = newTitle.replace("-", "")
    newTitle = newTitle.replace(":", "")
    newTitle = newTitle.replace(",", "")
    newTitle = newTitle.replace("!", "")
    searchMovie.append(newTitle)


def saveMovie():
    for i in range(len(movies[0])):
        if (search.find(movies[0][i]) == None):
            if (movies[0][i] != search.find(movies[0][i])):
                title = movies[0][i]
                newTitle = searchMovie[i]
                kmdbUrl = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey=" + \
                    kmdbSecret + "&detail=N&query=" + \
                    quote(newTitle) + "&releaseDts=" + str(movies[4][i])
                request = urllib.request.Request(kmdbUrl)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
                response_body = response.read()
                dict = json.loads(response_body.decode('utf-8'))
                if (dict["TotalCount"] != 0):
                    result = dict["Data"][0]["Result"]
                    if (result):
                        movieTitle = movies[0][i]
                        movieEng = result[0]["titleEng"]
                        movieNation = result[0]["nation"]
                        movieTime = result[0]["runtime"]
                        movieCoach = result[0]["directors"]["director"][0]["directorNm"]
                        movieActors = result[0]["actors"]["actor"]
                        movieActor = ""
                        for actor in movieActors:
                            movieActor += actor['actorNm'] + " "
                        movieText = result[0]["plots"]["plot"][0]["plotText"]
                        movieText = movieText.replace("'", "")
                        movieGenre = result[0]["genre"]
                        print(i, movieTitle, movieEng, movieNation, movieTime,
                              movieCoach, movieActor, movieText, movieGenre)
                        movieSession.save_movie_info(
                            movieTitle, movieNation, movieTime, movieCoach, movieActor, movieText, movieGenre, movieEng)
                        return saveMovie()
                    else:
                        print("Error Code:" + rescode)
                else:
                    movieTItle = movies[0][i]
                    print("kmdb Error : ", movieTItle)
                    # movieSession.save_movie_info(movieTitle)


for movieAud in movieAudiAcc:
    exList = []
    if (int(movieAud) < 10000):
        # movieHuman.append(str(movieAud))
        movies[1].append(str(movieAud))

    elif (100000 > int(movieAud) >= 10000):
        num = 0
        for i in str(movieAud):
            exList.append(i)
            num += 1
            if(num == 3):
                break
        # movieHuman.append(str(exList[0]+"."+exList[1]+exList[2]) + "만")
        movies[1].append(str(exList[0]+"."+exList[1]+exList[2]) + "만")

    elif (1000000 > int(movieAud) >= 100000):
        num = 0
        for i in str(movieAud):
            exList.append(i)
            num += 1
            if(num == 3):
                break
        # movieHuman.append(str(exList[0]+exList[1]+"."+exList[2]) + "만")
        movies[1].append(str(exList[0]+exList[1]+"."+exList[2]) + "만")
    else:
        num = 0
        for i in str(movieAud):
            exList.append(i)
            num += 1
            if(num == 4):
                break
        # movieHuman.append(str(exList[0]+exList[1]+exList[2]+"."+exList[3]) + "만")
        movies[1].append(
            str(exList[0]+exList[1]+exList[2]+"."+exList[3]) + "만")


def getScoreImg(title):
    findUrl = "https://movie.naver.com/movie/search/result.naver?query=" + \
        quote(title) + "&section=all&ie=utf8"
    find_code = requests.get(findUrl)
    find_text = find_code.text
    find_soup = BeautifulSoup(find_text, 'lxml')
    myUrl = find_soup.find('ul', "search_list_1")

    imgLink = myUrl.select_one('a')["href"]
    naverid = imgLink.split('=')[1]
    url = "https://movie.naver.com/movie/bi/mi/basic.naver?code=" + \
        quote(naverid)
    sourceCode = requests.get(url)
    plainText = sourceCode.text
    soup = BeautifulSoup(plainText, 'lxml')

    score = soup.find('div', "star_score").find_all('em')
    if (score and len(score) > 3):
        scores = score[0].text + score[1].text + score[2].text + score[3].text
        scores = float(scores)
        # movieScore.append(scores)
        movies[2].append(scores)
    else:
        scores = 0.0
        # movieScore.append(scores)
        movies[2].append(scores)

    imgFind = soup.find_all('meta')
    imgTag = imgFind[10]
    imgSoup = BeautifulSoup(str(imgTag), 'lxml')
    imgGet = imgSoup.select_one('meta')['content']
    if imgGet == "https://ssl.pstatic.net/static/m/movie/icons/OG_270_270.png":
        imgGet = "./static/img/movieset/noImg.jpg"
    movies[3].append(imgGet)


for movie in movies[0]:
    getScoreImg(movie)

movieLength = int(len(movies[0]) - 4)

saveMovie()

photoList = []
for f in os.listdir('./static/img/movieimg'):
    photoList.append(f)

for i in range(len(searchMovie)):
    if (searchMovie[i] not in photoList):
        url = movies[3][i]
        savelocation = "./static/img/movieimg/" + \
            searchMovie[i] + ".jpg"
        urllib.request.urlretrieve(url, savelocation)


@ app.route("/")
def hello():
    return render_template("index.html", movie=movies, lens=movieLength, searchMovie=searchMovie, time=year + "-" + month + "-" + day + "기준")


@ app.route("/detail/<movieName>")
def detail(movieName):
    movieDetail = search.getMovieInfo(movieName)
    newTitle = movieDetail[0].replace(" ", "")
    newTitle = newTitle.replace("-", "")
    newTitle = newTitle.replace(":", "")
    newTitle = newTitle.replace(",", "")
    newTitle = newTitle.replace("!", "")
    searchMovie = newTitle
    return render_template("detail.html", movieDetail=movieDetail, searchMovie=searchMovie)


if __name__ == ("__main__"):
    app.run()
