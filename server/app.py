""" import pafy

url = 'https://www.youtube.com/watch?v=BTYAsjAVa3I'
video = pafy.new(url)

print(video.title)

print(video.thumb)
audiostreams = video.audiostreams
for a in audiostreams:
    print(a.bitrate, a.extension, a.get_filesize())

bestaudio = video.getbestaudio()
print(bestaudio.url) """
# print(audiostreams[2].url)
# audiostreams[1].download()
import pafy
from enum import unique
from flask import Flask, request, jsonify
from flask import json
from flask_cors.decorator import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    artist = db.Column(db.String(80), unique=False)
    src = db.Column(db.Text(80), unique=False)
    pic = db.Column(db.Text(length=None), unique=False)

    def __init__(self, title, artist, src, pic):
        self.title = title
        self.artist = artist
        self.src = src
        self.pic = pic


class MusicSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'artist', 'src', 'pic')


song_schema = MusicSchema()
songs_schema = MusicSchema(many=True)


@app.route("/<ytid>", methods=["POST"])
def process_link(ytid):
    url = f'https://www.youtube.com/watch?v={ytid}'
    video = pafy.new(url)
    bestAudio = video.getbestaudio()

    title = str(video.title)
    artist = str(video.username)
    src = str(bestAudio.url)
    pic = str(video.thumb)

    new_song = Music(title, artist, src, pic)
    db.session.add(new_song)
    db.session.commit()
    return jsonify({
        'Message': f'title {title} artist {artist} src {src} pic {pic} is inserted.'
    })


@app.route("/songs", methods=["GET"])
def get_songs():
    all_songs = Music.query.all()
    result = songs_schema.dump(all_songs)
    return jsonify(result)


@app.route("/songs/<id>", methods=["DELETE"])
def delete_song(id):
    song = Music.query.get(id)
    db.session.delete(song)
    db.session.commit()

    return song_schema.jsonify(song)


""" @app.route("/songs", methods=["POST"])
def add_song():
    title = request.json['title']
    artist = request.json['artist']
    src = request.json['src']
    pic = request.json['pic']

    new_song = Music(title, artist, src, pic)
    db.session.add(new_song)
    db.session.commit()
    return jsonify(new_song) """


if __name__ == "__main__":
    app.run(debug=True)
