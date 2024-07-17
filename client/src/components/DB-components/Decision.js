import React, { useState, useEffect } from "react";
import { CircularProgress } from "@mui/material";
import "../../styles/Decision.css";
import io from "socket.io-client";

// // Initialize socket connection
// const socket = io("http://127.0.0.1:5000/schedule");

const Decision = ({ decision, loading }) => {
  // const [decision, setDecision] = useState("");
  // const [loading, setLoading] = useState(true);

  // useEffect(() => {
  //   setLoading(true);
  //   socket.on("inference", (data) => {
  //     const roundedMessage = data.decision;
  //     setDecision(roundedMessage);
  //     setLoading(false);
  //   });

  //   return () => {
  //     socket.off("inference");
  //   };
  // }, [refresh]);

  const getClassName = () => {
    switch (decision) {
      case "buy":
        return "outcome buy";
      case "sell":
        return "outcome sell";
      case "hold":
        return "outcome hold";
      default:
        return "outcome";
    }
  };

  return (
    <div className="decision-container">
      <p>Our Suggestion:</p>
      {loading ? (
        <CircularProgress className="loading-container" size={50} />
      ) : (
        <div>
          <span className={getClassName()}>{decision}</span>
        </div>
      )}
    </div>
  );
};

export default Decision;

