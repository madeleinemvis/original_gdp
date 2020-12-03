import React, {  useState, useEffect } from 'react';
import { Redirect } from 'react-router';

import { v4 as uuidv4 } from 'uuid';
import { 
    Button,
    Col, 
    Row, 
    Container, 
    Jumbotron,
    Spinner
} from 'react-bootstrap';
import http from '../http-common'
const Home = props => {
    // https://dev.to/fuchodeveloper/dynamic-form-fields-in-react-1h6c

    const [redirect, setRedirect] = useState(false)
    const [loading, setLoading] = useState(false)

    var formData = new FormData()
    const [claim, setClaim] = useState("")

    const [inputFields, setInputFields] = useState([
        { url: '' }
    ]);
    const [pdfs, setPdfs] = useState([
        { url: '' }
    ]);
    function setUid(id){
        props.uid(id)
    }


    const handleSubmit = e => {
        e.preventDefault();
        setLoading(true)
        //Deleteing existing parts
        var uid = uuidv4();
        formData.delete('uid')
        formData.delete('claim')
        formData.delete('urls')
        formData.delete('pdfs')

        //Add uid
        formData.append('uid',uid)

        //Adding claim   
        formData.append('claim', claim)

        //urls and pdf urls 
        var urls = formatLinks(inputFields)  
        var pdfURL = formatLinks(pdfs)
        
        if(urls !== null){
            formData.append('urls', urls)
        }
        if(pdfURL !== null){
            formData.append('pdfs', pdfURL)
        }
        
        
        http.post('/documents', formData)
        .then(res =>{
            if(res.status === 201){   
                setUid(res.data)             
                setLoading(false)
                setRedirect(true)
                console.log(res.data)
            }
            
        })
        .catch(e => {
            console.log(e)
        })
    };
    const formatLinks = input => {

        if(input[0].url === ''){
            return null
        }
        var out = "{"        

        for (let i = 0; i < input.length; i++) {
            const e = input[i];

            var link =  "'url" + i.toString() + "': '" + e.url + "'"
            if(i !== (input.length - 1)){
                out += link +','
            }else{
                out += link 
            }
            
        }
        out += "}"
        return out
    }

    // Source: https://medium.com/@tchiayan/compressing-single-file-or-multiple-files-to-zip-format-on-client-side-6607a1eca662
    const upload = e => {
        e.preventDefault();
        formData.delete('files')

        var fs = e.target.files

        for (const f of fs) {
            //console.log(f)
            formData.append('files', f, f.name)
        }
    }

    const handleInputChange = (index, event) => {
        const values = [...inputFields];
        values[index].url = event.target.value;
        setInputFields(values);
    };

    const handleAddFields = () => {
        const values = [...inputFields];
        values.push({ url: ''});
        setInputFields(values);
      };
    
    const handleRemoveFields = index => {
      const values = [...inputFields];
      values.splice(index, 1);
      setInputFields(values);
    };

    const handleInputChangePdf = (index, event) => {
        const values = [...pdfs];
        values[index].url = event.target.value;
        setPdfs(values);
    };
    const handleAddFieldsPDF = () => {
        const values = [...pdfs];
        values.push({ url: ''});
        setPdfs(values);
    };    
    const handleRemoveFieldsPDF = index => {
      const values = [...pdfs];
      values.splice(index, 1);
      setPdfs(values);
    };

    if(redirect){
        return <Dash/>
    }
 
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
                {loading ? <Loading/>:

                <Col>
                    <h3>Add your links to be analysed</h3>   
                    <hr/>
                    <form onSubmit={handleSubmit}>
                        <h5>Claim:</h5>
                        <div className="input-group">
                            <input type="text" className="form-control" placeholder="Claim" aria-label="claim" aria-describedby="basic-addon2" onChange={e => setClaim(e.target.value)} />
                        </div>
                        <br/>
                        <h5>Links:</h5>
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
                        <br/>
                        <h5>PDF Links:</h5>
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

                        <input type="file" id="files" onChange={upload} name="files" multiple/>
                        
                        <hr/>
                        
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
                }
               
            </Row>
        </Container>
    </React.Fragment> 
    )
}

const Dash = () =>{
    return <Redirect to={{ pathname: "/dashboard" }}/>
}

const Loading = () =>{
    return <Spinner animation="border" role="status">
    <span className="sr-only">Loading...</span>
</Spinner> 
}
export default Home;
