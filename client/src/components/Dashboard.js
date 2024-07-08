// Dashboard.js
import React from "react";
import Grid from "@mui/material/Unstable_Grid2";
import { Container, Box } from "@mui/material";
import Decision from "./DB-components/Decision";
import Comparisons from "./DB-components/Comparisons";
import NewsCarousel from "./DB-components/NewsCarousel";
import temp from "../images/temp-stock.png";
import "../styles/Dashboard.css";

const Dashboard = () => {
  return (
    <Container maxWidth="lg">
      <Grid container spacing={2}>
        <Grid xs={6} md={8}>
          <Box
            component="img"
            sx={{
              height: 500,
              width: 750,
              maxHeight: { xs: 233, md: 300 },
              maxWidth: { xs: 350, md: 500 },
            }}
            alt="temp"
            src={temp}
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
            "overall_sentiment": "positive" | "neutral" | "negative",{" "}
          </span>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
