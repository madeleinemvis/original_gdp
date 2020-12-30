import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { 
    Container, Card,CardTitle, 
    CardSubtitle, CardBody,
    CardText
} from 'reactstrap';

import { Scrollbar } from "react-scrollbars-custom";

import Loading from "../Loading";

const Tweets = props => {
    
    const [tweets, setTweets] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    
    useEffect(() => {
        setTweets(props.tweets)
    }, [props.tweets]);

    
    
    return(
        <React.Fragment>
            {tweets.length === 0 ?
                <Loading/>
                :
                <Container>
                    <Row>
                        <Col>
                            <Loading/>
                        </Col>
                    :
                        <Col>
                            <Scrollbar style={{width: "100%", height: 400}}>
                                {tweets && tweets.map((tw, index) => (
                                    <Card key={index}>
                                        <CardBody>
                                            <CardTitle tag="h5">@{tw.screen_name}</CardTitle>
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
                    
                </Row>
            </Container>}
        </React.Fragment>
    );
}

export default Tweets;