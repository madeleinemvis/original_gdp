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

    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets/sentiment_scatter', formdata)
        .then(res => {
            const tweetsDf = res.data;
            setData(tweetsDf)
            sessionStorage.setItem('sentScatterData', JSON.stringify(tweetsDf))
            console.log("$$$ DATA")
            console.log(tweetsDf)
            setIsLoading(false);
        })
        .catch(e => {
            setIsError(true);
            console.log(e)
        })
    }

    useEffect(( ) => {
        if(data === null){
            fetchData()
        }else{
            setIsLoading(false)
        }
    }, []);

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