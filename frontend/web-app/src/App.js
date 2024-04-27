import React, { useState } from "react";
import SongList from "./SongList";
import AudioPlayer from "./AudioPlayer";
import "./App.css";

function App() {
  const [selectedSong, setSelectedSong] = useState(null);

  return (
    <div className="App">
      <header>
        <h1>Song Recommender</h1>
      </header>
      <SongList onSelectSong={setSelectedSong} />
      <AudioPlayer song={selectedSong} />
    </div>
  );
}

export default App;
