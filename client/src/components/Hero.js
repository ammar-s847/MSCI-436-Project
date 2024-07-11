import api from "../api";
import React, { useState } from "react";
import "../styles/Hero.css";
import Dashboard from "./Dashboard";

const Hero = ({ onSearchComplete, showDashboard, dashboardRef, tickerName }) => {
  const [query, setQuery] = useState("");
  const [hideTitle, setHideTitle] = useState(true);
  const [companyName, setCompanyName] = useState("");
  const [implied_volatility, set_implied_volatility] = useState(0);
  const [historical_volatility, set_historical_volatility] = useState(0);
  const [overall_sentiment, set_overall_sentiment] = useState('neutral');
  const [news_articles, set_news_articles] = useState([]);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = (e) => {
    e.preventDefault();
  
    api.post("http://127.0.0.1:5000/new_ticker", { ticker: query })
      .then((response) => {
        console.log("Search result:", response.data);
        setHideTitle(false);
        onSearchComplete(query);
        console.log("Testing: " + query)

        return Promise.all([
          api.get("http://127.0.0.1:5000/company_name"),
          api.get("http://127.0.0.1:5000/news_sentiment")
        ]);
      })
      .then(([companyNameResponse, newsSentimentResponse]) => {
        setCompanyName(companyNameResponse.data.company_name);
        set_news_articles(newsSentimentResponse.data.news_articles);
        set_overall_sentiment(newsSentimentResponse.data.overall_sentiment);
      })
      .catch((error) => {
        console.error("Error performing search:", error);
      });
  };

  return (
    <main className="App-main">
      {hideTitle && <h1 className="title">Welcome to Stocker!</h1>}
      <p className="hero-welcome">
        Search for your favourite stocks and make smarter decisions
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
      {showDashboard && <Dashboard ref={dashboardRef} tickerName={query} companyName={companyName} implied_volatility={implied_volatility} historical_volatility={historical_volatility} overall_sentiment={overall_sentiment} news_articles={news_articles}/>}
    </main>
  );
};

export default Hero;
