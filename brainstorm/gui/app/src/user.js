import React from 'react';
// import ExpansionPanel from '@material-ui/core/ExpansionPanel';
// import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
// import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
// import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import { Collection, CollectionItem } from './collection.js';
import { DataLoader } from './data.js';
import SnapshotCollection from './snapshot.js';
import { useStyles } from './style.js';
import { getUsersUrl, getUserUrl } from './urls.js';

// === Components ===

function UserInformation(props) {
  const birthday = new Date(props.birthday).toLocaleDateString();
  const gender = getGenderString(props.gender);

  return (
    <>
      <Typography>
        Birthday: {birthday}
        <br />
        Gender: {gender}
      </Typography>
    </>
  );
}

function UserHeader(props) {
  const classes = useStyles();

  return (
    <>
      <Typography className={classes.heading}>
        {props.name}
      </Typography>
      <Typography className={classes.secondaryHeading}>
        {props.userId}
      </Typography>
    </>
  );
}

function UserWithData(props) {
  const userData = props.data;
  // const userData = useFetchData(getUserUrl(props.apiUrl, props.userId));
  // if (!userData) {
  //   return <><CircularProgress /></>;
  // }

  return (
    <>
      <CollectionItem
        onClick={props.onClick}
        isExpanded={props.isExpanded}
      >
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
      </CollectionItem>
    </>
  );
}

// function UserWithData2(props) {
//   const userData = props.data;
//   // const userData = useFetchData(getUserUrl(props.apiUrl, props.userId));
//   // if (!userData) {
//   //   return <><CircularProgress /></>;
//   // }

//   return (
//     <>
//       <ExpansionPanel
//         expanded={props.isExpanded}
//         onChange={props.onChange}
//       >
//         <ExpansionPanelSummary
//           expandIcon={<ExpandMoreIcon />}
//           id={`panel${props.userId}-header`}
//         >
//           <UserHeader
//             userId={props.userId}
//             name={props.name}
//           />
//         </ExpansionPanelSummary>
//         <ExpansionPanelDetails>
//           <div>
//             <UserInformation
//               birthday={userData.birthday}
//               gender={userData.gender}
//             />
//             <SnapshotCollection
//               apiUrl={props.apiUrl}
//               userId={props.userId}
//             />
//           </div>
//         </ExpansionPanelDetails>
//       </ExpansionPanel>
//     </>
//   );
// }

function User(props) {
  return (
    <DataLoader url={getUserUrl(props.apiUrl, props.userId)}>
      <UserWithData {...props} />
    </DataLoader>
  );
}

function UserCollection(props) {
  // const classes = useStyles();
  const [expanded, setExpanded] = React.useState(false);

  const isExpanded = (userId) => (userId === expanded);
  const handleClick = (userId) => () => {
    setExpanded(isExpanded(userId) ? false : userId);
  };

  // const handleChange = (panel) => (event, isExpanded) => {
  //   setExpanded(isExpanded ? panel : false);
  // };

  // const users = useFetchData(getUsersUrl(props.apiUrl));
  // if (!users) {
  //   return <><CircularProgress /></>;
  // }

  const userItems = props.data.map((minimalUser) => {
    const userId = minimalUser.user_id;
    return (
      <User
        key={`${userId}`}
        apiUrl={props.apiUrl}
        userId={userId}
        name={minimalUser.name}
        isExpanded={isExpanded(userId)}
        onClick={handleClick(userId)}
      />
    );
  });
  const userCollection = (userItems.length > 0) ?
    <>{userItems}</> :
    <>No users...</>;

  // const renderUser = (minimalUser, expandedUserId, handleClick) => {
  //   const userId = minimalUser.user_id;
  //   return (
  //     <User
  //       key={`${userId}`}
  //       apiUrl={props.apiUrl}
  //       userId={userId}
  //       name={minimalUser.name}
  //       onClick={handleClick(userId)}
  //       isExpanded={expandedUserId === userId}
  //     />
  //   );
  // }
  // const renderNoUsers = () => (
  //   <>No users...</>
  // );

  return (
    <Collection renderHeader={() => "Users"}>
      {userCollection}
    </Collection>
  );
}

function Users(props) {
  return (
    <DataLoader url={getUsersUrl(props.apiUrl)}>
      <UserCollection apiUrl={props.apiUrl} />
    </DataLoader>
  );
}

// function UserCollection(props) {
//   function renderUsers(users) {
//     const userItems = users.map((minimalUser) => (
//       <li key={minimalUser.user_id.toString()}>
//         <User
//           apiUrl={props.apiUrl}
//           userId={minimalUser.user_id}
//           name={minimalUser.name}
//         />
//       </li>
//     ));
//     const userCollection = (userItems.length > 0) ?
//       <ul>{userItems}</ul> :
//       'No users...';

//     return (
//       <div className="user-collection">
//         {userCollection}
//       </div>
//     );
//   }

//   return (
//     <>
//       <DataLoader
//         url={getUsersUrl(props.apiUrl)}
//         renderData={renderUsers}
//       />
//     </>
//   );
// }

// === Functions ===

function getGenderString(gender) {
  const genderMap = {
    'm': 'Male',
    'f': 'Female',
  };
  return genderMap[gender] || 'Other';
}

// === Exports ===

// export default UserCollection;
export default Users;
