import React, {
  forwardRef,
  useImperativeHandle,
  useState,
  useEffect,
} from "react";
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
import "../styles/Dashboard.css";
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:5000/schedule');

const Dashboard = forwardRef(
  (
    {
      tickerName,
      implied_volatility,
      historical_volatility,
      overall_sentiment,
      news_articles,
    },
    ref
  ) => {
    const [action, setAction] = useState("");
    const [companyName, setCompanyName] = useState("");
    const ticker_Name = tickerName.toUpperCase();
    const [decision, setDecision] = useState("");
    const [currentPrice, setCurrentPrice] = useState(0);
    const [loading, setLoading] = useState(true);

    const handleChange = async (event) => {
      const position = event.target.value;
      setAction(position);
  
      const id = generateUUID();
      const createdAt = new Date().toISOString();
      
      const tradeData = {
        id,
        symbol: tickerName,
        price: currentPrice,
        position,
        created_at: createdAt,
        user: "user"
      };

      console.log(tradeData)
  
      try {
        const response = await fetch('http://127.0.0.1:5000/trade', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(tradeData),
        });
  
        const result = await response.json();
        if (response.ok) {
          console.log('Trade created successfully:', result);
        } else {
          console.error('Failed to create trade:', result);
        }
      } catch (error) {
        console.error('Error creating trade:', error);
      }
    };

    const generateUUID = () => {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0,
              v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    };

    useEffect(() => {
      setLoading(true);
      socket.on("inference", (data) => {
        const roundedMessage = data.decision;
        setDecision(roundedMessage);
        setCurrentPrice(data.current);
        setLoading(false);
      });
  
      return () => {
        socket.off("inference");
      };
    }, [tickerName]);

    useImperativeHandle(ref, () => ({
      resetSelectBox() {
        setAction("");
      },
    }));

    const postTickerData = async (tickerData) => {
      try {
        const response = await fetch('http://127.0.0.1:5000/ticker', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(tickerData),
        });

        const result = await response.json();
        if (response.ok) {
          console.log('Ticker created successfully:', result);
        } else {
          console.error('Failed to create ticker:', result);
        }
      } catch (error) {
        console.error('Error creating ticker:', error);
      }
    };
    
    useEffect(() => {
      const fetchCompanyName = async () => {
        try {
          const response = await fetch("http://127.0.0.1:5000/company_name");
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          console.log("this is the data" + data)
          setCompanyName(data.company_name.toUpperCase());
        } catch (error) {
          console.error("Error fetching company name:", error);
        }
      };

      fetchCompanyName();

    }, [tickerName]);

    useEffect(() => {

      const createdAt = new Date().toISOString();

      const tickerData = {
        name: companyName,
        symbol: tickerName,
        created_at: createdAt,
      };

      console.log(tickerData)

      if (companyName !== '') {
        postTickerData(tickerData);
      }

    }, [companyName]);

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
              {ticker_Name} - {companyName}
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
                value={action}
                label="Select"
                onChange={handleChange}
                sx={{
                  color: "white",
                  "& .MuiSvgIcon-root": { color: "white" },
                }}
              >
                <MenuItem value="b">I bought</MenuItem>
                <MenuItem value="h">I held</MenuItem>
                <MenuItem value="s">I sold</MenuItem>
              </Select>
            </FormControl>
          </Grid2>
        </Grid2>

        <Divider style={{ backgroundColor: "grey", marginBottom: "2rem" }} />
        <Grid2
          xs={12}
          md={12}
          sx={{ display: "flex", justifyContent: "center" }}
        >
          <Iframe
            url={`${chart_Iframe_URL}?symbol=${tickerName}`}
            width="1500px"
            height="420px"
            id="myId"
            display="initial"
            style={{ border: "none" }}
          />
        </Grid2>
        <Grid2 sx={{ marginTop: "2rem" }} container spacing={4}>
          <Grid2 xs={6} md={4}>
            <ArimaComp refresh={tickerName}/>
          </Grid2>
          <Grid2 xs={6} md={4}>
            <GarchComp refresh={tickerName}/>
          </Grid2>
          <Grid2 xs={6} md={4}>
            <Decision decision={decision} loading={loading}/>
          </Grid2>
          <Grid2 xs={12} md={12}>
            <SideSections
              implied_volatility={implied_volatility}
              historical_volatility={historical_volatility}
              overall_sentiment={overall_sentiment}
              news_articles={news_articles}
              refresh={tickerName}
            />
          </Grid2>
        </Grid2>
      </Container>
    );
  }
);

export default Dashboard;
