import React from "react";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Input from "@material-ui/core/Input";
import Paper from "@material-ui/core/Paper";
import withStyles from "@material-ui/core/styles/withStyles";
import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import { createMuiTheme, formatMs } from "@material-ui/core/styles";
import styles from "./styles";
import { ThemeProvider, Grid, Toolbar, Card } from "@material-ui/core";
import { Link } from "react-router-dom";
import AppBar from "@material-ui/core/AppBar";
import IconButton from "@material-ui/core/IconButton";
import InputBase from "@material-ui/core/InputBase";
import Badge from "@material-ui/core/Badge";
import MenuItem from "@material-ui/core/MenuItem";
import Menu from "@material-ui/core/Menu";
import MenuIcon from "@material-ui/icons/Menu";
import "./aesthetic.css";
import PacificoRegular from "./fonts/Pacifico-Regular.ttf";
import KaushanScript from "./fonts/KaushanScript-Regular.ttf";
import AOS from "aos";

import "aos/dist/aos.css"; // You can also use <link> for styles
// ..

class HomeComponent extends React.Component {
  render() {
    const { classes } = this.props;
    const darkTheme = createMuiTheme({
      palette: {
        type: "light"
      }
    });

    const kaushan = {
      fontFamily: "Kaushan Script",

      src: `local('KaushanScript-Regular'),
      url(${KaushanScript}) format('ttf')`
    };

    const fontTheme = createMuiTheme({
      typography: {
        fontFamily: "Kaushan Script"
      },
      overrides: {
        MuiCssBaseline: {
          "@global": {
            "@font-face": [kaushan]
          }
        }
      }
    });

    const pacifico = {
      fontFamily: "Pacifico",
      src: `local('Pacifico-Regular'),
      url(${PacificoRegular})format('ttf)`
    };

    const pacificoTheme = createMuiTheme({
      typography: {
        fontFamily: "Pacifico"
      },
      overrides: {
        MuiCssBaseline: {
          "@global": {
            "@font-face": [pacifico]
          }
        }
      }
    });

    AOS.init({
      duration: 700
    });

    return (
      <body>
        <div className="navbar">
          <ul>
            <li>
              <a class="active" href="#home">
                Home
              </a>
            </li>
            <li>
              <a href="#news">News</a>
            </li>
            <li>
              <a href="#contact">Contact</a>
            </li>
            <li>
              <a href="#abt">About</a>
            </li>
          </ul>
        </div>

        <div className="home" id="home">
          <div className="logo">
            <img src={require("./images/logo.png")} />
            <h1 className="no-margin-top">Freelanco</h1>
          </div>

          <h6 className="centre-h4">~Your need is our deed~</h6>
        </div>

        <div className="about " id="abt">
          <Grid container justify="center" spacing={2}>
            <div className="about-tag">
              <Grid item xs>
                <ThemeProvider theme={fontTheme}>
                  <Typography component="h2" variant="h5">
                    Hello
                  </Typography>
                </ThemeProvider>
              </Grid>
            </div>

            <Grid item xs></Grid>
            <Grid item xs>
              <main className={classes.main}>
                <div data-aos="fade-right">
                  <Paper className={classes.paper} elevation={5}>
                    <p className="about-us">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Quisque orci felis, molestie a gravida eget, vulputate eu
                      turpis. In tristique auctor erat, in faucibus lectus
                      varius sodales. Nam laoreet odio vitae imperdiet
                      ultricies. Sed molestie dui quis ullamcorper ultricies.
                      Cras elementum feugiat faucibus. Duis vel interdum libero.
                      Nulla non sollicitudin ex. Nunc velit nisl, pharetra vitae
                      molestie non, auctor at lorem. Suspendisse potenti.
                      Suspendisse faucibus sed purus sit amet viverra. Praesent
                      et tristique sem. Suspendisse accumsan arcu vel nibh
                      cursus mollis. Nullam nec sapien et lectus lobortis
                      fermentum id sit amet sapien. Sed sed sem sit amet nunc
                      aliquam lacinia quis eu leo. Cras eleifend fermentum
                      ultricies. Nulla facilisi.
                    </p>
                  </Paper>
                </div>
              </main>
            </Grid>
          </Grid>
        </div>
      </body>
    );
  }
}
export default withStyles(styles)(HomeComponent);
