import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Link
} from "react-router-dom";

class Navbar extends Component{
    render(){
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
          </Router>
        </React.Fragment> 
        
        
        )
        
    }


}

export default Navbar;