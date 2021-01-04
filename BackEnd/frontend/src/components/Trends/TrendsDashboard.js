import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import EconGauge from "./EconGauge";
import EconBar from "./EconBar";
import HealthGauge from "./HealthGauge";
import HealthBar from "./HealthBar";
import PoliticsGauge from "./PoliticsGauge";
import PoliticsBar from "./PoliticsBar";
import TrendMap from "./TrendMap";

const TrendsDashboard = props => {
    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget">
                    <TrendMap uid={props.uid}/>
                    <h6>Map shows the google search rate of the manifesto keywords by country</h6>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget widget-alert">
                    <TrendAlert/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <EconGauge uid={props.uid}/>
                    <h6>Plot illustrates how many economic causal tests passed</h6>
                </Col>
                <Col className="col-md widget">
                    <EconBar uid={props.uid}/>
                    <h6>Breakdown of causal estimate and causal refutation values</h6>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <HealthGauge uid={props.uid}/>
                    <h6>Plot illustrates how many health causal tests passed</h6>
                </Col>
                <Col className="col-md widget">
                    <HealthBar uid={props.uid}/>
                    <h6>Breakdown of causal estimate and causal refutation values</h6>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <PoliticsGauge uid={props.uid}/>
                    <h6>Plot illustrates how many politics causal tests passed</h6>
                </Col>
                <Col className="col-md widget">
                    <PoliticsBar uid={props.uid}/>
                    <h6>Breakdown of causal estimate and causal refutation values</h6>
                </Col>
            </Row>
        </Container>
    );
}

const TrendAlert = () => {
    return(
        <Container>
            <Row>
                <Col>
                    <h4>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                             className="bi bi-info-circle" viewBox="0 0 16 16" style={{margin: "2px"}}>
                            <path fillRule="evenodd"
                                  d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                            <path
                                d="M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z"/>
                            <circle cx="8" cy="4.5" r="1"/>
                        </svg>Important Causality Test Information:</h4>
                </Col>
            </Row>
            <Row>
                <Col>
                    <p>Please note that the causal tests displayed here are only representative of the United Kingdom.</p>
                </Col>
            </Row>
        </Container>
    );
}


export default TrendsDashboard;