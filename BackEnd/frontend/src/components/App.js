import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar';
import Home from './Home';
import Dashboard from './Dashboard';

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
            
            <Navbar></Navbar>
            <br/>
            {view ? <Home action={this.handler}/> : <Dashboard/>}
            

        </React.Fragment> 
        
        
        )
        
    }


}

export default App;
ReactDOM.render(<App/>, document.getElementById('app'))