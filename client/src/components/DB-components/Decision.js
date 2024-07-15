import React from "react";
import "../../styles/Decision.css";

const Decision = ({ outcome }) => {
  const getClassName = (outcome) => {
    switch (outcome) {
      case "Buy":
        return "outcome buy";
      case "Sell":
        return "outcome sell";
      case "Hold":
        return "outcome hold";
      default:
        return "outcome";
    }
  };

  return (
    <>
      <p>Our Suggestion:</p>
      <div>
        <span className={getClassName(outcome)}>{outcome}</span>
      </div>
    </>
  );
};

export default Decision;
