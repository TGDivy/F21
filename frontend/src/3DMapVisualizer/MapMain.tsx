import React, {useEffect, useState} from "react";
import { render } from "react-dom";
import Render from "./SimpleMap";
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

  useEffect(()=> {
      Render();
  }, [currentData]);

  return (
    <div>
      <div>3DMapMain</div>
      <div>{currentData}</div>
    <canvas id="map">
    
    </canvas>
    </div>
  );
};

export default MapMain;
