import React, { useState, useEffect } from "react";
import { Container, Grid, CircularProgress } from "@mui/material";
import NewsCarousel from "./NewsCarousel";
import "../../styles/Comparisons.css";

const SideSections = ({ overall_sentiment, news_articles }) => {
  const [showInfo, setShowInfo] = useState(false);
  const [predictions, setPredictions] = useState({
    implied_volatility: 0.0,
    historical_volatility: 0.0,
    overall_sentiment: "neutral",
    news_articles: []
  });

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/news_sentiment");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const news_data = await response.json();
        console.log(news_data)
        setPredictions(() => ({
          implied_volatility: predictionsData.implied_volatility,
          historical_volatility: predictionsData.historical_volatility,
          overall_sentiment: news_data.overall_sentiment,
          news_articles: news_data.news_articles,
        }));
      } catch (error) {
        console.error("Error fetching predictions:", error);
      }
    };

    fetchPredictions();
  }, []);

  const getColorForPrediction = (value) => {
    if (value === "negative") {
      return "#FF5A5A";
    } else if (value === "neutral") {
      return "#DBCB3C";
    } else {
      return "#0EF2CC";
    }
  };

  const infoText = `
    Overall sentiment is calculated by analyzing news articles related to a specific company. 
    The function processes each article by combining the headline and summary, converting the 
    text to lowercase, and checking for the presence of the company's ticker or name. The 
    sentiment of each article is predicted using a sentiment analysis model. Articles 
    mentioning the company name or ticker directly are given additional weight: articles 
    mentioning the company get a weight of 2, and if the sentiment is negative and highly 
    confident, an extra weight of 1 is added. Sentiment scores are categorized as positive, 
    neutral, or negative based on model predictions and confidence levels. The overall sentiment 
    (positive, neutral, or negative) is determined by the highest count of these categories, and 
    the function returns this overall sentiment along with a list of analyzed news articles and 
    their respective sentiments.
  `;

  return (
    <Container>
      <Grid container spacing={2}>
        <Grid item xs={6} md={6} lg={6}>
          <p>Implied Volatility:</p>
          {loading ? (
            <CircularProgress className="loading-container" size={50} />
          ) : (
            <span className="scores-text">
              {Number(volatility.implied_volatility)}
            </span>
          )}
        </Grid>
        <Grid item xs={6} md={6} lg={6}>
          <p>Historical Volatility:</p>
          {loading ? (
            <CircularProgress className="loading-container" size={50} />
          ) : (
            <span className="scores-text">
              {Number(volatility.historical_volatility)}
            </span>
          )}
        </Grid>
        <Grid item xs={12} style={{ position: "relative" }}>
          <Grid
            container
            direction="row"
            justifyContent="flex-start"
            alignItems="center"
            style={{ position: "relative" }}
          >
            <button
              onClick={() => setShowInfo(!showInfo)}
              style={{
                marginRight: "5px",
                backgroundColor: "white",
                color: "black",
                border: "none",
                borderRadius: "50%",
                width: "20px",
                height: "20px",
                fontSize: "10px",
                cursor: "pointer",
                position: "relative",
              }}
            >
              ?
            </button>
            <p>Overall News Sentiment:</p>
            {showInfo && (
              <div
                style={{
                  backgroundColor: "white",
                  padding: "10px",
                  border: "1px solid #ddd",
                  borderRadius: "5px",
                  zIndex: 1000,
                  width: "300px",
                  maxHeight: "200px",
                  overflowY: "auto",
                  position: "absolute",
                  top: "30px",
                  left: "0",
                }}
              >
                <p style={{ fontSize: "15px", color: "black" }}>{infoText}</p>
              </div>
            )}
          </Grid>
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
          <NewsCarousel news_articles={predictions.news_articles} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default SideSections;
