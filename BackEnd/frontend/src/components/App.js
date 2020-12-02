import React, {Fragment, useState } from 'react';
import ReactDOM from 'react-dom';
import Home from './Home';
import Dashboard from './Dashboard';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

const App = () => {
    const[uid, setUid] = useState('null')

    function setUID(id){
        setUid(id)
    }

    return (
        <Fragment>
            <Router>
                <nav className="navbar navbar-expand-sm sticky-top navbar-dark bg-dark">
                    <div className="container">
                        <a className="navbar-brand" href="/">Propaganda analysis</a>
                        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"/>
                        </button>
                        <div className="collapse navbar-collapse" id="navbarNav">
                            <ul className="navbar-nav">
                                <li className="nav-item">
                                    <Link to="/" className="nav-link">Home</Link>
                                </li>
                                <li className="nav-item">
                                  <Link to="/about" className="nav-link">About</Link>
                                </li> 
                                {/*<li className="nav-item">
                                  <Link to="/dashboard" className="nav-link">Dashboard</Link>
                                </li>       */}               
                            </ul>
                        </div>
                    </div>
                </nav>
                <br/>
                <Switch>
                    <Route path="/about">

                    </Route>
                    <Route path="/dashboard">
                        <Dashboard uid={uid} />
                    </Route>
                    <Route exact path="/">
                        <Home uid={setUID}/>
                    </Route>
                </Switch>  
            </Router>
        </Fragment>
    )
}

export default App;
ReactDOM.render(<App/>, document.getElementById('app'))