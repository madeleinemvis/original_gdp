import React, {  useState } from 'react';
import { Redirect } from 'react-router';

import {
    Button,
    Col, 
    Row, 
    Container, 
    Jumbotron
} from 'react-bootstrap';

import http from '../http-common'
import '../style/App.css'
import Suggestion from './Suggestion';
import Input from "./Input";
import Loading from "./Loading";
import Error from "./Error";

const Home = props => {
    // https://dev.to/fuchodeveloper/dynamic-form-fields-in-react-1h6c

    //Local component state
    const [redirect, setRedirect] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [suggest, setSuggest] = useState(false)

    const { uid } = props
    const [claim, setClaim] = useState('')
    const [links, setLinks] = useState([{url:''}])
    const [pdfs, setPdfs] = useState([{url:''}])

    const [isError, setIsError] = useState(false);

    const formData = new FormData();


    // Suggested links
    const [suggestions, setSuggestions] = useState([])




    const handleSubmit = suggest => {
        setIsLoading(true)

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
            http.post('/documents/suggest', formData)
            .then(res => {
                setSuggestions(res.data)
                setIsLoading(false)
                setSuggest(suggest)
            })
            .catch(e => {
                setIsError(true)
                console.log(e)
            })
        }else{
            http.post('/documents/upload', formData)
                .then(res =>{
                    if(res.status === 201) {
                        setIsLoading(false)
                        setRedirect(true)
                    }
                })
                .catch(e => {
                    setIsError(true)
                    console.log(e)
                })
        }
    };

    // [{url: ''}] -> "{}"
    const formatLinks = input => {

        if(input[0].url === ''){
            return null
        }
        let out = "{";

        for (let i = 0; i < input.length; i++) {
            const e = input[i];

            const link = "'url" + i.toString() + "': '" + e.url + "'";
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
        const fs = e.target.files;

        for (const f of fs) {
            formData.append('files', f, f.name)
        }
    }

    if(redirect){
        return <Redirect to={{ pathname: "/dashboard" }}/>
    }


    return (
        <React.Fragment>
            {isError ?
                <Container>
                    <Row>
                        <Col>
                            <Error/>
                        </Col>
                    </Row>
                </Container>
                :
                <Container>
                    {!isLoading ?
                        <Row>
                            <Col>
                                <Jumbotron>
                                    <h1 className="jumbotron-h1">Welcome</h1>
                                    <p className="jumbotron-p">Our system is here to show you how a particular theme of
                                        propaganda has spread!</p>
                                    <hr/>
                                    <p className="jumbotron-p">On this page, you can add links and files that you wish to be analysed.
                                    These files will be used to generate a manifesto about the propaganda theme that you wish to investigate.
                                    Please read and understand what each component does before inputting, to allow the system to work optimally:</p>
                                    <br/>
                                    <ul>
                                        <li className="jumbotron-p">Claim:
                                            The phrase that will summarise your propaganda theme. Please keep the length of the claim minimal, such that the system can collect more documents related to the topic.
                                            Furthermore, the claim should also be relevant to the documents that you will be uploading. You can add more URLs with the '+' button and delete URLs with the '-' button.</li>
                                        <li className="jumbotron-p">Links:
                                            Should be URLs that link to web-pages or web-articles. Our system's quality increases with the number of documents uploaded, so please try to include
                                            as many as you can.</li>
                                        <li className="jumbotron-p">PDF Links: Should all be URLs that link to PDF pages.</li>
                                        <li className="jumbotron-p">File: Upload any PDF files that are related to the propaganda theme. All PDF files must be added simultaneously, but as separate files.</li>
                                    </ul>
                                    <br/>
                                    <p className="jumbotron-p">Suggesting URLs: If you are struggling to find documents to upload, you can select our 'Suggest URLs?' checkbox. Our system will then return a list of URLs for you to
                                    look through and choose from, to increase the collection of documents, and therefore increase the quality of the system.</p>
                                </Jumbotron>
                            </Col>
                            <span className="vertical-line"/>
                            <Col>
                                {suggest ?
                                    <Suggestion submit={handleSubmit} suggested={suggestions} addLinks={add_links}/>
                                    :
                                    <Input uid={uid} submit={handleSubmit} setFiles={set_files} setClaim={set_claim} setLinks={set_links} setPdfs={set_pdfs}/>
                                }
                            </Col>
                        </Row>
                    :
                       <Loading/>
                    }
                </Container>
            }
    </React.Fragment> 
    )
}
export default Home;
