import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { 
    Container, Card,CardTitle, 
    CardSubtitle, CardBody,
    CardText, CardColumns
} from 'reactstrap';

import { Scrollbar } from "react-scrollbars-custom";

import DB from '../services/db.service';
import http from '../http-common';

const Tweets = () => {
    
    const [tweets, setTweets] = useState([]);
    
    useEffect(() => {
        retrieveTweets();
    }, []);

    const retrieveTweets = () => {
        http.get('/tweets')
            .then( res => {
                console.log('api')
                setTweets(res.data)
                console.log(res.data)
            })
            .catch(e => {
                console.log(e)
            })
    }
    const style = {
        height: '250',
        width: '250',
    }

    
    return(
        <React.Fragment>
            
                <Row>
                    <Col>
                        <h5>Sentiment Analysis</h5>
                        
                            <Scrollbar style={{ width: "100%",  height: 400 }}>
                                {tweets && tweets.map( (tw, index) => (
                                    <Card key={index}>    
                                        <CardBody>
                                            <CardTitle tag="h5">Tweet #{index}</CardTitle>
                                            <CardSubtitle tag="h6" className="mb-2 text-muted">Sentiment: { tw.sentiment }</CardSubtitle>
                                            <CardSubtitle tag="h6" className="mb-2 text-muted">Favorite Count: { tw.favorite_count } Retweet Count: { tw.retweet_count }</CardSubtitle>
                                            <CardSubtitle tag="h6" className="mb-2 text-muted">Tweet Location: { tw.user_location }</CardSubtitle>
                                            
                                            <CardText> {  tw.text  }</CardText>                      
                                        </CardBody>
                                    </Card>                    
                                ))}</Scrollbar>
                            
                                         
                    </Col>
                    <Col>
                    
                    </Col>
                    
                </Row>
        </React.Fragment>
    )
}

export default Tweets;