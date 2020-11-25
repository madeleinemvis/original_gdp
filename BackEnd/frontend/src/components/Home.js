import React, {  useState } from 'react';
import JSZip from 'jszip'
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
    const [pdfs, setPdfs] = useState([
        { pdfs: '' }
    ]);
    const formData = new FormData()
    
    const handleSubmit = e => {
        e.preventDefault();
        console.log(formData);
    };

    // Source: https://medium.com/@tchiayan/compressing-single-file-or-multiple-files-to-zip-format-on-client-side-6607a1eca662
    const upload = e => {
        e.preventDefault();
        
        
    }

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

    const handleInputChangePdf = (index, event) => {
        const values = [...pdfs];
        values[index].pdfs = event.target.value;
        setPdfs(values);
    };
    const handleAddFieldsPDF = () => {
        const values = [...pdfs];
        values.push({ pdfs: ''});
        setPdfs(values);
    };    
    const handleRemoveFieldsPDF = index => {
      const values = [...pdfs];
      values.splice(index, 1);
      setPdfs(values);
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
                    <hr/>
                    <form onSubmit={handleSubmit}>
                        {pdfs.map((pdf, index) => (
                            <div key={`${pdf}~${index}`}>
                                <div className="input-group">
                                    <input type="text" className="form-control" placeholder="PDF URL" aria-label="pdf" aria-describedby="basic-addon2" onChange={event => handleInputChangePdf(index, event)}/>
                                    <div className="input-group-append">
                                      <button className="btn btn-outline-secondary" type="button" onClick={() => handleAddFieldsPDF()}>+</button>
                                      <button className="btn btn-outline-secondary" type="button" onClick={() => handleRemoveFieldsPDF(index)}>-</button>
                                    </div>
                                </div>
                            </div>
                        ))}                            
                        <br></br>
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
                        <input type="file" id="files" onChange={upload} name="files" multiple/>
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

     
        </Container>
    </React.Fragment> 
    )
  }
  
export default Home;
