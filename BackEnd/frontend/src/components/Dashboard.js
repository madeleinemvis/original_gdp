import React, { useState, useEffect } from 'react';
import { Nav, NavItem, NavLink, Container } from 'reactstrap';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    useRouteMatch,
    Redirect,
    NavLink as RRNavLink
} from "react-router-dom";

import Tweets from './Tweets';
import Sources from "./Sources";

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
            <Container>
                <Router>
                    {/*TODO: active buttons*/}
                    <nav style="pills">
                        <ul className="navbar-nav">
                            <li className="nav-item">
                                <a href={`${url}`}>Web Articles</a>
                            </li>
                            <li>
                                <a href={`${url}/sources`}>Sources</a>
                            </li>
                        </ul>
                        {/*<NavItem>
                            <NavLink exact to={`${url}`} tag={RRNavLink} activeClassName="active">Info</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink exact to={`${url}/sources`} tag={RRNavLink} activeClassName="active">Sources</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink exact to={`${url}/tweets`} tag={RRNavLink} activeClassName="active">Tweets</NavLink>
                        </NavItem>*/}
                    </nav>

                    <Switch>
                        {/*<Route exact path={path}>
                            <h3>Info</h3>
                        </Route>*/}
                        <Route exact path={`${path}/sources`}>
                            <Sources uid={uid}/>
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