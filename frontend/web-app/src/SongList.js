import React, { useEffect, useState, useRef } from "react";
import StarRating from "./StarRating";
import LogoutButton from "./LogoutButton";
import "./SongList.css";

function SongList() {
  const [songs, setSongs] = useState([]);
  const [ratings, setRatings] = useState({});
  const [recommendedSongs, setRecommendedSongs] = useState([]);

  const audioRef = useRef(null);

  const fetchRecommendations = () => {
    const songIndices = Object.keys(ratings).map((id) => parseInt(id));
    const ratingsValues = Object.values(ratings);

    fetch("/recommendations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        song_indices: songIndices,
        ratings: ratingsValues,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Recommendation IDs received:", data.recommended_songs);
        fetchSongDetails(data.recommended_songs);
      })
      .catch((error) =>
        console.error("Failed to fetch recommendations:", error)
      );
  };

  const fetchSongDetails = (songIds) => {
    fetch(`/api/songs/details`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ song_ids: songIds }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Song details fetched:", data);
        const orderedData = songIds.map((id) =>
          data.find((song) => song.id === id)
        );
        setRecommendedSongs(orderedData);
      })
      .catch((error) => {
        console.error("Error fetching song details:", error);
      });
  };

  const handleRating = (rating, songId) => {
    fetch("/rate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ song_id: songId, rating: rating }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Network response was not ok.");
      })
      .then((data) => {
        setRatings((prevRatings) => ({ ...prevRatings, [songId]: rating }));
      })
      .catch((error) => {
        console.error("Error posting rating:", error);
      });
  };

  const onSelectSong = (song) => {
    if (audioRef.current) {
      audioRef.current.src = `/audio/${song.id}`;
      audioRef.current
        .play()
        .catch((e) => console.error("Error playing audio:", e));
    }
  };

  useEffect(() => {
    fetch("/api/songs")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((text) => JSON.parse(text))
      .then((data) => {
        setSongs(data);
        return fetch("/api/ratings");
      })
      .then((response) => response.json())
      .then((data) => {
        setRatings(data);
      })
      .catch((error) => {
        console.error("Error fetching songs:", error);
      });
  }, []);

  return (
    <div className="song-list-container">
      <LogoutButton />
      <h2 className="recommended-songs-title">Recommended Songs</h2>
      <button className="song-list-button" onClick={fetchRecommendations}>
        Get Recommendations
      </button>
      <ul className="recommended-songs-list">
        {recommendedSongs.map((song) => (
          <li key={song.id} className="song-item">
            {song.title} by {song.artist}
            <button className="play-button" onClick={() => onSelectSong(song)}>
              Play
            </button>
            <StarRating
              songId={song.id}
              onChange={(rating) => handleRating(rating, song.id)}
              initialRating={ratings[song.id] || 0}
            />
          </li>
        ))}
      </ul>
      <audio ref={audioRef} controls />
      <h2 className="song-list-title">Songs</h2>
      <ul className="song-list">
        {songs.map((song) => (
          <li key={song.id} className="song-item">
            {song.title} by {song.artist}
            <button className="play-button" onClick={() => onSelectSong(song)}>
              Play
            </button>
            <StarRating
              songId={song.id}
              onChange={handleRating}
              initialRating={ratings[song.id] || 0}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SongList;
