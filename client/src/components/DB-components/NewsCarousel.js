import React, { useEffect, useState } from "react";
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css";
import newsData from "../../data/newsArticles.json";
import "../../styles/NewsCarousel.css";

const NewsCarousel = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    setArticles(newsData.news_articles);
  }, []);

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case "positive":
        return "green";
      case "neutral":
        return "gray";
      case "negative":
        return "red";
      default:
        return "black";
    }
  };

  return (
    <Carousel>
      {articles.map((article, index) => (
        <div key={index} className="carousel-item">
          <h2>{article.headline}</h2>
          <p>{article.description}</p>
          <p>
            <strong>Sentiment:</strong>{" "}
            <span style={{ color: getSentimentColor(article.sentiment) }}>
              {article.sentiment}
            </span>
          </p>
          <p>
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              Read more
            </a>
          </p>
        </div>
      ))}
    </Carousel>
  );
};

export default NewsCarousel;
