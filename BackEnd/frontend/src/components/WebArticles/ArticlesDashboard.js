import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import TweetFreq from "../SocialMedia/TweetFreq";
import WordCloud from "./WordCloud";
import DocumentFreq from "./DocumentFreq";
import SentimentPie from "../SocialMedia/SentimentPie";


const ArticlesDashboard = props => {
    console.log("uid articles:", props.uid);
    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget">
                    <TweetFreq uid={props.uid}/>
                </Col>
                <Col className="col-md widget">
                    <DocumentFreq uid={props.uid}/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <WordCloud uid={props.uid} />
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <Row>
                        <Col className="col-md">
                            <h4>Articles Pie Chart</h4>
                        </Col>
                    </Row>
                    <Row>
                        <Col className="col-md">
                            <p>The following pie chart shows the distribution of detected stance for the crawled documents.</p>
                        </Col>
                    </Row>
                    <SentimentPie uid={props.uid}/>
                </Col>
            </Row>
        </Container>
    );
}

export default ArticlesDashboard;