import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import WordCloud from "./WordCloud";
import DocumentFreq from "./DocumentFreq";
import SentimentList from "./SentimentList";
import WebsiteGraph from "./WebsiteGraph";


const ArticlesDashboard = props => {
    console.log("uid articles:", props.uid);
    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget">
                    <DocumentFreq uid={props.uid}/>
                </Col>
                <Col className="col-md widget">
                    <WordCloud uid={props.uid} />
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <SentimentList uid={props.uid} />
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <WebsiteGraph uid={props.uid} />
                </Col>
            </Row>
        </Container>
    );
}

export default ArticlesDashboard;