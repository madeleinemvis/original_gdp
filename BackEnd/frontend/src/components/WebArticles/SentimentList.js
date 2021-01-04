import React, {useEffect, useState} from 'react'
import {Row, Col} from 'react-bootstrap';
import { 
    Container, Card,CardTitle, 
    CardSubtitle, CardBody,
    CardText
} from 'reactstrap';

import { Scrollbar } from "react-scrollbars-custom";
import http from '../../http-common'
import Loading from "../Loading";
import Error from "../Error";

const SentimentList = props => {
    const[data, setData] = useState(JSON.parse(sessionStorage.getItem('sentiment')));
    const[isEmpty, setIsEmpty] = useState(true);
    const[isLoading, setIsLoading] = useState(true);

    const[isError, setIsError] = useState(false);


    useEffect(( ) => {
<<<<<<< HEAD
        console.log(data);
        if(data === null){ 
=======
        console.log("Made effect");
        console.log(data);
        if(data === null){
            console.log("Is NULL");
>>>>>>> a792090f10f8a4b43107ff7ffca600bfc55ed773
            fetchData();
        }else{
            setIsLoading(false)
        }
        
    }, []);


    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
<<<<<<< HEAD
=======
        console.log('Made fetch');
>>>>>>> a792090f10f8a4b43107ff7ffca600bfc55ed773
        http.post('/documents/document_list', formdata)
            .then(res => {
                setData(res.data)
                console.log(res.data);
                sessionStorage.setItem('sentiment', JSON.stringify(res.data))
                if(res.data.length !== 0){
                    setIsEmpty(false);
                }
                setIsLoading(false)
            })
            .catch(e => {
                setIsError(true)
                console.log(e)
            })
    }

    return (
        <React.Fragment>
            <Container>
                 <Row>
                    <Col>
                        <h4>Document Sentiments:</h4>
                    </Col>
                </Row>
                {isError ?
                    <Row>
                        <Col>
                            <Error/>
                        </Col>
                    </Row>
                :
                    <Row>
                    {isLoading ?
                        <Col>
                            <Loading/>
                        </Col>
                    :
                        <Col>
                        {isEmpty ?
                            <p>No Documents Found</p>
                            :
                            <Scrollbar style={{width: "100%", height: 400}}>
                                {data && data.map((doc, index) => (
                                    <Card key={index}>
                                        <CardBody>
                                            <CardTitle tag="h5">{doc.title}</CardTitle>
                                            <CardSubtitle tag="h6"
                                                          className="mb-2 text-muted">Sentiment: {doc.sentiment}</CardSubtitle>
                                            <CardSubtitle tag="h6" className="mb-2 text-muted">Stance: {doc.stance}</CardSubtitle>
                                            <CardSubtitle tag="h6" className="mb-2 text-muted">URL: {doc.url}</CardSubtitle>
                                        </CardBody>
                                    </Card>
                                ))}
                            </Scrollbar>
                        }
                        </Col>
                    
                    }</Row>
                }

            </Container>
        </React.Fragment>
    );
}

export default SentimentList;