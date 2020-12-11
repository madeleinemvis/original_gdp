import React, {Fragment, useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import Home from './Home';
import Dashboard from './Dashboard';
import Suggestion from './Suggestion'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";
import '../style/App.css';
import {Navbar, Nav, Container} from "react-bootstrap";
import { v4 as uuidv4 } from 'uuid';

const App = () => {

    const [uid, setUid] = useState(uuidv4())


    return (
        <Fragment>
            <Router>
                <Container>
                    <nav className="navbar navbar-expand-sm">
                        <a className="navbar-brand" href="/">Propaganda analysis</a>
                        <div className="collapse navbar-collapse" id="navbarNav">
                            <ul className="navbar-nav">
                                <li className="nav-item">
                                    <a href="/" className="nav-link">Home</a>
                                </li>
                                <li className="nav-item">
                                  <a href="/about" className="nav-link">About</a>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </Container>
                <Container className="center-body">
                <Switch>
                    <Route exact path="/about">

                    </Route>
                    <Route path="/dashboard">
                        <Dashboard uid={uid} />
                    </Route>
                    <Route exact path="/">
                        <Home uid={uid} />
                    </Route>
                </Switch>
                </Container>
            </Router>
        </Fragment>
    )
}

export default App;
ReactDOM.render(<App/>, document.getElementById('app'))