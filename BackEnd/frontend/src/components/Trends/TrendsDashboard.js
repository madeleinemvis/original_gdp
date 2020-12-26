import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import EconGauge from "./EconGauge";
import EconBar from "./EconBar";

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
        </Container>
    );
}

export default TrendsDashboard;