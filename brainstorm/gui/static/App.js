class ImageResult extends React.Component {
  render() {
    return (
      <div className="result-base-image">
        Width: {this.props.width},
        Height: {this.props.height},
        Data: {this.props.data}
      </div>
    )
  }
}

class ColorImageResult extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      width: null,
      height: null,
      data: null,
    }
  }

  componentDidMount() {
    fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'color_image'))
    .then(res => res.json())
    .then((colorImage) => {
      this.setState({
        width: colorImage.width,
        height: colorImage.height,
        data: colorImage.data,
      })
    })
    .catch(console.log);
  }

  render() {
    return (
      <div className="result-color-image">
        <ImageResult
          width={this.state.width}
          height={this.state.height}
          data={this.state.data}
        />
      </div>
    );
  }
}

class DepthImageResult extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      width: null,
      height: null,
      data: null,
    }
  }

  componentDidMount() {
    fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'depth_image'))
    .then(res => res.json())
    .then((depthImage) => {
      this.setState({
        width: depthImage.width,
        height: depthImage.height,
        data: depthImage.data,
      })
    })
    .catch(console.log);
  }

  render() {
    return (
      <div className="result-depth-image">
        <ImageResult
          width={this.state.width}
          height={this.state.height}
          data={this.state.data}
        />
      </div>
    );
  }
}

class FeelingsResult extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      thirst: null,
      hunger: null,
      exhaustion: null,
      happiness: null,
    }
  }

  componentDidMount() {
    fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'feelings'))
    .then(res => res.json())
    .then((feelings) => {
      this.setState({
        thirst: feelings.thirst,
        hunger: feelings.hunger,
        exhaustion: feelings.exhaustion,
        happiness: feelings.happiness,
      })
    })
    .catch(console.log);
  }

  render() {
    return (
      <div className="result-feelings">
        <div className="result-feeling-hunger">
          Hunger: {this.state.hunger}
        </div>
        <div className="result-feeling-thirst">
          Thirst: {this.state.thirst}
        </div>
        <div className="result-feeling-exhaustion">
          Exhaustion: {this.state.exhaustion}
        </div>
        <div className="result-feeling-happiness">
          Happiness: {this.state.happiness}
        </div>
      </div>
    );
  }
}

function Coordinate(props) {
  return (
    <React.Fragment>
      {props.value.toFixed(3)}
    </React.Fragment>
  );
}

class TranslationResult extends React.Component {
  render() {
    return (
      <div className="result-pose-translation">
        Translation: (
          <Coordinate value={this.props.x} />,&nbsp;
          <Coordinate value={this.props.y} />,&nbsp;
          <Coordinate value={this.props.z} />
        )
      </div>
    );
  }
}

class RotationResult extends React.Component {
  render() {
    return (
      <div className="result-pose-rotation">
        Rotation: (
          <Coordinate value={this.props.x} />,&nbsp;
          <Coordinate value={this.props.y} />,&nbsp;
          <Coordinate value={this.props.z} />,&nbsp;
          <Coordinate value={this.props.w} />
        )
      </div>
    );
  }
}

class PoseResult extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      translation: null,
      rotation: null,
    }
  }

  componentDidMount() {
    fetch(getResultUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId, 'pose'))
    .then(res => res.json())
    .then((pose) => {
      this.setState({
        translation: pose.translation,
        rotation: pose.rotation,
      })
    })
    .catch(console.log);
  }

  render() {
    const translation = this.state.translation;
    const rotation = this.state.rotation;

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
}

const resultComponents = {
  'color_image': ColorImageResult,
  'depth_image': DepthImageResult,
  'feelings': FeelingsResult,
  'pose': PoseResult,
};

class ResultCollection extends React.Component {
  render() {
    const resultItems = this.props.results.map((result) => {
      const ResultComponent = resultComponents[result];
      return (
        <li key={result}>
          <ResultComponent
            apiUrl={this.props.apiUrl}
            userId={this.props.userId}
            snapshotId={this.props.snapshotId}
          />
        </li>
      )
    });

    return (
      <div className="result-collection">
        {resultItems.length > 0 &&
          <ul>
            {resultItems}
          </ul>
        }
      </div>
    );
  }
}

class SnapshotInformation extends React.Component {
  render() {
    return (
      <div className="snapshot-information">
      </div>
    );
  }
}

class SnapshotHeader extends React.Component {
  render() {
    const timestamp = new Date(this.props.timestamp).toLocaleString();

    return (
      <div className="snapshot-header">
        <div className="snapshot-id">
          {this.props.snapshotId}
        </div>
        <div className="snapshot-timestamp">
          {timestamp}
        </div>
      </div>
    );
  }
}

