import React from 'react';
import DataLoader from './data.js';
import SnapshotCollection from './snapshot.js';
import { getUsersUrl, getUserUrl } from './urls.js';

// === Components ===

function UserInformation(props) {
  const birthday = new Date(props.birthday).toLocaleDateString();
  const gender = getGenderString(props.gender);

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

// class UserInformation2 extends React.Component {
//   render() {
//     const birthday = new Date(this.props.birthday).toLocaleDateString();
//     const gender = getGenderString(this.props.gender);

//     return (
//       <div className="user-information">
//         <div className="user-birthday">
//           Birthday: {birthday}
//         </div>
//         <div className="user-gender">
//           Gender: {gender}
//         </div>
//       </div>
//     );
//   }
// }

function UserHeader(props) {
  return (
    <div className="user-header">
      <div className="user-id">
        {props.userId}
      </div>
      <div className="user-name">
        {props.name}
      </div>
    </div>
  );
}

// class UserHeader2 extends React.Component {
//   render() {
//     return (
//       <div className="user-header">
//         <div className="user-id">
//           {this.props.userId}
//         </div>
//         <div className="user-name">
//           {this.props.name}
//         </div>
//       </div>
//     );
//   }
// }

function User(props) {
  function renderUser(userData) {
    return (
      <div className="user">
        <UserHeader
          userId={props.userId}
          name={props.name}
        />
        <UserInformation
          birthday={userData.birthday}
          gender={userData.gender}
        />
        <SnapshotCollection
          apiUrl={props.apiUrl}
          userId={props.userId}
        />
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getUserUrl(props.apiUrl, props.userId)}
        renderData={renderUser}
      />
    </>
  );
}

// class User2 extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       birthday: '',
//       gender: '',
//     };
//   }

//   componentDidMount() {
//     fetch(getUserUrl(this.props.apiUrl, this.props.userId))
//     .then(res => res.json())
//     .then((user) => {
//       this.setState({
//         birthday: user.birthday,
//         gender: user.gender,
//       })
//     })
//     .catch(console.log);
//   }

//   render() {
//     return (
//       <div className="user">
//         <UserHeader
//           userId={this.props.userId}
//           name={this.props.name}
//         />
//         <UserInformation
//           birthday={this.state.birthday}
//           gender={this.state.gender}
//         />
//         <SnapshotCollection
//           apiUrl={this.props.apiUrl}
//           userId={this.props.userId}
//         />
//       </div>
//     );
//   }
// }

function UserCollection(props) {
  function renderUsers(users) {
    const userItems = users.map((minimalUser) => (
      <li key={minimalUser.user_id.toString()}>
        <User
          apiUrl={props.apiUrl}
          userId={minimalUser.user_id}
          name={minimalUser.name}
        />
      </li>
    ));
    const userCollection = (userItems.length > 0) ?
      <ul>{userItems}</ul> :
      'No users...';

    return (
      <div className="user-collection">
        {userCollection}
      </div>
    );
  }

  return (
    <>
      <DataLoader
        url={getUsersUrl(props.apiUrl)}
        renderData={renderUsers}
      />
    </>
  );
}

// === Functions ===

function getGenderString(gender) {
  const genderMap = {
    'm': 'Male',
    'f': 'Female',
  };
  return genderMap[gender] || 'Other';
}

// === Exports ===

export default UserCollection;
