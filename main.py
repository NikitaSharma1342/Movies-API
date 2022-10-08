from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    type_of_movie = db.Column(db.String(20), nullable=False)
    ratings = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    directors = db.Column(db.String(200), nullable=False)
    main_lead_actors = db.Column(db.String(500), nullable=False)
    date_of_release = db.Column(db.String(80), nullable=False)

    def __init__(self, name, genre, type_of_movie, ratings,
                 description, directors, main_lead_actors, date_of_release):
        self.name = name
        self.genre = genre
        self.type_of_movie = type_of_movie
        self.ratings = ratings
        self.description = description
        self.directors = directors
        self.main_lead_actors = main_lead_actors
        self.date_of_release = date_of_release

    def __repr__(self):
        return f"{self.name} | {self.ratings} | {self.description}"

db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/addMovie', methods=['POST'])
def add_movie():
    content_type = request.headers.get('Content-type')
    if content_type == 'application/json':
        name = request.json["name"]
        genre = request.json["genre"]
        type_of_movie = request.json["type_of_movie"]
        ratings = request.json["ratings"]
        description = request.json["description"]
        directors = request.json["directors"]
        main_lead_actors = request.json["main_lead_actors"]
        date_of_release = request.json["date_of_release"]

        new_movie = Movie(name=name, genre=genre, type_of_movie=type_of_movie,
                          ratings=ratings, description=description, directors=directors,
                          main_lead_actors=main_lead_actors, date_of_release=date_of_release)

        db.session.add(new_movie)
        db.session.commit()

        return jsonify(name= new_movie.name,
                       ratings= new_movie.ratings,
                       status = "Added the movie successfully")
@app.route('/getHighRatedMovies')
def get_high_rated_movies():
    all = Movie.query.filter(Movie.ratings>8).all()
    result = ""
    for a in all:
        result = result + a.name+"\n"

    return result


@app.route('/updateMovieList', methods=['PATCH'])
def update_movies():
    content_type = request.headers.get('Content-type')
    if content_type == 'application/json':
        movie_to_update_name = request.json["name"]
        movie_to_update = Movie.query.filter_by(name = movie_to_update_name).first()

        updated_name = request.json['updated-name']
        updated_rating = request.json["updated-ratings"]

        movie_to_update.name = updated_name
        movie_to_update.ratings = updated_rating


        db.session.commit()
        return "Successfully Updated"


@app.route('/delete', methods = ['DELETE'])
def delete():
    content_type = request.headers.get('Content-type')
    if content_type == 'application/json':
        movie_to_delete_name = request.json['name']
        movie_to_delete = Movie.query.filter_by(name = movie_to_delete_name).first()
        db.session.delete(movie_to_delete)
        db.session.commit()
        return f"Successfully deleted {movie_to_delete.name}."



if __name__ == "__main__":
    app.run(debug=True)
