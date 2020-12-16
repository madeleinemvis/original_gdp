import React, { useState, useEffect } from 'react';
import { Nav, NavItem, NavLink, Container } from 'reactstrap';
import {
    HashRouter as Router,
    Switch,
    Route,
    useRouteMatch,
    Redirect,
    NavLink as RRNavLink
} from "react-router-dom";

import Tweets from './SocialMedia/Tweets';
import Sources from "./WebArticles/Sources";
import SocialMedia from "./SocialMedia/SocialMedia";

// Source: https://bezkoder.com/react-hooks-crud-axios-api/
const Dashboard = props => {
    const uid = props.uid
    let { path, url } = useRouteMatch();
    if(props.uid === 'null'){
        console.log('redirecting')
        return <Redirect to={{ pathname: "/" }}/>
    }
    return (
        <React.Fragment>
            <Router basename={path}>
                <Container>
                    {/*TODO: active buttons*/}
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