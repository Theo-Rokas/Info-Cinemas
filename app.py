from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response, render_template
import json
import os

# Connect to our local MongoDB
mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

# Choose InfoCinemas database
db = client["InfoCinemas"]
users = db["Users"]
movies = db["Movies"]

# Initiate Flask App
app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("base.html")


@app.route("/insertuser", methods=["POST", "GET"])
def insert_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if not name or not email or not password:
            return Response("Fields are required", status=500, mimetype="application/json")

        same_users = list(users.find({"email": email}))

        if len(same_users) == 0:
            all_users = list(users.find({}))
            is_admin = False

            if len(all_users) == 0:
                is_admin = True

            user = {"name": name,
                    "email": email,
                    "password": password,
                    "movies_seen": [],
                    "connected": False,
                    "admin": is_admin}

            users.insert_one(user)

            return Response("User was added to the mongodb successfully", status=200, mimetype='application/json')
        else:
            return Response("User with this email already exists", status=200, mimetype='application/json')

    return render_template("insert-user.html")


@app.route("/connectuser", methods=["POST", "GET"])
def connect_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if not email or not password:
            return Response("Fields are required", status=500, mimetype="application/json")

        if users.find_one({"email": email, "password": password}):
            users.update_one(
                {"email": email, "password": password},
                {"$set":
                    {
                        "connected": True,
                    }
                 }
            )

            return Response("Connected successfully", status=500, mimetype="application/json")
        else:
            return Response("Email or password are not valid", status=500, mimetype="application/json")

    return render_template("connect-user.html")


@app.route("/<string:email>/searchmovie/<string:title>", methods=["POST", "GET"])
def search_movie(email, title):
    if email == None or title == None:
        return Response("Bad request", status=500, mimetype='application/json')

    user = users.find_one({"email": email})
    same_movies = list(movies.find({"title": title}))

    if user == None:
        return Response("No user found with the email " + email, status=500, mimetype="application/json")

    if len(same_movies) == 0:
        return Response("No movies found with the title " + title, status=500, mimetype="application/json")

    connected = user["connected"]

    if not connected:
        return Response("Not connected, connect first and try again", status=500, mimetype="application/json")

    newer = 0
    for movie in same_movies:
        year = movie["year"]
        if newer == 0:
            newer = year
        if year > newer:
            newer = year

    newer_movie = movies.find_one({"title": title, "year": newer})

    if request.method == "POST":
        screening = request.form["screening"]
        tickets = int(request.form["tickets"])

        if not screening or not tickets:
            return Response("Fields are required", status=500, mimetype="application/json")

        all_screenings = newer_movie["dates"]["screening"]
        all_tickets = newer_movie["dates"]["tickets"]

        pos = 0
        for i, day_screening in enumerate(all_screenings):
            if day_screening == screening:
                pos = i
                break
            else:
                pos = -1

        if pos == -1:
            return Response("You can't watch this movie on " + screening, status=500, mimetype="application/json")

        for j, day_tickets in enumerate(all_tickets):
            if j == pos:
                tickets_left = day_tickets
                final_tickets = day_tickets - tickets

                if final_tickets < 0:
                    return Response("Not enough tickets for you to buy, only " + str(tickets_left) + " left", status=500, mimetype="application/json")

                all_tickets[j] = final_tickets

        final_dates = {"screening": all_screenings,
                       "tickets": all_tickets}

        prev_movies = user["movies_seen"]
        prev_movies.append(movie["title"])

        movies.update_one(
            {"title": title, "year": newer},
            {"$set":
                {
                    "dates": final_dates
                }
             }
        )

        users.update_one(
            {"email": email},
            {"$set":
                {
                    "movies_seen": prev_movies
                }
             }
        )

        return Response("Transaction completed, enjoy the movie", status=500, mimetype="application/json")

    return render_template("search-movie.html", movie=newer_movie)


