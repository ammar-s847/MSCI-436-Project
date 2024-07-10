import React, { useState, useRef } from "react";
import "./styles/App.css";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Dashboard from "./components/Dashboard";

function App() {
  const [showDashboard, setShowDashboard] = useState(false);
  const [symbol, setSymbol] = useState("");
  const dashboardRef = useRef(null);

  const handleSearchComplete = (newSymbol) => {
    setSymbol(newSymbol);
    setShowDashboard(true);
    if (dashboardRef.current) {
      dashboardRef.current.resetSelectBox();
    }
  };

  return (
    <div className="App">
      <Header />
      <Hero onSearchComplete={handleSearchComplete} />
      {showDashboard && <Dashboard ref={dashboardRef} symbol={symbol} />}
    </div>
  );
}

export default App;
