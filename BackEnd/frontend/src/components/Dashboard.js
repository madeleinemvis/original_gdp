import React, {useState} from 'react';
import { NavLink, Container } from 'reactstrap';
import {
    BrowserRouter as Router,
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
            <Router>
                <Container>
                    <Container>
                        <nav className="navbar navbar-expand-sm">
                            <div className="collapse navbar-collapse" id="navbarNav">
                                <ul className="navbar-nav">
                                    <li className="nav-item-menu">
                                        <NavLink exact to={`${url}/sources`} tag={RRNavLink} activeClassName="active">Web Articles</NavLink>
                                    </li>
                                    <li className="nav-item-menu">
                                        <NavLink exact to={`${url}/tweets`} tag={RRNavLink} activeClassName="active">Tweets</NavLink>
                                    </li>
                                    <li className="nav-item-menu">
                                        <NavLink exact to={`${url}/trends`} tag={RRNavLink} activeClassName="active">Trends</NavLink>
                                    </li>
                                </ul>
                            </div>
                        </nav>
                    </Container>
                    <Switch>
                        <Route exact path={`${path}/sources`}>
                            <ArticlesDashboard className="center-body" uid={uid}/>
                        </Route>
                        <Route exact path={`${path}/tweets`}>
                            <TweetsDashboard uid={uid}/>
                        </Route>
                        <Route exact path={`${path}/trends`}>
                            <TrendsDashboard uid={uid}/>
                        </Route>
                    </Switch>
                </Container>
            </Router>
        </React.Fragment>
    )
}

export default Dashboard;