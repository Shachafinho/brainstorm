import React from 'react';
import Collapse from '@material-ui/core/Collapse';
// import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ChevronRight from '@material-ui/icons/ChevronRight';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';

import PropTypes from 'prop-types';
import { fade, makeStyles } from '@material-ui/core/styles';
import { useSpring, animated } from 'react-spring';

// import ExpansionPanel from '@material-ui/core/ExpansionPanel';
// import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
// import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';

// === Components ===

function TransitionComponent(props) {
  const style = useSpring({
    from: { opacity: 0, transform: 'translate3d(40px,0,0)' },
    to: { opacity: props.in ? 1 : 0, transform: `translate3d(${props.in ? 0 : 40}px,0,0)` },
  });

  return (
    <animated.div style={style}>
      <Collapse {...props} />
    </animated.div>
  );
}
TransitionComponent.propTypes = {
  /**
   * Show the component; triggers the enter or exit states
   */
  in: PropTypes.bool,
};

function CollectionItem(props) {
  const classes = useStyles();
  const [summary, ...details] = props.children;

  return (
    <div>
      <ListItem button
        onClick={props.onClick}
      >
        <ListItemIcon>
          {props.isExpanded ? <ExpandMoreIcon /> : <ChevronRight />}
        </ListItemIcon>
        <ListItemText>
          {summary}
        </ListItemText>
      </ListItem>
      <TransitionComponent
        in={props.isExpanded}
        timeout="auto"
      >
        <ListItem>
          <ListItemText inset>
            {details}
          </ListItemText>
        </ListItem>
      </TransitionComponent>
    </div>
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

// === Functions ===

const useStyles = makeStyles((theme) => ({
  collectionItem: {
    marginLeft: theme.spacing(2),
    paddingLeft: theme.spacing(2),
    borderLeft: `1px dashed ${fade(theme.palette.text.primary, 0.4)}`,
  },
  collectionItemSummary: {
    paddingLeft: theme.spacing(2),
  }
}));

// === Exports ===

export {
  Collection,
  CollectionItem,
};
