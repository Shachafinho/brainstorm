import React from 'react';
import Typography from '@material-ui/core/Typography';

import { Collection, CollectionItem } from './collection.js';
import { DataLoader } from './data.js';
import { ImageDialog } from './image.js';
import { useStyles } from './style.js';
import { getResultUrl } from './urls.js';

// === Components ===

function ImageResult(props) {
  return (
    <>
      <ImageDialog
        width={props.width}
        height={props.height}
        data={props.data}
      />
    </>
  )
}

// class ImageResult2 extends React.Component {
//   render() {
//     return (
//       <div className="result-base-image">
//         Width: {this.props.width},
//         Height: {this.props.height},
//         Data: {this.props.data}
//       </div>
//     )
//   }
// }

function ColorImageResult(props) {
  const colorImage = props.data;
  return (
    <>
      <ImageResult
        width={colorImage.width}
        height={colorImage.height}
        data={colorImage.data}
      />
    </>
  );
}

// class ColorImageResult2 extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       width: null,
//       height: null,
//       data: null,
//     }
//   }

//   componentDidMount() {
//     fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'color_image'))
//     .then(res => res.json())
//     .then((colorImage) => {
//       this.setState({
//         width: colorImage.width,
//         height: colorImage.height,
//         data: colorImage.data,
//       })
//     })
//     .catch(console.log);
//   }

//   render() {
//     return (
//       <div className="result-color-image">
//         <ImageResult
//           width={this.state.width}
//           height={this.state.height}
//           data={this.state.data}
//         />
//       </div>
//     );
//   }
// }

function DepthImageResult(props) {
  const depthImage = props.data;
  return (
    <>
      <ImageResult
        width={depthImage.width}
        height={depthImage.height}
        data={depthImage.data}
      />
    </>
  );
}

// class DepthImageResult2 extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       width: null,
//       height: null,
//       data: null,
//     }
//   }

//   componentDidMount() {
//     fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'depth_image'))
//     .then(res => res.json())
//     .then((depthImage) => {
//       this.setState({
//         width: depthImage.width,
//         height: depthImage.height,
//         data: depthImage.data,
//       })
//     })
//     .catch(console.log);
//   }

//   render() {
//     return (
//       <div className="result-depth-image">
//         <ImageResult
//           width={this.state.width}
//           height={this.state.height}
//           data={this.state.data}
//         />
//       </div>
//     );
//   }
// }

function FeelingsResult(props) {
  const feelings = props.data;
  return (
    <>
      <Typography>
        Hunger: {feelings.hunger}
      </Typography>
      <Typography>
        Thirst: {feelings.thirst}
      </Typography>
      <Typography>
        Exhaustion: {feelings.exhaustion}
      </Typography>
      <Typography>
        Happiness: {feelings.happiness}
      </Typography>
    </>
  );
}

// class FeelingsResult2 extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       thirst: null,
//       hunger: null,
//       exhaustion: null,
//       happiness: null,
//     }
//   }

//   componentDidMount() {
//     fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'feelings'))
//     .then(res => res.json())
//     .then((feelings) => {
//       this.setState({
//         thirst: feelings.thirst,
//         hunger: feelings.hunger,
//         exhaustion: feelings.exhaustion,
//         happiness: feelings.happiness,
//       })
//     })
//     .catch(console.log);
//   }

//   render() {
//     return (
//       <div className="result-feelings">
//         <div className="result-feeling-hunger">
//           Hunger: {this.state.hunger}
//         </div>
//         <div className="result-feeling-thirst">
//           Thirst: {this.state.thirst}
//         </div>
//         <div className="result-feeling-exhaustion">
//           Exhaustion: {this.state.exhaustion}
//         </div>
//         <div className="result-feeling-happiness">
//           Happiness: {this.state.happiness}
//         </div>
//       </div>
//     );
//   }
// }

function Coordinate(props) {
  return <>{props.value.toFixed(3)}</>;
}

function TranslationResult(props) {
  return (
    <div className="result-pose-translation">
      Translation: (
        <Coordinate value={props.x} />,&nbsp;
        <Coordinate value={props.y} />,&nbsp;
        <Coordinate value={props.z} />
      )
    </div>
  );
}

// class TranslationResult2 extends React.Component {
//   render() {
//     return (
//       <div className="result-pose-translation">
//         Translation: (
//           <Coordinate value={this.props.x} />,&nbsp;
//           <Coordinate value={this.props.y} />,&nbsp;
//           <Coordinate value={this.props.z} />
//         )
//       </div>
//     );
//   }
// }

function RotationResult(props) {
  return (
    <div className="result-pose-rotation">
      Rotation: (
        <Coordinate value={props.x} />,&nbsp;
        <Coordinate value={props.y} />,&nbsp;
        <Coordinate value={props.z} />,&nbsp;
        <Coordinate value={props.w} />
      )
    </div>
  );
}

