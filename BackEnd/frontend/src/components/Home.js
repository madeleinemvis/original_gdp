import React, {  useState } from 'react';

import { 
    Button,
    Col, 
    Row, 
    Container, 
    Jumbotron
} from 'react-bootstrap';

const Home = () => {
    // https://dev.to/fuchodeveloper/dynamic-form-fields-in-react-1h6c
    const [inputFields, setInputFields] = useState([
        { link: '' }
    ]);
    const [inputFiles, setInputFiles] = useState([
        { file: '' }
    ])
    
    const handleSubmit = e => {
        e.preventDefault();
        console.log("inputFields", inputFields);
    };

    const handleInputChange = (index, event) => {
        const values = [...inputFields];
        values[index].link = event.target.value;
        setInputFields(values);
    };

    const handleAddFields = () => {
        const values = [...inputFields];
        values.push({ link: ''});
        setInputFields(values);
      };
    
    const handleRemoveFields = index => {
      const values = [...inputFields];
      values.splice(index, 1);
      setInputFields(values);
    };


    return (
        <React.Fragment>
        <Container>
            <Row>
                <Col>
                    <Jumbotron>
                        <h1>Welcome</h1>
                        <p>Project description!</p>
                        <hr/>
                        <p>Add a link to be analysed. More than one link can be added.</p>
                        <p>
                            <Button variant="primary" size="lg">
                                Learn More
                            </Button>
                        </p>
                    </Jumbotron> 
                </Col>
                <Col>
                
                
                    <h3>Add your links to be analysed</h3>   

                    <form onSubmit={handleSubmit}>
                        {inputFields.map((inputField, index) => (
                            <div key={`${inputField}~${index}`}>
                                <div className="input-group">
                                    <input type="text" className="form-control" placeholder="URL" aria-label="link" aria-describedby="basic-addon2" onChange={event => handleInputChange(index, event)}/>
                                    <div className="input-group-append">
                                      <button className="btn btn-outline-secondary" type="button" onClick={() => handleAddFields()}>+</button>
                                      <button className="btn btn-outline-secondary" type="button" onClick={() => handleRemoveFields(index)}>-</button>
                                    </div>
                                </div>
                            </div>
                        ))}                            
                        <br></br>
                        <div className="submit-button">
                            <button
                              className="btn btn-primary mr-2"
                              type="submit"
                              onSubmit={handleSubmit}
                            >
                              Submit
                            </button>
                        </div>
                    </form>        
                    
                    <br/>
                
                
                </Col>
               
            </Row>
            
            <Row>
            <pre>
                {JSON.stringify(inputFields, null, 2)}
            </pre>
                    
            </Row> 
            <Row>            
                                
            </Row>       
        </Container>
    </React.Fragment> 
    )
  }
  
export default Home;
