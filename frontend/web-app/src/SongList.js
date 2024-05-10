import React, { useEffect, useState, useRef } from "react";
import StarRating from "./StarRating";
import LogoutButton from "./LogoutButton";

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
        setRecommendedSongs(data.recommended_songs); // Update state with the recommended songs
      })
      .catch((error) =>
        console.error("Failed to fetch recommendations:", error)
      );
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
      audioRef.current.src = `/audio/${song.id}`; // Adjusted to your file path setup
      audioRef.current
        .play()
        .catch((e) => console.error("Error playing audio:", e));
    }
  };

  // In the JSX, call handleRating when a star is clicked

  useEffect(() => {
    fetch("/api/songs")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text(); // First get the text of the response
      })
      .then((text) => {
        return JSON.parse(text); // Then parse the text as JSON
      })
      .then((data) => {
        setSongs(data);
        return fetch("/api/ratings");
      })
      .then((response) => response.json())
      .then((data) => {
        console.log("Ratings fetched:", data);
        setRatings(data);
      })
      .catch((error) => {
        console.error("Error fetching songs:", error);
      });
  }, []);

  return (
    <div>
      <LogoutButton />
      <h2>Songs</h2>
      <button onClick={fetchRecommendations}>Get Recommendations</button>
      <ul>
        {songs.map((song) => (
          <li key={song.id}>
            {song.title} by {song.artist}
            <button onClick={() => onSelectSong(song)}>Play</button>
            <StarRating
              songId={song.id}
              onChange={handleRating}
              initialRating={ratings[song.id] || 0}
            />
          </li>
        ))}
      </ul>
      <audio ref={audioRef} controls />
      <h2>Recommended Songs</h2>
      <ul>
        {recommendedSongs.map((song, index) => (
          <li key={song.id || index}>
            {song.title} by {song.artist}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SongList;