@app.route("/<string:email>/showhistory", methods=["GET"])
def show_history(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')

    user = users.find_one({"email": email})

    if user == None:
        return Response("No user found with the email " + email, status=500, mimetype="application/json")

    connected = user["connected"]

    if not connected:
        return Response("Not connected, connect first and try again", status=500, mimetype="application/json")

    movies_seen = user["movies_seen"]

    return render_template("show-history.html", movies_seen=movies_seen)


@app.route("/<string:email>/insertmovie", methods=["POST", "GET"])
def insert_movie(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')

    user = users.find_one({"email": email})

    if user == None:
        return Response("No user found with the email " + email, status=500, mimetype="application/json")

    admin = user["admin"]

    if not admin:
        return Response("Only admins can perform this operation", status=500, mimetype="application/json")

    if request.method == "POST":
        title = request.form["title"]
        year = int(request.form["year"])
        description = request.form["description"]
        dates = request.form["dates"]

        if not title or not year or not description or not dates:
            return Response("Fields are required", status=500, mimetype="application/json")

        dates_list = []
        dates_list = dates.split(", ")

        tickets_list = []
        for _ in dates_list:
            tickets_list.append(50)

        final_dates = {"screening": dates_list,
                       "tickets": tickets_list}

        movie = {"title": title,
                 "year": year,
                 "description": description,
                 "dates": final_dates}

        movies.insert_one(movie)

        return Response("Movie was added to the mongodb successfully", status=200, mimetype='application/json')

    return render_template("insert-movie.html")


@app.route("/<string:email>/deletemovie/<string:title>", methods=["DELETE", "GET"])
def delete_movie(email, title):
    if email == None or title == None:
        return Response("Bad request", status=500, mimetype="application/json")

    user = users.find_one({"email": email})
    same_movies = list(movies.find({"title": title}))

    if user == None:
        return Response("No user found with the email " + email, status=500, mimetype="application/json")

    if len(same_movies) == 0:
        return Response("No movie found with the title " + title, status=500, mimetype="application/json")

    admin = user["admin"]

    if not admin:
        return Response("Only admins can perform this operation", status=500, mimetype="application/json")

    older = 0
    for movie in same_movies:
        year = movie["year"]
        if older == 0:
            older = year
        if year < older:
            older = year

    movies.delete_one({"title": title, "year": older})

    return Response("Movie deleted successfully", status=500, mimetype="application/json")


@app.route("/<string:email>/updatemovie/<string:title>", methods=["POST", "GET"])
def update_movie(email, title):
    if email == None or title == None:
        return Response({"Bad request"}, status=500, mimetype="application/json")

    user = users.find_one({"email": email})
    same_movies = list(movies.find({"title": title}))

    if user == None:
        return Response("No user found with the email " + email, status=500, mimetype="application/json")

    if len(same_movies) == 0:
        return Response("No movie found with the title " + title, status=500, mimetype="application/json")

    admin = user["admin"]

    if not admin:
        return Response("Only admins can perform this operation", status=500, mimetype="application/json")

    older = 0
    for movie in same_movies:
        year = movie["year"]
        if older == 0:
            older = year
        if year < older:
            older = year

    if request.method == "POST":
        post_title = request.form["title"]
        year = int(request.form["year"])
        description = request.form["description"]
        dates = request.form["dates"]

        if not post_title or not year or not description or not dates:
            return Response("Fields are required", status=500, mimetype="application/json")

        dates_list = []
        dates_list = dates.split(", ")

        tickets_list = []
        for _ in dates_list:
            tickets_list.append(50)

        final_dates = {"screening": dates_list,
                       "tickets": tickets_list}

        movies.update_one(
            {"title": title, "year": older},
            {"$set":
                {
                    "title": post_title,
                    "year": year,
                    "description": description,
                    "dates": final_dates
                }
             }
        )

        return Response("Movie was updated to the mongodb successfully", status=200, mimetype='application/json')

    return render_template("update-movie.html")


@app.route("/<string:email>/makeadmin", methods=["POST", "GET"])
def make_admin(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')

    user = users.find_one({"email": email})

    if user == None:
        return Response("No user found with the email " + email, status=500, mimetype="application/json")

    admin = user["admin"]

    if not admin:
        return Response("Only admins can perform this operation", status=500, mimetype="application/json")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if not email or not password:
            return Response("Fields are required", status=500, mimetype="application/json")

        if users.find({"email": email, "password": password}):
            users.update_one(
                {"email": email, "password": password},
                {"$set":
                    {
                        "admin": True,
                    }
                 }
            )

            return Response("User is now Admin", status=200, mimetype='application/json')

    return render_template("make-admin.html")


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
