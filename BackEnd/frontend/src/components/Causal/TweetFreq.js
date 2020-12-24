import React, {useEffect, useState} from 'react'
import {Container, Spinner, Row, Col} from 'react-bootstrap';

import http from '../../http-common'
import Loading from "../Loading";
const TweetFreq = props => {
    const[frequency, setFrequency] = useState(0);
    const[isLoading, setIsLoading] = useState(true);
    const[isEmpty, setIsEmpty] = useState(false);

    useEffect(( ) => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/causal/freq', formdata)
                .then(res => {
                    setFrequency(res.data);
                    console.log("frequency:", frequency)
                    setIsLoading(false);
                })
                .catch(e => {
                    console.log(e)
                })

        }

        fetchData();
    }, []);

    return <React.Fragment>
                {isLoading ?
                    <Loading/>
                :
                    <Container>
                        <Row>
                            <Col> <h4>Number of Tweets Collected</h4></Col>
                        </Row>
                        <Row>
                            <Col><h1>{frequency}</h1></Col>
                        </Row>
                    </Container>
                }
    </React.Fragment>;
}

export default TweetFreq;