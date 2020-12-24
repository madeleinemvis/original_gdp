import React from 'react';
import { NavLink, Container } from 'reactstrap';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    useRouteMatch,
    Redirect,
    NavLink as RRNavLink
} from "react-router-dom";

import Sources from "./WebArticles/Sources";
import TweetsDashboard from "./SocialMedia/TweetsDashboard";
import ArticlesDashboard from "./WebArticles/ArticlesDashboard";

// Source: https://bezkoder.com/react-hooks-crud-axios-api/
const Dashboard = props => {
    const uid = props.uid
    let { path, url } = useRouteMatch();
    if(props.uid === 'null'){
        return <Redirect to={{ pathname: "/" }}/>
    }
    return (
        <React.Fragment>
            <Router>
                <Container>
                    {/*TODO: active buttons*/}
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
                                        <NavLink exact to={`${url}/causal`} tag={RRNavLink} activeClassName="active">Trends</NavLink>
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
                        <Route exact path={`${path}/causal`}>
                            <TweetsDashboard uid={uid}/>
                        </Route>
                    </Switch>
                </Container>
            </Router>
        </React.Fragment>
    )
}

export default Dashboard;