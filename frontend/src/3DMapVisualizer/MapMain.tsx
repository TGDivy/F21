import React from "react";

const MapMain = () => {
  // Fetch the data from the backend
  const [data, setData] = React.useState(null);
  React.useEffect(() => {
    fetch("http://0.0.0.0:5000/data")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      })
      .catch((err) => console.log(err));
  }, []);

  console.log(data);

  // fetch("http://localhost:3000/api/");
  return (
    <div>
      <div>3DMapMain</div>
      <div>{data}</div>
    </div>
  );
};

export default MapMain;
