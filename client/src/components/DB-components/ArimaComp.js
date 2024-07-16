import React, { useState, useEffect } from "react";
import { CircularProgress } from "@mui/material";
import "../../styles/Comparisons.css";
import io from "socket.io-client";

const socket = io("http://127.0.0.1:5000/schedule");

const ArimaComp = ({refresh}) => {
  const [predicted, setPredicted] = useState("");
  const [current, setCurrent] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    socket.on("inference", (data) => {
      const roundedPredicted = Number(data.arima).toFixed(2);
      setPredicted(roundedPredicted);
      console.log(roundedPredicted);
      const roundedCurrent = Number(data.current).toFixed(2)
      setCurrent(roundedCurrent);
      console.log(roundedCurrent);
      setLoading(false);
    });

    return () => {
      socket.off("inference");
    };
  }, [refresh]);

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
        {loading ? (
          <CircularProgress className="loading-container" size={50} />
        ) : (
          <span
            className="scores-text"
            style={{ color: getColorForPrediction(Number(current), Number(predicted)) }}
          >
            {predicted}
          </span>
        )}
      </div>
    </>
  );
};

export default ArimaComp;
