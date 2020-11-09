import React, { Component } from 'react';
import { Nav, NavItem, NavLink, Container } from 'reactstrap';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    useRouteMatch
} from "react-router-dom";

const Dashboard = () => {

    let { path, url } = useRouteMatch();

    return (
        <React.Fragment>
            <Container>
                <Router>
                    <Nav pills>
                        <NavItem>
                            <NavLink to="/">Info</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink to={`/sources`}><a>Sources</a></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href="#">Another Link</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink disabled href="#">Disabled Link</NavLink>
                        </NavItem>
                    </Nav>

                    <Switch>
                        <Route exact path={path}>
                            <h1>INFO</h1>
                        </Route>
                        <Route path="/sources">
                            <h1>INFO</h1>
                        </Route>
                    </Switch>  
                </Router>
            </Container>
        </React.Fragment>
    )
}

export default Dashboard;