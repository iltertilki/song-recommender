from flask import Flask, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import eyed3
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
import logging
from recommendations import enhanced_recommend


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b\xad\x07b\x9d\x06\xc1$\xc9\xd8\x85\x12\xed\xb9\xfd\xb1\xc2\x97\xdd\xd1\x02_\xb9R\xba'
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
logging.basicConfig(level=logging.INFO)

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the User model
    rating = db.Column(db.Integer, nullable=False)

    # Adding relationship to User
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))

class User(db.Model, UserMixin):
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
@login_required
def rate_song():
    data = request.get_json()
    rating = data.get('rating')
    song_id = data.get('song_id')
    
    logging.info(f"Received rating: {rating} for song ID: {song_id} from user ID: {current_user.id}")

    # Ensure the current user is logged in
    if not current_user.is_authenticated:
        return jsonify({'message': 'User not authenticated'}), 401

    # Check for existing rating by the user for the same song
    existing_rating = Rating.query.filter_by(song_id=song_id, user_id=current_user.id).first()
    if existing_rating:
        existing_rating.rating = rating
    else:
        new_rating = Rating(song_id=song_id, user_id=current_user.id, rating=rating)
        db.session.add(new_rating)
    
    db.session.commit()
    return jsonify({'message': 'Rating updated successfully'}), 200
    
@app.route('/api/ratings')
@login_required
def get_ratings():
    if not current_user.is_authenticated:
        return jsonify({'message': 'User not authenticated'}), 401
    
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    ratings_dict = {rating.song_id: rating.rating for rating in user_ratings}
    return jsonify(ratings_dict)

# Flask backend - app.py
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'User already exists'}), 400

    # Create new user
    new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True, 'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'authenticated': True, 'user': user.username}), 200
    else:
        return jsonify({'authenticated': False}), 401

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/recommendations', methods=['POST'])
@login_required
def generate_recommendations():
    data = request.get_json()
    song_indices = data.get('song_indices')
    ratings = data.get('ratings')
    
    # Fetch already rated song IDs by the current user to exclude from recommendations
    rated_song_ids = {rating.song_id for rating in Rating.query.filter_by(user_id=current_user.id).all()}
    print("Rated song ids are: ", rated_song_ids)
    
    try:
        recommendations = enhanced_recommend(song_indices, ratings, exclude_indices=rated_song_ids)
        recommendations = [int(song_id) for song_id in recommendations]
        app.logger.info(f"Recommendations generated: {recommendations}")
        return jsonify({'recommended_songs': recommendations}), 200
    except Exception as e:
        return jsonify({'message': 'Error generating recommendations', 'error': str(e)}), 500



@app.route('/api/songs/details', methods=['POST'])
def song_details():
    song_ids = request.json.get('song_ids', [])
    songs = Song.query.filter(Song.id.in_(song_ids)).all()
    song_data = [{'id': song.id, 'title': song.title, 'artist': song.artist} for song in songs]
    return jsonify(song_data)



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
