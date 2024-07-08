import React from "react";
import Grid from "@mui/material/Unstable_Grid2";
import { Container } from "@mui/material";
import Decision from "./DB-components/Decision";
import Comparisons from "./DB-components/Comparisons";
import NewsCarousel from "./DB-components/NewsCarousel";
import Iframe from "react-iframe";
import "../styles/Dashboard.css";

const Dashboard = ({ symbol }) => {
  const chart_Iframe_URL =
    "https://ammar-s847.github.io/TradingView-chart-Iframe/";

  return (
    <Container maxWidth="lg">
      <Grid container spacing={2}>
        <Grid xs={6} md={8}>
          <Iframe
            url={`${chart_Iframe_URL}?symbol=${symbol}`}
            width="420px"
            height="420px"
            id="myId"
            display="initial"
            position="relative"
          />
        </Grid>
        <Grid xs={6} md={4}>
          <Decision outcome="Buy" />
        </Grid>
        <Grid xs={6} md={4}>
          <Comparisons />
        </Grid>
        <Grid xs={6} md={8}>
          <h4>This is News</h4>
          <NewsCarousel />
        </Grid>
        <Grid>
          <span>
            "implied_volatility": 0.0, "historical_volatility": 0.0,
            "overall_sentiment": "positive" | "neutral" | "negative"
          </span>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
