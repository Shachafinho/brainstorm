import React from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';

// === Components ===

function DataLoader(props) {
  const data = useFetchData(props.url);
  if (!data) {
    return <CircularProgress />;
  }

  const children = React.Children.toArray(props.children);
  return children.map((child) => (
    React.cloneElement(child, {
      data: data,
      ...child.props,
    })
  ));
}

// === Functions ===

async function fetchJsonData(url) {
  return await fetch(url)
    .then(res => res.json())
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
  }, [url]);
  return data;
}

// === Exports ===

// export default DataLoader;
export {
  DataLoader,
  useFetchData,
};
