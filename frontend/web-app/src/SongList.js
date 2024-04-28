import React, { useEffect, useState } from "react";

function SongList({ onSelectSong }) {
  const [songs, setSongs] = useState([]);

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
      })
      .catch((error) => {
        console.error("Error fetching songs:", error);
      });
  }, []);

  return (
    <div>
      <h2>Songs</h2>
      <ul>
        {songs.map((song, index) => (
          <li key={index}>
            {" "}
            {/* Using index as a last resort if there's no unique id */}
            {song.title} by {song.artist}
            <button onClick={() => onSelectSong(song)}>Play</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SongList;
