import React from 'react';
import ButtonBase from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogContent from '@material-ui/core/DialogContent';
import { makeStyles } from '@material-ui/core/styles';

// === Components ===

function ImageButton(props) {
  const classes = useStyles();
  return (
    <ButtonBase
      focusRipple
      onClick={props.onClick}
    >
      <img className={classes.imageButton} src={props.src} alt='Show'/>
    </ButtonBase>
  );
}

function ImageDialog(props) {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  }
  const handleClose = () => {
    setOpen(false);
  }

  return (
    <React.Fragment className={classes.imageDialog}>
      <ImageButton
        onClick={handleClickOpen}
        width={props.width}
        height={props.height}
        src={props.data}
      />
      <Dialog
        className={classes.dialog}
        maxWidth={false}
        open={open}
        onClose={handleClose}
      >
        <DialogContent className={classes.dialogContent}>
          <img src={props.data} alt={props.data} />
        </DialogContent>
      </Dialog>
    </React.Fragment>
  );
}

// === Functions ===

const useStyles = makeStyles((theme) => ({
  dialog: {
    padding: 0,
    margin: 0,
  },
  dialogContent: {
    margin: 0,
    maxHeight: '100%',
    maxWidth: '100%',
  },
  imageDialog: {
    display: 'flex',
    flexWrap: 'wrap',
    minWidth: 300,
    width: '100%',
  },
  imageButton: {
    maxHeight: 200,
  },
}));

// === Exports ===

export {
  ImageDialog,
};
