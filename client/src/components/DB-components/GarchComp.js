import React, { useState, useEffect } from "react";
import predictionsData from "../../data/backendLoad.json";
import "../../styles/Comparisons.css";
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:5000/schedule');

const GarchComp = () => {
  // const [predictions, setPredictions] = useState({ garch: 0.0 });
  const [message, setMessage] = useState('');
  useEffect(() => {
    // setPredictions(predictionsData.time_series_predictions);
    socket.on('inference', (data) => {
      const roundedMessage = Number(data.garch).toFixed(2);
      setMessage(roundedMessage);
      console.log(roundedMessage);
    });

    return () => {
      socket.off('inference');
    };
  }, []);

  const getColorForPrediction = (value) => {
    if (value < 100) {
      return "#FF5A5A";
    } else if (value >= 100 && value <= 120) {
      return "#DBCB3C";
    } else {
      return "#0EF2CC";
    }
  };

  return (
    <>
      <p>Garch Scores:</p>
      <div>
        <span
          className="scores-text"
          style={{ color: getColorForPrediction(Number(message)) }}
        >
          {message}
        </span>
      </div>
    </>
  );
};

export default GarchComp;
