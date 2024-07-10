import React, { useState, useEffect } from "react";
import { Container, Grid } from "@mui/material";
import predictionsData from "../../data/backendLoad.json";
import NewsCarousel from "./NewsCarousel";
import "../../styles/Comparisons.css";

const SideSections = () => {
  const [predictions, setPredictions] = useState({
    implied_volatility: 0.0,
    historical_volatility: 0.0,
    overall_sentiment: "neutral",
  });

  useEffect(() => {
    setPredictions({
      implied_volatility: predictionsData.implied_volatility,
      historical_volatility: predictionsData.historical_volatility,
      overall_sentiment: predictionsData.overall_sentiment,
    });
  }, []);

  const getColorForPrediction = (value) => {
    if (value == "Negative") {
      return "#FF5A5A";
    } else if (value == "Neutral") {
      return "#DBCB3C";
    } else {
      return "#0EF2CC";
    }
  };

  return (
    <Container>
      <Grid container spacing={2}>
        <Grid item xs={6} md={6} lg={6}>
          <p>Implied Volatility:</p>
          <span className="scores-text">{predictions.implied_volatility}</span>
        </Grid>
        <Grid item xs={6} md={6} lg={6}>
          <p>Historical Volatility:</p>
          <span className="scores-text">
            {predictions.historical_volatility}
          </span>
        </Grid>
        <Grid item xs={12}>
          <p>Overall News Sentiment:</p>
          <span
            className="scores-text"
            style={{
              color: getColorForPrediction(predictions.overall_sentiment),
            }}
          >
            {predictions.overall_sentiment}
          </span>
        </Grid>
        <Grid item xs={12}>
          <NewsCarousel />
        </Grid>
      </Grid>
    </Container>
  );
};

export default SideSections;
