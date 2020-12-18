import React from "react";
import Container from "react-bootstrap";
import Row from "react-bootstrap";
import Col from "react-bootstrap";
import Tweets from "./Tweets";
import SentimentScatter from "./SentimentScatter";
import TweetFreq from "./TweetFreq";


const GridDashboard = (props) => {

    return(
        <React.Fragment>
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
                        <TweetFreq uid={uid.props}/>
                    </Col>
                </Row>
            </Container>
        </React.Fragment>
    );
}

export default GridDashboard;