import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar';
import Home from './Home';
import Dashboard from './Dashboard';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

class App extends Component{

    constructor(props) {
        super(props);

        this.handler = this.handler.bind(this);

        this.state = { 
            mode: 'home'
        };
    }


    handler(){
        this.setState({
            mode: 'dashboard'
        })
    }


    render(){

        const view = this.state.mode === 'home';

        return (
        
        
        <React.Fragment>
            
            
            
            <Router>
                <nav className="navbar navbar-expand-sm sticky-top navbar-dark bg-dark">
                    <div className="container">
                        <a className="navbar-brand" href="#">Propaganda Analysis</a>
                        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                        </button>
                        <div className="collapse navbar-collapse" id="navbarNav">
                            <ul className="navbar-nav">
                                <li className="nav-item active">
                                    <Link to="/">Home</Link>
                                </li>
                                <li className="nav-item">
                                  <Link to="/about">About</Link>
                                </li> 
                                <li className="nav-item">
                                  <Link to="/dashboard" disabled>Dashboard</Link>
                                </li>                      
                            </ul>
                        </div>
                    </div>
                </nav>
                <br/>
                <Switch>
                    <Route path="/about">

                    </Route>
                    <Route path="/dashboard">
                        <Dashboard />
                    </Route>
                    <Route exact path="/">
                        <Home action={this.handler}/>
                    </Route>
                </Switch>  
            </Router>
            

            
            
            

        </React.Fragment> 
        
        
        )
        
    }


}

export default App;
ReactDOM.render(<App/>, document.getElementById('app'))