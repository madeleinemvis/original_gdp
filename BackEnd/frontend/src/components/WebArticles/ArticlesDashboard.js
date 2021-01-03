import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import TweetFreq from "../SocialMedia/TweetFreq";
import WordCloud from "./WordCloud";
import DocumentFreq from "./DocumentFreq";


const ArticlesDashboard = props => {
    console.log("uid articles:", props.uid);

    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget">
                    <TweetFreq tweetsFreq={props.tweetsFreq}/>
                </Col>
                <Col className="col-md widget">
                    <DocumentFreq docFreq={props.docFreq}/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <WordCloud wordCloud={props.wordCloud} />
                </Col>
            </Row>
        </Container>
    );
}

export default ArticlesDashboard;