import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import Tweets from "./Tweets";
import SentimentScatter from "./SentimentScatter";
import TweetFreq from "./TweetFreq";


const TweetsDashboard = props => {
    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget">
                    <Tweets uid={props.uid}/>
                </Col>
                <Col className="col-md widget">
                    <TweetFreq uid={props.uid}/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <SentimentScatter uid={props.uid}/>
                </Col>
            </Row>
        </Container>
    );
}

export default TweetsDashboard;