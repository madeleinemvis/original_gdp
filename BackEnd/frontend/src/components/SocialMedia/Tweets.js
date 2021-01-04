import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { 
    Container, Card,CardTitle, 
    CardSubtitle, CardBody,
    CardText
} from 'reactstrap';

import { Scrollbar } from "react-scrollbars-custom";
import http from '../../http-common'
import Loading from "../Loading";
import Error from "../Error";

const Tweets = props => {
    
    const [tweets, setTweets] = useState(JSON.parse(sessionStorage.getItem('tweets')));
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);
    const[isEmpty, setIsEmpty] = useState(true);
    const [errorCode, setErrorCode] = useState(201);

    useEffect(() => {
        if(tweets === null){
            setIsEmpty(true)
            retrieveTweets();
        }
        else{
            setIsLoading(false)
            setIsEmpty(false)
        }
        
    }, []);

    const retrieveTweets = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets', formdata)
            .then(res => {
                setTweets(res.data)
                sessionStorage.setItem('tweets', JSON.stringify(res.data))
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

    
    
    return(
        <React.Fragment>
            <Container>
                 <Row>
                    <Col>
                        <h4>All Tweets Collected: (Sorted by Impact)</h4>
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
                        }
                        </Col>
                    
                    }</Row>
                }

            </Container>
        </React.Fragment>
    );
}

export default Tweets;