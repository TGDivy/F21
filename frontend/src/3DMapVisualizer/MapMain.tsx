import React, { useEffect, useState } from "react";

const MapMain = () => {
  // Fetch the data from the backend
  const [currentData, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch("/data")
      .then((res) => res.json())
      .then((data) => {
        setCurrentTime(data.data);
      });
  }, []);

  return (
    <div>
      <div>3DMapMain</div>
      <div>{currentData}</div>
    </div>
  );
};

export default MapMain;
