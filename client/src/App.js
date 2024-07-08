import React, { useState } from "react";
import "./styles/App.css";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Dashboard from "./components/Dashboard";

function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  const handleSearchComplete = () => {
    setShowDashboard(true);
  };

  return (
    <div className="App">
      <Header />
      <Hero onSearchComplete={handleSearchComplete} />
      {showDashboard && <Dashboard />}
    </div>
  );
}

export default App;
