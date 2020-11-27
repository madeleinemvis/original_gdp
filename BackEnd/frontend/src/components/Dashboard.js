import React, { useState, useEffect } from 'react';
import { Nav, NavItem, NavLink, Container } from 'reactstrap';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    useRouteMatch,
    NavLink as RRNavLink
} from "react-router-dom";

import Tweets from './Tweets';
import WordCloud from "./WordCloud";

// Source: https://bezkoder.com/react-hooks-crud-axios-api/
const Dashboard = () => {

    let { path, url } = useRouteMatch();
   
    return (
        <React.Fragment>
            <Container>
                <h3>Results from Analysis</h3>
                <Router>
                    <Nav pills>
                        <NavItem>
                            <NavLink exact to={`${url}`} tag={RRNavLink} activeClassName="active">Info</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink exact to={`${url}/sources`} tag={RRNavLink} activeClassName="active">Sources</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink exact to={`${url}/tweets`} tag={RRNavLink} activeClassName="active">Tweets</NavLink>
                        </NavItem>
                    </Nav>

                    <Switch>
                        <Route exact path={path}>
                            <h3>Info</h3>
                        </Route>
                        <Route exact path={`${path}/sources`}>
                            <h1>tester</h1>
                            <WordCloud />
                        </Route>
                        <Route exact path={`${path}/tweets`}>
                            <Tweets />
                        </Route>
                    </Switch>  
                </Router>
            </Container>
        </React.Fragment>
    )
}

export default Dashboard;