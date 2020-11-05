import React, { Component } from 'react';

class Navbar extends Component{
    render(){
        return (
        
        
        <React.Fragment>
            <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
                
                <a class="navbar-brand" href="#">Navbar</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                      <li class="nav-item active">
                        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="#">About</a>
                      </li>                      
                    </ul>
                </div>
            
            </nav>

        </React.Fragment> 
        
        
        )
        
    }


}

export default Navbar;