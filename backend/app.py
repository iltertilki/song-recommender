from flask import Flask, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
import eyed3
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

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
    
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    # Add a user_id field if implementing user-specific ratings
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



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

@app.route('/rate', methods=['POST'])
def rate_song():
    data = request.get_json()
    song_id = data.get('song_id')
    rating = data.get('rating')

    if not song_id or not isinstance(song_id, int):
        return jsonify({'message': 'Invalid or missing song_id'}), 400
    
    if not rating or not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({'message': 'Invalid rating'}), 400

    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found'}), 404

    # Check if a rating already exists for this song
    existing_rating = Rating.query.filter_by(song_id=song_id).first()
    if existing_rating:
        existing_rating.rating = rating  # Update the existing rating
        db.session.commit()
        return jsonify({'message': 'Rating updated successfully'}), 200
    else:
        # Create a new rating if not exists
        new_rating = Rating(song_id=song_id, rating=rating)
        db.session.add(new_rating)
        db.session.commit()
        return jsonify({'message': 'Rating submitted successfully'}), 200
    
@app.route('/api/ratings')
def get_ratings():
    ratings = Rating.query.all()
    ratings_dict = {rating.song_id: rating.rating for rating in ratings}
    return jsonify(ratings_dict)




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
