import React, { useEffect, useState } from "react";
import { Wrapper, Status } from "@googlemaps/react-wrapper";
import render, { MyMapComponent } from "./Map";

import { Stack } from "@mui/material";

const MapMain = () => {
  // Fetch the data from the backend
  const [currentData, setData] = useState(null);
  useEffect(() => {
    fetch("/data")
      .then((res) => res.json())
      .then((data) => {
        setData(data.data);
      });
  }, []);

  useEffect(() => {}, [currentData]);

  return (
    <Stack spacing={3} justifyContent="center" alignItems="center">
      Hello
      <Wrapper
        apiKey={"AIzaSyDwddSbdeMLDvUNIEUzv6gBb0dGFCCUyoA"}
        render={render}
      >
        <MyMapComponent />
      </Wrapper>
    </Stack>
  );
};

export default MapMain;
