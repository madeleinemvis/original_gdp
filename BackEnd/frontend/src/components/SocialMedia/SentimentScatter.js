import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Scatter from "./Scatter";
import Loading from "../Loading";
import Error from "../Error";
const SentimentScatter = props => {
    const[data, setData] = useState(JSON.parse(sessionStorage.getItem('sentScatterData')));
    const[isLoading, setIsLoading] = useState(true);
    const[isError, setIsError] = useState(false);


    useEffect(( ) => {
        const abortController = new AbortController()
        const signal = abortController.signal
        if(data === null){
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/tweets/sentiment_scatter', formdata, {signal: signal})
            .then(res => {
                const tweetsDf = res.data;
                setData(tweetsDf)
                sessionStorage.setItem('sentScatterData', JSON.stringify(tweetsDf))
                setIsLoading(false);
            })
            .catch(e => {
                setIsError(true);
                console.log(e)
            })
        }else{
            setIsLoading(false)
        }

        return function cleanup() {
            abortController.abort()
        }
    }, []);

    console.log("sentiment data: ", data)
    return(
        <React.Fragment>
            <Container>
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
                                <div className="svg-container">
                                    <Scatter data={data}/>
                                </div>
                            </Col>
                        }
                    </Row>
                }
            </Container>
        </React.Fragment>
    );
}
export default SentimentScatter;