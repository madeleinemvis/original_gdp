import React, {useEffect, useState} from 'react'
import {Container, Row, Col} from 'react-bootstrap';
import http from '../../http-common'

import Loading from "../Loading";
import Error from "../Error";
const TweetFreq = props => {
    const[frequency, setFrequency] = useState(JSON.parse(sessionStorage.getItem('tweetFreq')))
    const[isLoading, setIsLoading] = useState(true);
    const[isError, setIsError] = useState(false);

    useEffect(( ) => {
        if(frequency === null){
            fetchData();  
        }else{
            setIsLoading(false)
        }
    }, []);

    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets/freq', formdata)
            .then(res => {
                setFrequency(res.data);
                sessionStorage.setItem('tweetFreq', JSON.stringify(res.data))
                setIsLoading(false);
            })
            .catch(e => {
                setIsError(true);
                console.log(e);
            })

    }

    return <React.Fragment>
            <Container>
                <Row>
                    <Col>
                        <h4>Number of Tweets Collected</h4>
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
                                <h1>{frequency}</h1>
                            </Col>
                        }
                    </Row>
                }
            </Container>
    </React.Fragment>;
}

export default TweetFreq;