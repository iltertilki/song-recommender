from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import eyed3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=True)
    file_path = db.Column(db.String(500), nullable=False)  # Adjust the length as necessary

    def __repr__(self):
        return f'<Song {self.title}, {self.artist}, {self.file_path}>'


# Ensure the tables are created
with app.app_context():
    db.create_all()

@app.route('/api/test')
def test():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/songs')
def list_songs():
    songs = Song.query.all()  # Retrieves all songs from the database
    return jsonify([
        {'id': song.id, 'title': song.title, 'artist': song.artist, 'file_path': song.file_path} for song in songs
    ])

@app.route('/audio/<int:song_id>')
def serve_audio(song_id):
    song = Song.query.get(song_id)
    if song:
        return send_from_directory(os.path.dirname(song.file_path), os.path.basename(song.file_path))
    else:
        return "Song not found", 404



def populate_database(root_directory):
    count = 0
    for subdir, dirs, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith('.mp3'):
                file_path = os.path.join(subdir, filename)
                try:
                    audiofile = eyed3.load(file_path)
                    if audiofile and audiofile.tag:
                        title = audiofile.tag.title or 'Unknown Title'
                        artist = audiofile.tag.artist or 'Unknown Artist'
                        existing_song = Song.query.filter_by(file_path=file_path).first()  # Check by file path
                        if not existing_song:
                            new_song = Song(title=title, artist=artist, file_path=file_path)
                            db.session.add(new_song)
                            count += 1
                            if count % 100 == 0:  # Commit for every 100 added songs
                                db.session.commit()
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    db.session.commit()  # Final commit if there are any remaining songs

if __name__ == '__main__':
    #with app.app_context():  # Set up an application context
        # Uncomment the following line when you want to populate the database
        #populate_database('./data')
    app.run(debug=True, port=5000)
