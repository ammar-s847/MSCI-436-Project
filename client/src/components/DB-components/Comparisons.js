import React, { useState, useEffect } from "react";
import predictionsData from "../../data/timeSeriesPredictions.json"; // Adjust the path as necessary
import "../../styles/Comparisons.css";

const Comparisons = () => {
  const [predictions, setPredictions] = useState({ arima: 0.0, garch: 0.0 });

  useEffect(() => {
    setPredictions(predictionsData.time_series_predictions);
  }, []);

  return (
    <>
      <h4>This is model comparisons</h4>
      <span>Arima: {predictions.arima}</span>
      <div>
        <span>Garch: {predictions.garch}</span>
      </div>
    </>
  );
};

export default Comparisons;
