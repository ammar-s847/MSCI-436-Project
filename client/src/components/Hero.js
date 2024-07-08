import api from "../api";
import React, { useState, useEffect } from "react";
import "../styles/Hero.css";

const Hero = ({ onSearchComplete }) => {
  const [data, setData] = useState(null);
  const [query, setQuery] = useState("");
  const [hideTitle, setHideTitle] = useState(true);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    console.log("Search input:", query);
    setHideTitle(false);
    onSearchComplete(query);
    api
      .post("/search", { query }) // Replace search with endpoint
      .then((response) => {
        console.log("Search result:", response.data);
        // onSearchComplete(query);
      })
      .catch((error) => {
        console.error("Error performing search:", error);
      });
  };

  useEffect(() => {
    api
      .get("/endpoint")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <main className="App-main">
      {hideTitle && <h1 className="title">Welcome to Stocker!</h1>}
      <p>Search for your favourite stocks and make smarter decisions</p>
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
      {data && (
        <div>
          <h2>Fetched Data:</h2>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </main>
  );
};

export default Hero;
