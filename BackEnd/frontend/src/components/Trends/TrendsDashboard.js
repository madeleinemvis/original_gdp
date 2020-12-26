import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import EconGauge from "./EconGauge";
import EconBar from "./EconBar";
import HealthGauge from "./HealthGauge";
import HealthBar from "./HealthBar";
import PoliticsGauge from "./PoliticsGauge";
import PoliticsBar from "./PoliticsBar";

const TrendsDashboard = props => {
    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget">
                    <EconGauge uid={props.uid}/>
                </Col>
                <Col className="col-md widget">
                    <EconBar uid={props.uid}/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <HealthGauge uid={props.uid}/>
                </Col>
                <Col className="col-md widget">
                    <HealthBar uid={props.uid}/>
                </Col>
            </Row>
            <Row>
                <Col className="col-md widget">
                    <PoliticsGauge uid={props.uid}/>
                </Col>
                <Col className="col-md widget">
                    <PoliticsBar uid={props.uid}/>
                </Col>
            </Row>
        </Container>
    );
}

export default TrendsDashboard;