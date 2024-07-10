import React, { useState, useEffect } from "react";
import predictionsData from "../../data/timeSeriesPredictions.json";
import "../../styles/Comparisons.css";

const ArimaComp = () => {
  const [predictions, setPredictions] = useState({ arima: 0.0 });

  useEffect(() => {
    setPredictions(predictionsData.time_series_predictions);
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
      <p>Arima Scores:</p>
      <div>
        <span
          className="scores-text"
          style={{ color: getColorForPrediction(predictions.arima) }}
        >
          {predictions.arima}
        </span>
      </div>
    </>
  );
};

export default ArimaComp;
