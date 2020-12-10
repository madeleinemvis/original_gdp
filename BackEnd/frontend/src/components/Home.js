import React, {  useState, useEffect } from 'react';
import { Redirect } from 'react-router';


import { 
    Button,
    Col, 
    Row, 
    Container, 
    Jumbotron,
    Spinner,
    Form
} from 'react-bootstrap';
import http from '../http-common'
import Suggestion from './Suggestion';

const Home = props => {
    // https://dev.to/fuchodeveloper/dynamic-form-fields-in-react-1h6c

    //Local component state
    const [redirect, setRedirect] = useState(false)
    const [loading, setLoading] = useState(false)
    const [suggest, setSuggest] = useState(false)

    const { uid } = props
    const [claim, setClaim] = useState('')
    const [links, setLinks] = useState([{url:''}])
    const [pdfs, setPdfs] = useState([{url:''}])

    var formData = new FormData()


    // Suggested links
    const [suggestions, setSuggestions] = useState([])

    


    const handleSubmit = suggest => {
        setLoading(true)

        formData.delete('uid')
        formData.append('uid', uid)
        
        formData.delete('claim')
        formData.append('claim',claim)

        if(links[0].url !== ''){
            formData.delete('urls')
            let urls = formatLinks(links) 
            formData.append('urls', urls)
        }
        if(pdfs[0].url !== ''){
            formData.delete('pdfs')
            let pdf_links = formatLinks(pdfs)
            formData.append('pdfs', pdf_links)
        }

        if(suggest){
            formData.append('want_suggestions', suggest)
            http.post('/documents/suggest', formData)
            .then(res => {
                setSuggestions(res.data)
                setLoading(false)
                setSuggest(suggest)
            })
            .catch(e => {
                console.log(e)
            })            
        }else{
            http.post('/documents/upload', formData)
                .then(res =>{
                    if(res.status === 201){   
                        setLoading(false)
                        setRedirect(true)
                    }
                })
                .catch(e => {
                    console.log(e)
                })
        }
    };

    // [{url: ''}] -> "{}"
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
    // functions that will be passed to child components
    function set_claim(claim){
        setClaim(claim)
    }
    function add_links(urls){
        let values = [...links]
        for(const url of urls){
            values.push(url)

        }
        setLinks(values)
    }
    function set_links(links){
        setLinks(links)
    }
    function set_pdfs(pdfs){
        setPdfs(pdfs)
    }

    // Source: https://medium.com/@tchiayan/compressing-single-file-or-multiple-files-to-zip-format-on-client-side-6607a1eca662
    function set_files(e){
        formData.delete('files')
        var fs = e.target.files

        for (const f of fs) {
            formData.append('files', f, f.name)            
        }
    }

    if(redirect){
        return <Redirect to={{ pathname: "/dashboard" }}/>
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
                <Col>                    
                    {
                        suggest ? null : <Input uid={uid} submit={handleSubmit} setFiles={set_files} setClaim={set_claim} setLinks={set_links} setPdfs={set_pdfs}/>}
                    {
                        loading ? <Loading/> : null
                    }
                    {
                        suggest ? <Suggestion submit={handleSubmit} suggested={suggestions} addLinks={add_links}/> : null
                    }
                </Col>
            </Row>
        </Container>
    </React.Fragment> 
    )
}

const Loading = () =>{
    return <Spinner animation="border" role="status">
                <span className="sr-only">Loading...</span>
            </Spinner> 
}

const Input = props => {
    const {uid } = props
    const [claim, setClaim] = useState('')
    const [inputFields, setInputFields] = useState([{ url: '' }]);
    const [pdfs, setPdfs] = useState([{ url: '' }]);

    const[suggest, setSuggest] = useState(false)
    // functions from parent 

    function submitParent(suggest){
        props.submit(suggest)
    }

    function set_claim(claim){
        props.setClaim(claim)
    }

    const set_files = e => {
        props.setFiles(e)
    }

    const set_links = (links) => {
        props.setLinks(links)
    }

    const set_pdfs = (pdfs) => {
        props.setPdfs(pdfs)
    }

    //Functions for manipulating link fields
    const handleInputChange = (index, event) => {
        const values = [...inputFields];
        values[index].url = event.target.value;
        setInputFields(values);
        set_links(values)

    };
    const handleAddFields = () => {
        const values = [...inputFields];
        values.push({ url: ''});
        setInputFields(values);
        set_links(values)
    };    
    const handleRemoveFields = index => {
      const values = [...inputFields];
      values.splice(index, 1);
      setInputFields(values);
      set_links(values)
    };
    //Functions for manipulating pdf link fields
    const handleInputChangePdf = (index, event) => {
        const values = [...pdfs];
        values[index].url = event.target.value;
        setPdfs(values);
        set_pdfs(values)
    };
    const handleAddFieldsPDF = () => {
        const values = [...pdfs];
        values.push({ url: ''});
        setPdfs(values);
        set_pdfs(values)
    };    
    const handleRemoveFieldsPDF = index => {
      const values = [...pdfs];
      values.splice(index, 1);
      setPdfs(values);
      set_pdfs(values)
    };

    const submit = e => {
        e.preventDefault()
        submitParent(suggest)
    }

    return (
        
        <div>
                             
            <h3>Add your links to be analysed</h3>   
            <hr/>
            <form onSubmit={submit}>
                <h5>Claim:</h5>
                <div className="input-group">
                    <input type="text" className="form-control" placeholder="Claim" aria-label="claim" aria-describedby="basic-addon2" onChange={e => set_claim(e.target.value)} />
                </div>
                <br/>
                <h5>Links:</h5>
                {inputFields.map((inputField, index) => (
                    <div key={`${inputField}~${index}`}>
                        <div className="input-group">
                            <input type="text" className="form-control" placeholder="URL" aria-label="link" aria-describedby="basic-addon2" onChange={event => handleInputChange(index, event)}/>
                            <div className="input-group-append">
                              <button className="btn btn-outline-secondary" type="button" onClick={() => handleAddFields()}>+</button>
                              { (inputFields.length === 1) ?
                                <button className="btn btn-outline-secondary" disabled type="button" onClick={() => handleRemoveFields(index)}>-</button> :
                                <button className="btn btn-outline-secondary" type="button" onClick={() => handleRemoveFields(index)}>-</button>
                              }
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
                            { (pdfs.length === 1) ?
                                <button className="btn btn-outline-secondary" disabled type="button" onClick={() => handleRemoveFieldsPDF(index)}>-</button>:
                                <button className="btn btn-outline-secondary" type="button" onClick={() => handleRemoveFieldsPDF(index)}>-</button>
                            }
                            </div>
                        </div>
                    </div>
                ))} 
                         
                <br></br>
                <input type="file" id="files" onChange={set_files} name="files" multiple/>
                
                <br></br>
                
                <Form.Check 
                    type="checkbox"
                    id={`suggest`}
                    label={`Suggest urls?`}
                    value={suggest}
                    onChange={() => setSuggest(!suggest)}
                />
                <hr/>
                
                <div className="submit-button">
                    <button
                      className="btn btn-primary mr-2"
                      type="submit"
                    >
                      Submit
                    </button>
                </div>
            </form>        
            
            <br/>
        </div>
    )
}

export default Home;
