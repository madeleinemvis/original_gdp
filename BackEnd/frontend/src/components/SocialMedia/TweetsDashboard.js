import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import Tweets from "./Tweets";
import SentimentScatter from "./SentimentScatter";
import TweetFreq from "./TweetFreq";


const TweetsDashboard = props => {
    const uid = props.uid
    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget widget-alert">
                    <TweetAlert/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <Tweets uid={uid}/>
                </Col>
                <Col className="col-md widget">
                    <TweetFreq uid={uid}/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <Row>
                        <Col className="col-md">
                            <h4>Retweet Count vs Favorite Count</h4>
                        </Col>
                    </Row>
                    <Row>
                        <Col className="col-md">
                            <p>The Tweets are colour-coded based on their sentiment that is predicted by a sentiment analysis model. The influence of a Tweet can be estimated by the number of interactions, by the number of Retweets and Favourites.</p>
                        </Col>
                    </Row>
                    <SentimentScatter uid={uid}/>
                </Col>
            </Row>
        </Container>
    );
}

const TweetAlert = () => {
    return(
        <Container>
            <Row>
                <Col>
                    <h4>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                             className="bi bi-info-circle" viewBox="0 0 16 16" style={{margin: "2px"}}>
                            <path fill-rule="evenodd"
                                  d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                            <path
                                d="M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z"/>
                            <circle cx="8" cy="4.5" r="1"/>
                        </svg>Important Twitter Information:</h4>
                </Col>
            </Row>
            <Row>
                <Col>
                    <p>Please note that all Tweets collected have all been <strong>posted within the previous 9 days</strong>.<br />
                    Therefore, please be aware that the data shown from the following visuals may be skewed due to lack of interaction by other users.</p>
                </Col>
            </Row>
        </Container>
    );
}

export default TweetsDashboard;