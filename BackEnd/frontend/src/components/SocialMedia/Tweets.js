import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { 
    Container, Card,CardTitle, 
    CardSubtitle, CardBody,
    CardText
} from 'reactstrap';

import { Scrollbar } from "react-scrollbars-custom";

import http from '../../http-common';
import Loading from "../Loading";
import Error from "../Error";

const Tweets = props => {
    
    const [tweets, setTweets] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);
    const [errorCode, setErrorCode] = useState(201);

    useEffect(() => {
        retrieveTweets();
    }, []);

    const retrieveTweets = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets', formdata)
            .then(res => {
                let code = res.status;
                if(code !== 201){
                    setIsError(true)
                    setErrorCode(code)
                }
                setTweets(res.data)
                console.log("Tweets:", tweets)
                setIsLoading(false)
            })
            .catch(e => {
                console.log(e)
            })
    }
    
    return(
        <React.Fragment>
            <Container>
                <Row>
                    <Col>
                         <h4>All Tweets Crawled:</h4>
                    </Col>
                </Row>
                <Row>
                    {isLoading ?
                        <Col>
                            <Loading/>
                        </Col>
                    :
                        {isError ?
                        <Col>
                            <Scrollbar style={{width: "100%", height: 400}}>
                                {tweets && tweets.map((tw, index) => (
                                    <Card key={index}>
                                        <CardBody>
                                            <CardTitle tag="h5">Tweet #{index}</CardTitle>
                                            <CardSubtitle tag="h6"
                                                          className="mb-2 text-muted">Sentiment: {tw.sentiment}</CardSubtitle>
                                            <CardSubtitle tag="h6" className="mb-2 text-muted">Favorite
                                                Count: {tw.favorite_count}</CardSubtitle>
                                            <CardSubtitle tag="h6" className="mb-2 text-muted">Retweet
                                                Count: {tw.retweet_count}</CardSubtitle>
                                            {(tw.user_location !== "") ?
                                                <CardSubtitle tag="h6" className="mb-2 text-muted">Tweet
                                                    Location: {tw.user_location}</CardSubtitle> : null
                                            }
                                            <CardText> {tw.text}</CardText>
                                        </CardBody>
                                    </Card>
                                ))}
                            </Scrollbar>
                        </Col>
                                :
                        <Error code={errorCode}/>

                    }

                    }
                </Row>
            </Container>
        </React.Fragment>
    );
}

export default Tweets;