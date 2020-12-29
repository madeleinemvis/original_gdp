import React, {useState} from 'react';
import { NavLink, Container } from 'reactstrap';
import {
    HashRouter as Router,
    Switch,
    Route,
    useRouteMatch,
    Redirect,
    NavLink as RRNavLink
} from "react-router-dom";

import TweetsDashboard from "./SocialMedia/TweetsDashboard";
import ArticlesDashboard from "./WebArticles/ArticlesDashboard";
import TrendsDashboard from "./Trends/TrendsDashboard";

// Source: https://bezkoder.com/react-hooks-crud-axios-api/
const Dashboard = props => {
    const [uid, setUid] = useState(props.uid)
    let { path, url } = useRouteMatch();
    if(uid.toString() === 'null'){
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
                                <Sources className="center-body" uid={uid}/>
                            </Route>
                            <Route exact path={`/tweets`}>
                                <SocialMedia uid={uid}/>
                            </Route>
                        </Switch>
                    </Container>
                </Container>
            </Router>
        </React.Fragment>
    )
}

export default Dashboard;