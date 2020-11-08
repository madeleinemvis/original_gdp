import React, { Component } from 'react';
import { Container } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';

class Dashboard extends Component{

    constructor(props) {
        super(props);
        this.state = {         };
    }


    render(){

        return (
        
        
        <React.Fragment>
            <Container>
                <Button>Hello</Button> 
            </Container>
            
        </React.Fragment> 
        
        
        )
        
    }


}

export default Dashboard;