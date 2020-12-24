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

const Tweets = props => {
    
    const [tweets, setTweets] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    
    useEffect(() => {
        retrieveTweets();
    }, []);

    const retrieveTweets = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/causal', formdata)

            .then(res => {
                setTweets(res.data)
                console.log("Tweets:", tweets)
                setIsLoading(false);
            })
            .catch(e => {
                console.log(e)
            })
    }
    
    return(
        <React.Fragment>
            {isLoading ?
                <Loading/>
                :
                <Container>
                    <Row>
                        <Col>
                            <h3>All Tweets Crawled:</h3>
                        </Col>
                    </Row>
                    <Row>
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
                                            {(tw.user_location === "") ?
                                                <CardSubtitle tag="h6" className="mb-2 text-muted">Tweet
                                                    Location: {tw.user_location}</CardSubtitle> : null
                                            }
                                            <CardText> {tw.text}</CardText>
                                        </CardBody>
                                    </Card>
                                ))}
                            </Scrollbar>
                        </Col>
                    </Row>
                </Container>
            }
        </React.Fragment>
    );
}

export default Tweets;