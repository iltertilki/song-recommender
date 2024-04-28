import React from "react";

function AudioPlayer({ song }) {
  return (
    <div>
      {song ? (
        <div>
          <h3>
            Now Playing: {song.title} by {song.artist}
          </h3>
          <audio controls autoPlay src={`/audio/${song.id}`}>
            Your browser does not support the audio element.
          </audio>
        </div>
      ) : (
        <p>Select a song to play</p>
      )}
    </div>
  );
}

export default AudioPlayer;
