import React, { useEffect, useState } from "react";
import StarRating from "./StarRating";

function SongList({ onSelectSong }) {
  const [songs, setSongs] = useState([]);
  const [ratings, setRatings] = useState({});

  const handleRating = (songId, rating) => {
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
        console.log(data.message); // Or handle this message in your UI
      })
      .catch((error) => {
        console.error("Error posting rating:", error);
      });
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
        setRatings(data);
      })
      .catch((error) => {
        console.error("Error fetching songs:", error);
      });
  }, []);

  return (
    <div>
      <h2>Songs</h2>
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
    </div>
  );
}

export default SongList;
