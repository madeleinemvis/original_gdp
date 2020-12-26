import React from "react";
import {Row, Col, Container} from "react-bootstrap";
import EconGauge from "./EconGauge";


const TrendsDashboard = props => {
    return(
        <Container className="dashboard">
            <Row>
                <Col className="col-md widget">
                    <EconGauge uid={props.uid}/>
                </Col>
            </Row>
        </Container>
    );
}

export default TrendsDashboard;