import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar';

class App extends Component{

    constructor(props) {
        super(props);
        this.state = { 
            mode:'input'
        };
    }


    render(){
        return (
        
        
        <React.Fragment>
            
            <Navbar></Navbar>

            <div class="container">
                

                <div class="jumbotron">
                    <h1 class="display-4">Welcome!</h1>
                    <p class="lead">Project description!</p>
                    <hr class="my-4"/>
                    <p>Add a link to be analysed. More than one link can be added.</p>
                    <p class="lead">
                      <a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a>
                    </p>
                </div>
                
                <br/>
                <div class="row">
                    <div class="col-sm">
                        <form>
                            <div class="form-group">
                                <label for="link">Link:</label>
                                <input type="text" class="form-control" id="link" aria-describedby="linkHelp" placeholder="Enter email"/>
                                <small id="linkHelp" class="form-text text-muted">Link must be a URL.</small>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm">
                        <button type="button" class="btn btn-primary btn-lg btn-block">SEND</button>
                    </div>
                    <div class="col-sm">
                        <button type="button" class="btn btn-secondary btn-lg btn-block">ADD MORE</button>
                    </div>
                </div>
                
                
            </div>

        </React.Fragment> 
        
        
        )
        
    }


}

export default App;
ReactDOM.render(<App/>, document.getElementById('app'))