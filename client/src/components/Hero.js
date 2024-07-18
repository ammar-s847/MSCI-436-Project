import api from "../api";
import React, { useState } from "react";
import { CircularProgress, Container } from "@mui/material";
import "../styles/Hero.css";
import Dashboard from "./Dashboard";

const Hero = ({ onSearchComplete, showDashboard, dashboardRef, tickerName }) => {
  const [query, setQuery] = useState("");
  const [hideTitle, setHideTitle] = useState(true);
  const [companyName, setCompanyName] = useState("");
  const [impliedVolatility, setImpliedVolatility] = useState(null);
  const [historicalVolatility, setHistoricalVolatility] = useState(null);
  const [overallSentiment, setOverallSentiment] = useState(null);
  const [newsArticles, setNewsArticles] = useState([]);
  const [loader, setLoader] = useState(false);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };
  const handleSearch = (e) => {
    e.preventDefault();
    setLoader(true);
    
    api.post("http://127.0.0.1:5000/new_ticker", { ticker: query })
      .then((response) => {
        console.log("Search result:", response.data);
        setHideTitle(false);
        onSearchComplete(query);

        return api.get("http://127.0.0.1:5000/company_name");
      })
      .then((companyNameResponse) => {
        setCompanyName(companyNameResponse.data.company_name);
        setLoader(false); 

        return api.get("http://127.0.0.1:5000/news_sentiment");
      })
      .then((newsSentimentResponse) => {
        setNewsArticles(newsSentimentResponse.data.news_articles);
        setOverallSentiment(newsSentimentResponse.data.overall_sentiment);
      })
      .catch((error) => {
        console.error("Error performing search:", error);
        setLoader(false);
      });
  };

  return (
    <main className="App-main">
      {hideTitle && <h1 className="title">Welcome to Stocker!</h1>}
      <p className="hero-welcome">
        Search for your favourite stock tickers and make smarter decisions
      </p>
      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search stocks"
          value={query}
          onChange={handleInputChange}
          className="search-input"
        />
        <button type="submit" className="search-button">
          <span>Search</span>
        </button>
      </form>
      {loader ? (
        <Container className="loading-container">
          <CircularProgress size={50} />
        </Container>
      ) : (
        showDashboard && (
          <Dashboard
            ref={dashboardRef}
            tickerName={query}
            companyName={companyName}
            impliedVolatility={impliedVolatility}
            historicalVolatility={historicalVolatility}
            overallSentiment={overallSentiment}
            newsArticles={newsArticles}
          />
        )
      )}
    </main>
  );
};

export default Hero;

