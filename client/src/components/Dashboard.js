import React, { forwardRef, useImperativeHandle } from "react";
import Grid2 from "@mui/material/Unstable_Grid2";
import {
  Container,
  Divider,
  Typography,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from "@mui/material";
import Decision from "./DB-components/Decision";
import GarchComp from "./DB-components/GarchComp";
import ArimaComp from "./DB-components/ArimaComp";
import SideSections from "./DB-components/SideSections";
import Iframe from "react-iframe";
import Data from "../data/backendLoad.json";
import "../styles/Dashboard.css";

const Dashboard = forwardRef(({ symbol }, ref) => {
  const [age, setAge] = React.useState("");

  const handleChange = (event) => {
    setAge(event.target.value);
  };

  useImperativeHandle(ref, () => ({
    resetSelectBox() {
      setAge("");
    },
  }));

  const chart_Iframe_URL =
    "https://ammar-s847.github.io/TradingView-chart-Iframe/";

  return (
    <Container maxWidth="lg" sx={{ color: "white" }}>
      <Grid2
        container
        alignItems="center"
        justifyContent="space-between"
        sx={{ marginBottom: "1rem" }}
      >
        <Grid2 item>
          <Typography
            variant="h4"
            className="stocker-name"
            sx={{ color: "white" }}
          >
            {Data.ticker_name} - {Data.company_name}
          </Typography>
        </Grid2>
        <Grid2 item>
          <FormControl
            fullWidth
            sx={{
              minWidth: 120,
              color: "white",
              "& .MuiInputBase-root": { color: "white" },
              "& .MuiOutlinedInput-notchedOutline": { borderColor: "white" },
            }}
          >
            <InputLabel id="demo-simple-select-label" sx={{ color: "white" }}>
              Action
            </InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={age}
              label="Select"
              onChange={handleChange}
              sx={{ color: "white", "& .MuiSvgIcon-root": { color: "white" } }}
            >
              <MenuItem value="Buying">I bought</MenuItem>
              <MenuItem value="Holding">I held</MenuItem>
              <MenuItem value="Selling">I sold</MenuItem>
            </Select>
          </FormControl>
        </Grid2>
      </Grid2>

      <Divider style={{ backgroundColor: "grey", marginBottom: "2rem" }} />
      <Grid2 container spacing={4}>
        <Grid2 xs={6} md={4}>
          <ArimaComp />
        </Grid2>
        <Grid2 xs={6} md={4}>
          <GarchComp />
        </Grid2>
        <Grid2 xs={6} md={4}>
          <Decision outcome={Data.decision} />
        </Grid2>
        <Grid2 xs={6} md={5}>
          <Iframe
            url={`${chart_Iframe_URL}?symbol=${symbol}`}
            width="420px"
            height="420px"
            id="myId"
            display="initial"
          />
        </Grid2>
        <Grid2 xs={6} md={7}>
          <SideSections />
        </Grid2>
      </Grid2>
    </Container>
  );
});

export default Dashboard;
