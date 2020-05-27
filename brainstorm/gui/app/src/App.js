import React from 'react';
// import logo from './logo.svg';
// import './App.css';
// import UserCollection from './user.js';
import Users from './user.js';

// === Components ===

class App extends React.Component {
  render() {
    return (
      <div className="App">
        {/* <UserCollection apiUrl={this.props.apiUrl} /> */}
        <Users apiUrl={this.props.apiUrl} />
      </div>
    );
  }
}

// function App(props) {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//         API URL: {props.apiUrl}
//       </header>
//     </div>
//   );
// }

// === Exports ===

export default App;
