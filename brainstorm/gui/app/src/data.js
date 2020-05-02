import React from 'react';
import ReactLoading from 'react-loading';

// === Components ===

function DataLoader(props) {
  const data = useFetchData(props.url);
  if (!data) {
    return <ReactLoading type="spinningBubbles" color="black" />;
  }
  return props.renderData(data);
}

// === Functions ===

function sleep(ms) {
  // TODO: DELETE ME
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchJsonData(url) {
  return await fetch(url)
    .then(res => res.json())
    .then(async data => {
      return await sleep(1000).then(() => data);
    })
    .catch(console.log);
}

function useFetchData(url) {
  const [data, setData] = React.useState(null);
  React.useEffect(() => {
    if (!url) {
      return;
    }
    fetchJsonData(url).then(fetchedData => {
      setData(fetchedData);
    });
  });
  return data;
}

// === Exports ===

export default DataLoader;
