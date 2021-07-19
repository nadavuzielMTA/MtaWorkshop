import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });

  }, []);

  return (
    //window.open("../forum/index.html")
    <div className="App">
      <header className="App-header">

        <p>This message comes from BackEnd :) </p>
        <p>{currentTime}.</p>
      </header>
    </div>
  );
}

export default App;