import React from 'react';
import DataLoader from './data.js';
import ResultCollection from './result.js';
import { getSnapshotsUrl, getSnapshotUrl } from './urls.js';

// === Components ===

function SnapshotInformation(props) {
  return (
    <div className="snapshot-information">
    </div>
  );
}

// class SnapshotInformation2 extends React.Component {
//   render() {
//     return (
//       <div className="snapshot-information">
//       </div>
//     );
//   }
// }

function SnapshotHeader(props) {
  const timestamp = new Date(props.timestamp).toLocaleString();
  return (
    <div className="snapshot-header">
      <div className="snapshot-id">
        {props.snapshotId}
      </div>
      <div className="snapshot-timestamp">
        {timestamp}
      </div>
    </div>
  );
}

// class SnapshotHeader extends React.Component {
//   render() {
//     const timestamp = new Date(this.props.timestamp).toLocaleString();

//     return (
//       <div className="snapshot-header">
//         <div className="snapshot-id">
//           {this.props.snapshotId}
//         </div>
//         <div className="snapshot-timestamp">
//           {timestamp}
//         </div>
//       </div>
//     );
//   }
// }

function Snapshot(props) {
  function renderSnapshot(snapshotData) {
    return (
      <div className="snapshot">
        <SnapshotHeader
          snapshotId={props.snapshotId}
          timestamp={props.timestamp}
        />
        <SnapshotInformation />
        <ResultCollection
          apiUrl={props.apiUrl}
          userId={props.userId}
          snapshotId={props.snapshotId}
          results={snapshotData.results}
        />
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getSnapshotUrl(props.apiUrl, props.userId, props.snapshotId)}
        renderData={renderSnapshot}
      />
    </>
  );
}

// class Snapshot2 extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       results: [],
//     }
//   }

//   componentDidMount() {
//     fetch(getSnapshotUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId))
//     .then(res => res.json())
//     .then((snapshot) => {
//       this.setState({
//         results: snapshot.results,
//       })
//     })
//     .catch(console.log);
//   }

//   render() {
//     const results = this.state.results;
//     return (
//       <div className="snapshot">
//         <SnapshotHeader
//           snapshotId={this.props.snapshotId}
//           timestamp={this.props.timestamp}
//         />
//         <SnapshotInformation />
//         {results.length > 0 &&
//           <ResultCollection
//             apiUrl={this.props.apiUrl}
//             userId={this.props.userId}
//             snapshotId={this.props.snapshotId}
//             results={this.state.results}
//           />
//         }
//       </div>
//     );
//   }
// }

function SnapshotCollection(props) {
  function renderSnapshots(snapshots) {
    const snapshotItems = snapshots.map((minimalSnapshot) => (
      <li key={minimalSnapshot.snapshot_id.toString()}>
        <Snapshot
          apiUrl={props.apiUrl}
          userId={props.userId}
          snapshotId={minimalSnapshot.snapshot_id}
          timestamp={minimalSnapshot.timestamp}
        />
      </li>
    ));
    const snapshotCollection = (snapshotItems.length > 0) ?
      <ul>{snapshotItems[0]}</ul> :
      'No snapshots...';

    return (
      <div className="snapshot-collection">
        {snapshotCollection}
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getSnapshotsUrl(props.apiUrl, props.userId)}
        renderData={renderSnapshots}
      />
    </>
  );
}

// class SnapshotCollection2 extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       snapshots: [],
//     }
//   }

//   componentDidMount() {
//     fetch(getSnapshotsUrl(this.props.apiUrl, this.props.userId))
//     .then(res => res.json())
//     .then((minimalSnapshots) => {
//       this.setState({snapshots: minimalSnapshots})
//     })
//     .catch(console.log);
//   }

//   render() {
//     const snapshotItems = this.state.snapshots.map((minimalSnapshot) => (
//       <li key={minimalSnapshot.snapshot_id.toString()}>
//         <Snapshot
//           apiUrl={this.props.apiUrl}
//           userId={this.props.userId}
//           snapshotId={minimalSnapshot.snapshot_id}
//           timestamp={minimalSnapshot.timestamp}
//         />
//       </li>
//     ));
//     return (
//       <div className="snapshot-collection">
//         {snapshotItems.length > 0 &&
//           <ul>
//             {snapshotItems[0]}
//           </ul>
//         }
//       </div>
//     );
//   }
// }

// === Exports ===

export default SnapshotCollection;
