import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import TweetFreq from "../SocialMedia/TweetFreq";
import WordCloud from "./WordCloud";
import DocumentFreq from "./DocumentFreq";


const ArticlesDashboard = props => {
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
        </Container>
    );
}

export default ArticlesDashboard;