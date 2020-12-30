import React, { useEffect, useState} from 'react';
import { NavLink, Container } from 'reactstrap';
import {
    HashRouter as Router,
    Switch,
    Route,
    useRouteMatch,
    Redirect,
    NavLink as RRNavLink
} from "react-router-dom";

import http from "../http-common"

import TweetsDashboard from "./SocialMedia/TweetsDashboard";
import ArticlesDashboard from "./WebArticles/ArticlesDashboard";
import TrendsDashboard from "./Trends/TrendsDashboard";
import WordCloud from './WebArticles/WordCloud';

// Source: https://bezkoder.com/react-hooks-crud-axios-api/
const Dashboard = props => {
    let { path, url } = useRouteMatch();
    
    const uid = props.uid
    const [tweets, setTweets] = useState([])
    const [tweetsFreq, setTweetsFreq] = useState(0)

    const [wordCloud, setWordCloud] = useState([])

    const [docFreq, setDocFreq] = useState(0)
    
    useEffect(() => {
        fetchWordCloud()
        retrieveTweets()
        fetchTweetFreq()
        fetchDocFreq()
    },[])

    // Retrieves tweets with sentiments - replaced here from Tweets.js
    const retrieveTweets = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets', formdata)
            .then(res => {
                setTweets(res.data)
            })
            .catch(e => {
                console.log(e)
            })
    }
    const fetchTweetFreq = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets/freq', formdata)
            .then(res => {
                setTweetsFreq(res.data);
                console.log('Tweet Freq' + res.data)
            })
            .catch(e => {
                console.log(e)
            })

    }

    

    const fetchWordCloud = () => {
        const formdata = new FormData();
        formdata.append("uid", uid);
        http.post('/documents/wordcloud', formdata)
            .then(res => {
                const tempCloud = []
                let keywords;
                keywords = res.data;

                let x = 0;
                for (let k in keywords) {
                    tempCloud[x] = {value: k, count: keywords[k]};
                    x += 1;
                }
                console.log(tempCloud)
                setWordCloud(tempCloud);
            })
            .catch(e => {
                console.log(e)
            })
    }
    const fetchDocFreq = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/documents/freq', formdata)

            .then(res => {
                setDocFreq(res.data);
            })
            .catch(e => {
                console.log(e)
            })

    }
    
    if(props.uid === 'null'){
        return <Redirect to={{ pathname: "/" }}/>
    }
    console.log("UID", props.uid)
    return (
        <React.Fragment>
            <Router basename={path}>
                <Container>
                    <Container>
                        <nav className="navbar navbar-expand-sm">
                            <div className="collapse navbar-collapse" id="navbarNav">
                                <ul className="navbar-nav">
                                    <li className="nav-item-menu">
                                        <NavLink exact to={`/sources`} tag={RRNavLink} activeClassName="active">Web Articles</NavLink>
                                    </li>
                                    <li className="nav-item-menu">
                                        <NavLink exact to={`/tweets`} tag={RRNavLink} activeClassName="active">Tweets</NavLink>
                                    </li>
                                    <li className="nav-item-menu">
                                        <NavLink exact to={`${url}/trends`} tag={RRNavLink} activeClassName="active">Trends</NavLink>
                                    </li>
                                </ul>
                            </div>
                        </nav>
                    </Container>
                    <Container>
                        <Switch>
                            <Route exact path={`/sources`}>
                                <ArticlesDashboard className="center-body" uid={uid} wordCloud={wordCloud} docFreq={docFreq} tweetsFreq={tweetsFreq}/>
                            </Route>
                            <Route exact path={`/tweets`}>
                                <TweetsDashboard uid={uid} tweets={tweets} tweetsFreq={tweetsFreq}/>
                            </Route>
                            <Route exact path={`/trends`}>
                                <TweetsDashboard uid={uid}/>
                            </Route>
                        </Switch>
                    </Container>
                </Container>
            </Router>
        </React.Fragment>
    )
}



export default Dashboard;