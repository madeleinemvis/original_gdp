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
            <Row>
                <Container>
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
                        <pre>
                         {JSON.stringify(inputFields, null, 2)}
                        </pre>
                                                
                </Container>
                    
            </Row> 
            <Row>            
                

                
            </Row>       
        </Container>
    </React.Fragment> 
    )
  }
  

/*
className Home extends Component{
    // https://medium.com/@rkstrdee/dynamic-form-fields-using-react-with-hooks-b7d4d037042c    
    constructor(props) {
        super(props);
    }
    const [count, setCount] = useState(0);

    handleChangeInput(i, event) {
        const values = [...fields];
        const { name, value } = event.target;
        values[i][name] = value;
        setFields(values);
        console.log(fields);
    }

    handleAddInput() {
        const values = [...fields];
        values.push({
          link: '',
        });
        setFields(values);
    }

    handleRemoveInput(i) {
        const values = [...fields];
        console.log(values);
        values.splice(i, 1);
        setFields(values);
    }

    onSubmit = e => {
        e.preventDefault();
        console.log(e.target.value)
    }
    
    render(){
        return (        
        
        <React.Fragment>
            <Container>
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
                    
                <Row>
                    <Col>
                        <h3>Add your links to be analysed</h3>
                    </Col>
                    <Col>
                        <Button onClick={(e) => this.addLink(e)}>+</Button>
                    </Col>
                </Row>
                <Row>
                    <Form onSubmit={e => onSubmit(e)}>

                        {fields.map((field, index) => {
                            return(
                                <div key={`${field}-${index}`}>
                                    <FormGroup row>
                                    
                                        <Input
                                            type="text" 
                                            name="link"
                                            value={field.link} 
                                            ref={index} 
                                            placeholder="Your link"  
                                            onChange={e => handleChangeInput(index, e)} 
                                            />
                                    </FormGroup>
                                    <Button type="button" onClick={() => this.handleAddInput()}>
                                        <GrAdd />
                                    </Button>
                                    <Button type="button" onClick={() => this.handleAddInput()}>
                                        <GrAdd />
                                    </Button>
                                </div>
                                
                            )
                            })
                        }


                        <Button type="submit">Submit</Button>
                    </Form>
                </Row>      
            </Container>
        </React.Fragment> 
        )   
    }
}
*/
export default Home;
