import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

const API_URL = (window.API_URL === '__API_URL__') ? 'http://127.0.0.1:5000' : window.API_URL
ReactDOM.render(
  <React.StrictMode>
    <App apiUrl={API_URL} />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
