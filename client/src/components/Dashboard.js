import React from "react";
import Grid from "@mui/material/Unstable_Grid2";
import { Container, Divider, Typography } from "@mui/material";
import Decision from "./DB-components/Decision";
import GarchComp from "./DB-components/GarchComp";
import ArimaComp from "./DB-components/ArimaComp";
import SideSections from "./DB-components/SideSections";
import Iframe from "react-iframe";
import "../styles/Dashboard.css";

const Dashboard = ({ symbol }) => {
  const chart_Iframe_URL =
    "https://ammar-s847.github.io/TradingView-chart-Iframe/";

  return (
    <Container maxWidth="lg">
      <h4 className="stocker-name">[Symbol Name] - [Company Name]</h4>
      <Divider style={{ backgroundColor: "grey", marginBottom: "2rem" }} />
      <Grid container spacing={4}>
        <Grid xs={6} md={4}>
          {" "}
          <ArimaComp />
        </Grid>
        <Grid xs={6} md={4}>
          <GarchComp />
        </Grid>
        <Grid xs={6} md={4}>
          <Decision outcome="HOLD" />
        </Grid>
        <Grid xs={6} md={5}>
          <Iframe
            url={`${chart_Iframe_URL}?symbol=${symbol}`}
            width="420px"
            height="420px"
            id="myId"
            display="initial"
          />
        </Grid>
        <Grid xs={6} md={7}>
          <SideSections />
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
