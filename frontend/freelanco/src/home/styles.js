import { Backdrop } from "@material-ui/core";
import { fade, makeStyles } from "@material-ui/core/styles";

const styles = theme => ({
  main: {
    width: "auto",
    display: "block", // Fix IE 11 issue.
    marginLeft: theme.spacing.unit * 10,
    marginRight: theme.spacing.unit * 10,
    [theme.breakpoints.up(300 + theme.spacing.unit * 3 * 3)]: {
      width: 400,
      marginLeft: "auto",
      marginRight: "150px"
    }
  },

  paper: {
    width: "500px",
    display: "block", // Fix IE 11 issue.
    marginLeft: theme.spacing.unit * 1,
    marginRight: theme.spacing.unit * 10,
    marginTop: theme.spacing.unit * 1,
    display: "block",
    height: "400px",
    flexDirection: "row",
    alignItems: "right",

    padding: `${theme.spacing.unit * 5}px ${theme.spacing.unit * 2}px ${theme
      .spacing.unit * 5}px`
  }
});
export default styles;
