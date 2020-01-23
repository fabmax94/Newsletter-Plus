import React, {useState, useEffect} from "react";
import axios from 'axios';
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import {makeStyles} from "@material-ui/core/styles";

// @material-ui/icons

// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
import Parallax from "components/Parallax/Parallax.js";

import styles from "assets/jss/material-kit-react/views/landingPage.js";

// Sections for this page
import NewsLandingSection from "./Sections/NewsLandingSection.js";

;

const dashboardRoutes = [];

const useStyles = makeStyles(styles);

export default function HomePage(props) {
    const classes = useStyles();
    const [lastNews, setLastNews] = useState([]);
    const [bestNews, setBestNews] = useState([]);

    const loadNews = (typeNews) => {
        switch (typeNews) {
            case 'last':
                axios.get('http://127.0.0.1:8000/api/news/last').then((response => setLastNews(response.data)));
                break;
            case 'best':
                axios.get('http://127.0.0.1:8000/api/news/best').then((response => setBestNews(response.data)));
                break;
            default:
                break;
        }
    };
    useEffect(() => {
        loadNews('last');
        loadNews('best');
    }, []);

    const {...rest} = props;
    return (
        <div>
            <Header
                color="transparent"
                routes={dashboardRoutes}
                brand="Newsletter Plus"
                rightLinks={<HeaderLinks/>}
                fixed
                changeColorOnScroll={{
                    height: 400,
                    color: "white"
                }}
                {...rest}
            />
            <Parallax filter image={require("assets/img/landing-bg.jpg")}>
                <div className={classes.container}>
                    <GridContainer>
                        <GridItem xs={12} sm={12} md={6}>
                            <h1 className={classes.title}>Notícias de tecnologia</h1>
                            <h4>
                                Every landing page needs a small description after the big bold
                                title, that{"'"}s why we added this text here. Add here all the
                                information that can make you or your product create the first
                                impression.
                            </h4>
                        </GridItem>
                    </GridContainer>
                </div>
            </Parallax>
            <div className={classNames(classes.main, classes.mainRaised)}>
                <div className={classes.container}>
                    <NewsLandingSection section={"Last News"} items={lastNews}/>
                    <NewsLandingSection section={"Best News"} items={bestNews}/>
                </div>
            </div>
            <Footer/>
        </div>
    );
}
