import React from 'react';
// import CircularProgress from '@material-ui/core/CircularProgress';
// import ExpansionPanel from '@material-ui/core/ExpansionPanel';
// import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
// import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
// import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import { Collection, CollectionItem } from './collection.js';
import { DataLoader } from './data.js';
import ResultCollection from './result.js';
import { useStyles } from './style.js';
import { getSnapshotsUrl, getSnapshotUrl } from './urls.js';

// === Components ===

function SnapshotInformation(props) {
  return (
    <>
    </>
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
  const classes = useStyles();
  const timestamp = new Date(props.timestamp).toLocaleString();

  return (
    <>
      <Typography className={classes.heading}>
        {timestamp}
      </Typography>
      <Typography className={classes.secondaryHeading}>
        {props.snapshotId}
      </Typography>
    </>
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

function SnapshotWithData(props) {
  const snapshotData = props.data;

  return (
    <>
      <CollectionItem
        onClick={props.onClick}
        isExpanded={props.isExpanded}
      >
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
      </CollectionItem>
    </>
  );
}

function Snapshot(props) {
  return (
    <DataLoader url={getSnapshotUrl(props.apiUrl, props.userId, props.snapshotId)}>
      <SnapshotWithData {...props} />
    </DataLoader>
  );
}

// function Snapshot2(props) {
//   const snapshotData = useFetchData(getSnapshotUrl(props.apiUrl, props.userId, props.snapshotId));
//   if (!snapshotData) {
//     return <><CircularProgress /></>;
//   }

//   return (
//     <>
//       <ExpansionPanel
//         expanded={props.isExpanded}
//         onChange={props.onChange}
//       >
//         <ExpansionPanelSummary
//           expandIcon={<ExpandMoreIcon />}
//           id={`panel${props.snapshotId}-header`}
//         >
//           <SnapshotHeader
//             snapshotId={props.snapshotId}
//             timestamp={props.timestamp}
//           />
//         </ExpansionPanelSummary>
//         <ExpansionPanelDetails>
//           <div>
//             <SnapshotInformation />
//             <ResultCollection
//               apiUrl={props.apiUrl}
//               userId={props.userId}
//               snapshotId={props.snapshotId}
//               results={snapshotData.results}
//             />
//           </div>
//         </ExpansionPanelDetails>
//       </ExpansionPanel>
//     </>
//   );
// }

// function Snapshot3(props) {
//   function renderSnapshot(snapshotData) {
//     return (
//       <div className="snapshot">
//         <SnapshotHeader
//           snapshotId={props.snapshotId}
//           timestamp={props.timestamp}
//         />
//         <SnapshotInformation />
//         <ResultCollection
//           apiUrl={props.apiUrl}
//           userId={props.userId}
//           snapshotId={props.snapshotId}
//           results={snapshotData.results}
//         />
//       </div>
//     );
//   }

//   return (
//     <>
//       <DataLoader
//         url={getSnapshotUrl(props.apiUrl, props.userId, props.snapshotId)}
//         renderData={renderSnapshot}
//       />
//     </>
//   );
// }

// class Snapshot4 extends React.Component {
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
  const [expanded, setExpanded] = React.useState(false);

  const isExpanded = (snapshotId) => (snapshotId === expanded);
  const handleClick = (snapshotId) => () => {
    setExpanded(isExpanded(snapshotId) ? false : snapshotId);
  };

  const snapshotItems = props.data.map((minimalSnapshot) => {
    const snapshotId = minimalSnapshot.snapshot_id;
    return (
      <Snapshot
        key={`${snapshotId}`}
        apiUrl={props.apiUrl}
        userId={props.userId}
        snapshotId={snapshotId}
        timestamp={minimalSnapshot.timestamp}
        isExpanded={isExpanded(snapshotId)}
        onClick={handleClick(snapshotId)}
      />
    );
  });
  const snapshotCollection = (snapshotItems.length > 0) ?
    <>{snapshotItems}</> :
    <>No snapshots...</>;

  return (
    <Collection renderHeader={() => "Snapshots"}>
      {snapshotCollection}
    </Collection>
  );
}

// function SnapshotCollection2(props) {
//   const classes = useStyles();
//   const [expanded, setExpanded] = React.useState(false);

//   const handleChange = (panel) => (event, isExpanded) => {
//     setExpanded(isExpanded ? panel : false);
//   };

//   const snapshots = useFetchData(getSnapshotsUrl(props.apiUrl, props.userId));
//   if (!snapshots) {
//     return <><CircularProgress /></>;
//   }

//   const snapshotItems = snapshots.map((minimalSnapshot) => (
//     <Snapshot
//       key={`${minimalSnapshot.snapshot_id}`}
//       apiUrl={props.apiUrl}
//       userId={props.userId}
//       snapshotId={minimalSnapshot.snapshot_id}
//       timestamp={minimalSnapshot.timestamp}
//       isExpanded={minimalSnapshot === expanded}
//       onChange={handleChange(minimalSnapshot.snapshot_id)}
//     />
//   ));
//   const snapshotCollection = (snapshotItems.length > 0) ?
//     <>{snapshotItems[0]}</> :
//     'No snapshots...';

//   return (
//     <div className={classes.root}>
//       {snapshotCollection}
//     </div>
//   );
// }

// function SnapshotCollection3(props) {
//   function renderSnapshots(snapshots) {
//     const snapshotItems = snapshots.map((minimalSnapshot) => (
//       <li key={minimalSnapshot.snapshot_id.toString()}>
//         <Snapshot
//           apiUrl={props.apiUrl}
//           userId={props.userId}
//           snapshotId={minimalSnapshot.snapshot_id}
//           timestamp={minimalSnapshot.timestamp}
//         />
//       </li>
//     ));
//     const snapshotCollection = (snapshotItems.length > 0) ?
//       <ul>{snapshotItems[0]}</ul> :
//       'No snapshots...';

//     return (
//       <div className="snapshot-collection">
//         {snapshotCollection}
//       </div>
//     );
//   }

//   return (
//     <>
//       <DataLoader
//         url={getSnapshotsUrl(props.apiUrl, props.userId)}
//         renderData={renderSnapshots}
//       />
//     </>
//   );
// }

// class SnapshotCollection4 extends React.Component {
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

function Snapshots(props) {
  return (
    <DataLoader url={getSnapshotsUrl(props.apiUrl, props.userId)}>
      <SnapshotCollection
        apiUrl={props.apiUrl}
        userId={props.userId}
      />
    </DataLoader>
  );
}

// === Exports ===

export default Snapshots;
