import React, { useEffect, useState } from "react";
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css";
import newsData from "../../data/backendLoad.json";
import "../../styles/NewsCarousel.css";
import { Grid } from "@mui/material";

const NewsCarousel = ({news_articles = []}) => {

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case "positive":
        return "#0EF2CC";
      case "neutral":
        return "#DBCB3C";
      case "negative":
        return "#FF5A5A";
      default:
        return "white";
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp*1000);
    return date.toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <Carousel showThumbs={false} showStatus={false}>
      {news_articles.map((article, index) => (
        <div key={index} className="carousel-item">
          <h2 style={{ fontStyle: 'italic' }}>{formatTimestamp(article.timestamp)}</h2>
          <h2>{article.headline}</h2>
          <p>{article.description}</p>
          <Grid container justifyContent="space-between" alignItems="center">
            <Grid item>
              <p>
                <strong>Sentiment:</strong>{" "}
                <span style={{ color: getSentimentColor(article.sentiment) }}>
                  {article.sentiment}
                </span>
              </p>
            </Grid>
            <Grid item>
              <p>
                <a href={article.url} target="_blank" rel="noopener noreferrer">
                  Read more
                </a>
              </p>
            </Grid>
          </Grid>
        </div>
      ))}
    </Carousel>
  );
};

export default NewsCarousel;