class Snapshot extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: [],
    }
  }

  componentDidMount() {
    fetch(getSnapshotUrl(this.props.apiUrl, this.props.userId, this.props.snapshotId))
    .then(res => res.json())
    .then((snapshot) => {
      this.setState({
        results: snapshot.results,
      })
    })
    .catch(console.log);
  }

  render() {
    const results = this.state.results;
    return (
      <div className="snapshot">
        <SnapshotHeader
          snapshotId={this.props.snapshotId}
          timestamp={this.props.timestamp}
        />
        <SnapshotInformation />
        {results.length > 0 &&
          <ResultCollection
            apiUrl={this.props.apiUrl}
            userId={this.props.userId}
            snapshotId={this.props.snapshotId}
            results={this.state.results}
          />
        }
      </div>
    );
  }
}

class SnapshotCollection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      snapshots: [],
    }
  }

  componentDidMount() {
    fetch(getSnapshotsUrl(this.props.apiUrl, this.props.userId))
    .then(res => res.json())
    .then((minimalSnapshots) => {
      this.setState({snapshots: minimalSnapshots})
    })
    .catch(console.log);
  }

  render() {
    const snapshotItems = this.state.snapshots.map((minimalSnapshot) => (
      <li key={minimalSnapshot.snapshot_id.toString()}>
        <Snapshot
          apiUrl={this.props.apiUrl}
          userId={this.props.userId}
          snapshotId={minimalSnapshot.snapshot_id}
          timestamp={minimalSnapshot.timestamp}
        />
      </li>
    ));
    return (
      <div className="snapshot-collection">
        {snapshotItems.length > 0 &&
          <ul>
            {snapshotItems[0]}
          </ul>
        }
      </div>
    );
  }
}

function getGenderString(gender) {
  const genderMap = {
    'm': 'Male',
    'f': 'Female',
  };
  return genderMap[gender] || 'Other';
}

class UserInformation extends React.Component {
  render() {
    const birthday = new Date(this.props.birthday).toLocaleDateString();
    const gender = getGenderString(this.props.gender);

    return (
      <div className="user-information">
        <div className="user-birthday">
          Birthday: {birthday}
        </div>
        <div className="user-gender">
          Gender: {gender}
        </div>
      </div>
    );
  }
}

class UserHeader extends React.Component {
  render() {
    return (
      <div className="user-header">
        <div className="user-id">
          {this.props.userId}
        </div>
        <div className="user-name">
          {this.props.name}
        </div>
      </div>
    );
  }
}

class User extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      birthday: '',
      gender: '',
    };
  }

  componentDidMount() {
    fetch(getUserUrl(this.props.apiUrl, this.props.userId))
    .then(res => res.json())
    .then((user) => {
      this.setState({
        birthday: user.birthday,
        gender: user.gender,
      })
    })
    .catch(console.log);
  }

  render() {
    return (
      <div className="user">
        <UserHeader
          userId={this.props.userId}
          name={this.props.name}
        />
        <UserInformation
          birthday={this.state.birthday}
          gender={this.state.gender}
        />
        <SnapshotCollection
          apiUrl={this.props.apiUrl}
          userId={this.props.userId}
        />
      </div>
    );
  }
}

class UserCollection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      users: [],
    };
  }

  componentDidMount() {
    fetch(getUsersUrl(this.props.apiUrl))
    .then(res => res.json())
    .then((minimalUsers) => {
      sleep(3000).then(() => {
        this.setState({users: minimalUsers})
      });
      // this.setState({users: minimalUsers})
    })
    .catch(console.log);
  }

  render() {
    const users = this.state.users;
    const userItems = users && users.map((minimalUser) => (
      <li key={minimalUser.user_id.toString()}>
        <User
          apiUrl={this.props.apiUrl}
          userId={minimalUser.user_id}
          name={minimalUser.name}
        />
      </li>
    ));

    return (
      <div className="user-collection">
        <ContentLoader
          isLoaded={Boolean(users)}
          render={() => (<div>Content</div>)}
          // {userItems.length > 0 &&
          //   <ul>
          //     {userItems}
          //   </ul>
          // }
        />
      </div>
    );
  }
}

class ContentLoader extends React.Component {
  render() {
    const loadingType = this.props.loadingType || 'spinningBubbles';
    return (
      <div className="content-loader">
        {this.props.isLoaded ?
          this.props.render() :
          <div>
            Loading...
          </div>
          // <ReactLoading type={loadingType} />
        }
      </div>
    );
  }
}

class App extends React.Component {
  render() {
    return (
      <UserCollection apiUrl={this.props.apiUrl} />
    );
  }
}


function sleep(ms) {
  // TODO: DELETE ME
  return new Promise(resolve => setTimeout(resolve, ms));
}


function getUsersUrl(baseUrl) {
  return baseUrl + '/users';
}

function getUserUrl(baseUrl, userId) {
  return getUsersUrl(baseUrl) + '/' + userId.toString();
}

function getSnapshotsUrl(baseUrl, userId) {
  return getUserUrl(baseUrl, userId) + '/snapshots';
}

function getSnapshotUrl(baseUrl, userId, snapshotId) {
  return getSnapshotsUrl(baseUrl, userId) + '/' + snapshotId.toString();
}

function getResultUrl(baseUrl, userId, snapshotId, resultName) {
  return getSnapshotUrl(baseUrl, userId, snapshotId) + '/' + resultName;
}