// class RotationResult2 extends React.Component {
//   render() {
//     return (
//       <div className="result-pose-rotation">
//         Rotation: (
//           <Coordinate value={this.props.x} />,&nbsp;
//           <Coordinate value={this.props.y} />,&nbsp;
//           <Coordinate value={this.props.z} />,&nbsp;
//           <Coordinate value={this.props.w} />
//         )
//       </div>
//     );
//   }
// }

function PoseResult(props) {
  const translation = props.data.translation;
  const rotation = props.data.rotation;

  return (
    <>
      <TranslationResult
        x={translation.x}
        y={translation.y}
        z={translation.z}
      />
      <RotationResult
        x={rotation.x}
        y={rotation.y}
        z={rotation.z}
        w={rotation.w}
      />
    </>
  );
}

// function PoseResult(props) {
//   function render(pose) {
//     const translation = pose.translation;
//     const rotation = pose.rotation;

//     return (
//       <div className="result-pose">
//         {translation &&
//           <TranslationResult
//             x={translation.x}
//             y={translation.y}
//             z={translation.z}
//           />
//         }
//         {rotation &&
//           <RotationResult
//             x={rotation.x}
//             y={rotation.y}
//             z={rotation.z}
//             w={rotation.w}
//           />
//         }
//       </div>
//     );
//   }

//   return (
//     <>
//       <DataLoader
//         url={getResultUrl(props.apiUrl, props.userId, props.snapshotId, 'pose')}
//         renderData={render}
//       />
//     </>
//   );
// }

// class PoseResult3 extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       translation: null,
//       rotation: null,
//     }
//   }

//   componentDidMount() {
//     fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'pose'))
//     .then(res => res.json())
//     .then((pose) => {
//       this.setState({
//         translation: pose.translation,
//         rotation: pose.rotation,
//       })
//     })
//     .catch(console.log);
//   }

//   render() {
//     const translation = this.state.translation;
//     const rotation = this.state.rotation;

//     return (
//       <div className="result-pose">
//         {translation &&
//           <TranslationResult
//             x={translation.x}
//             y={translation.y}
//             z={translation.z}
//           />
//         }
//         {rotation &&
//           <RotationResult
//             x={rotation.x}
//             y={rotation.y}
//             z={rotation.z}
//             w={rotation.w}
//           />
//         }
//       </div>
//     );
//   }
// }

function ResultHeader(props) {
  const classes = useStyles();
  return (
    <>
      <Typography className={classes.heading}>
        {props.name}
      </Typography>
    </>
  );
}

function Result(props) {
  const ResultComponent = getResultComponent(props.name);
  return (
    <>
      <CollectionItem
        onClick={props.onClick}
        isExpanded={props.isExpanded}
      >
        <ResultHeader name={props.name} />
        <DataLoader url={getResultUrl(props.apiUrl, props.userId, props.snapshotId, props.name)}>
          <ResultComponent {...props} />
        </DataLoader>
      </CollectionItem>
    </>
  );
}

function ResultCollection(props) {
  const [expanded, setExpanded] = React.useState(false);

  const isExpanded = (resultName) => (resultName === expanded);
  const handleClick = (resultName) => () => {
    setExpanded(isExpanded(resultName) ? false : resultName);
  };

  const resultItems = props.results.map((resultName) => {
    return (
      <Result
        key={resultName}
        apiUrl={props.apiUrl}
        userId={props.userId}
        snapshotId={props.snapshotId}
        name={resultName}
        isExpanded={isExpanded(resultName)}
        onClick={handleClick(resultName)}
      />
    );
  });
  const resultCollection = (resultItems.length > 0) ?
    <>{resultItems}</> :
    <>No results...</>;

  return (
    <Collection renderHeader={() => "Results"}>
      {resultCollection}
    </Collection>
  );
}

// function ResultCollection2(props) {
//   const resultItems = props.results.map((result) => {
//     const ResultComponent = resultComponents[result];
//     return (
//       <li key={result}>
//         <ResultComponent
//           apiUrl={props.apiUrl}
//           userId={props.userId}
//           snapshotId={props.snapshotId}
//         />
//       </li>
//     )
//   });
//   const resultCollection = (resultItems.length > 0) ?
//     <ul>{resultItems}</ul> :
//     'No results...';

//   return (
//     <div className="result-collection">
//       {resultCollection}
//     </div>
//   );
// }

// class ResultCollection3 extends React.Component {
//   render() {
//     const resultItems = this.props.results.map((result) => {
//       const ResultComponent = resultComponents[result];
//       return (
//         <li key={result}>
//           <ResultComponent
//             apiUrl={this.props.apiUrl}
//             userId={this.props.userId}
//             snapshotId={this.props.snapshotId}
//           />
//         </li>
//       )
//     });

//     return (
//       <div className="result-collection">
//         {resultItems.length > 0 &&
//           <ul>
//             {resultItems}
//           </ul>
//         }
//       </div>
//     );
//   }
// }

// === Functions ===

const resultComponents = {
  'color_image': ColorImageResult,
  'depth_image': DepthImageResult,
  'feelings': FeelingsResult,
  'pose': PoseResult,
};

function getResultComponent(resultName) {
  return resultComponents[resultName];
}

// === Exports ===

export default ResultCollection;
