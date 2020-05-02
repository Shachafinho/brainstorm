import React from 'react';
import DataLoader from './data.js';
import { getResultUrl } from './urls.js';

// === Components ===

function ImageResult(props) {
  return (
    <div className="result-base-image">
      Width: {props.width},
      Height: {props.height},
      Data: {props.data}
    </div>
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
  function render(colorImage) {
    return (
      <div className="result-color-image">
        <ImageResult
          width={colorImage.width}
          height={colorImage.height}
          data={colorImage.data}
        />
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getResultUrl(props.apiUrl, props.userId, props.snapshotId, 'color_image')}
        renderData={render}
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
  function render(depthImage) {
    return (
      <div className="result-depth-image">
        <ImageResult
          width={depthImage.width}
          height={depthImage.height}
          data={depthImage.data}
        />
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getResultUrl(props.apiUrl, props.userId, props.snapshotId, 'depth_image')}
        renderData={render}
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
  function render(feelings) {
    return (
      <div className="result-feelings">
        <div className="result-feeling-hunger">
          Hunger: {feelings.hunger}
        </div>
        <div className="result-feeling-thirst">
          Thirst: {feelings.thirst}
        </div>
        <div className="result-feeling-exhaustion">
          Exhaustion: {feelings.exhaustion}
        </div>
        <div className="result-feeling-happiness">
          Happiness: {feelings.happiness}
        </div>
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getResultUrl(props.apiUrl, props.userId, props.snapshotId, 'feelings')}
        renderData={render}
      />
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
  return (
    <>
      {props.value.toFixed(3)}
    </>
  );
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
  function render(pose) {
    const translation = pose.translation;
    const rotation = pose.rotation;

    return (
      <div className="result-pose">
        {translation &&
          <TranslationResult
            x={translation.x}
            y={translation.y}
            z={translation.z}
          />
        }
        {rotation &&
          <RotationResult
            x={rotation.x}
            y={rotation.y}
            z={rotation.z}
            w={rotation.w}
          />
        }
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getResultUrl(props.apiUrl, props.userId, props.snapshotId, 'pose')}
        renderData={render}
      />
    </>
  );
}

// class PoseResult2 extends React.Component {
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

const resultComponents = {
  'color_image': ColorImageResult,
  'depth_image': DepthImageResult,
  'feelings': FeelingsResult,
  'pose': PoseResult,
};

function ResultCollection(props) {
  const resultItems = props.results.map((result) => {
    const ResultComponent = resultComponents[result];
    return (
      <li key={result}>
        <ResultComponent
          apiUrl={props.apiUrl}
          userId={props.userId}
          snapshotId={props.snapshotId}
        />
      </li>
    )
  });
  const resultCollection = (resultItems.length > 0) ?
    <ul>{resultItems}</ul> :
    'No results...';

  return (
    <div className="result-collection">
      {resultCollection}
    </div>
  );
}

// class ResultCollection extends React.Component {
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

// === Exports ===

export default ResultCollection;
