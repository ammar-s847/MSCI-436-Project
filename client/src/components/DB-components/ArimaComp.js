import React, { useState, useEffect } from "react";
import predictionsData from "../../data/backendLoad.json";
import "../../styles/Comparisons.css";
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:5000/schedule');

const ArimaComp = () => {
  const [predicted, setPredicted] = useState('');
  const [current, setCurrent] = useState('');
  useEffect(() => {
    socket.on('inference', (data) => {
      const roundedMessage = Number(data.arima).toFixed(2);
      const roundedCurrent = Number(data.current).toFixed(2)
      setPredicted(roundedMessage);
      setCurrent(roundedCurrent);
      console.log(roundedMessage);
      console.log(roundedCurrent);
    });

    return () => {
      socket.off('inference');
    };
  }, []);

  const getColorForPrediction = (current, predicted) => {
    if (Number(predicted) > Number(current)) {
      return "#0EF2CC";
    } else if (Number(predicted) < Number(current)) {
      return "#FF5A5A";
    } else {
      return "#DBCB3C";
    }
  };

  return (
    <>
      <p>Arima Prediction:</p>
      <div>
        <span
          className="scores-text"
          style={{ color: getColorForPrediction(Number(current), Number(predicted)) }}
        >
          {predicted}
        </span>
      </div>
    </>
  );
};

export default ArimaComp;
