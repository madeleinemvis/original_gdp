import React, {  useState } from 'react';
import {
    Form
} from 'react-bootstrap';

const Input = props => {
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
                    <input type="text" className="form-control" aria-label="claim" placeholder="Claim" aria-describedby="basic-addon2" onChange={e => set_claim(e.target.value)} required/>
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

export default Input