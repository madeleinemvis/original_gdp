import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import Tweets from "./Tweets";
import SentimentScatter from "./SentimentScatter";
import TweetFreq from "./TweetFreq";


const GridDashboard = props => {
    console.log("uid is:", props.uid)
    return(
        <Container>
            <Row>
                <Col className="col-md-auto">
                    <Tweets uid={props.uid}/>
                </Col>
                <Col className="col-md-8">
                    <SentimentScatter uid={props.uid}/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md-auto">
                    <TweetFreq uid={props.uid}/>
                </Col>
            </Row>
        </Container>
    );
}

export default GridDashboard;