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

export default TrendsDashboard;