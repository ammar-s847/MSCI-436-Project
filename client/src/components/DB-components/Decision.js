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
      <h3>Overall the model recommends that you:</h3>
      <button className={getClassName(outcome)}>{outcome}</button>
    </>
  );
};

export default Decision;
