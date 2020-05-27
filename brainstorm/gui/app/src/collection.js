import React from 'react';
import Collapse from '@material-ui/core/Collapse';
import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';

// import ExpansionPanel from '@material-ui/core/ExpansionPanel';
// import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
// import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';

import { useStyles } from './style.js';

// === Components ===

function CollectionItem(props) {
  const [summary, ...details] = props.children;
  return (
    <>
      <ListItem button onClick={props.onClick}>
        <ListItemText>
          {summary}
        </ListItemText>
        {props.isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
      </ListItem>
      <Collapse
        in={props.isExpanded}
        timeout="auto"
      >
        {details}
      </Collapse>
    </>
  );
}

function Collection(props) {
  const classes = useStyles();
  // const [expanded, setExpanded] = React.useState(false);

  // const handleClick = (itemId) => () => {
  //   setExpanded(itemId);
  // }

  // const items = props.items.map((item) => {
  //   const isExpanded = (expanded === item.id);
  //   return (
  //     <>
  //       <ListItem button onClick={handleClick(item.id)}>
  //         <ListItemText>
  //           {item.summary}
  //         </ListItemText>
  //         {isExpanded ? <ExpandLess /> : <ExpandMore />}
  //       </ListItem>
  //       <Collapse
  //         in={isExpanded}
  //         timeout="auto"
  //         unmountOnExit
  //       >
  //         {item.details}
  //       </Collapse>
  //     </>
  //   );
  // });
  // const itemCollection = (
  //   <>
  //     {(props.items.length > 0) ?
  //       props.items.map((item) => props.renderItem(item, expanded, handleClick)) :
  //       props.renderNoItems()
  //     }
  //   </>
  // );

  return (
    <List
      component='div'
      subheader={
        <ListSubheader component="div">
          {props.renderHeader()}
        </ListSubheader>
      }
      className={classes.root}
    >
      {props.children}
    </List>
  );
}

// === Exports ===

export {
  Collection,
  CollectionItem,
};
