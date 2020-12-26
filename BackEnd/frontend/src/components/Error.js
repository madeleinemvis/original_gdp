import React from "react";
import {Container, Row, Col} from "react-bootstrap";

const Error = props => {
    return(
        <Container>
            <Row>
                <Col>
                    <h2>Error {props.code}</h2>
                </Col>
            </Row>
            <Row>
                <h4>Oops! Something went wrong! Process could not be completed.</h4>
            </Row>
        </Container>
    );
}

export default Error;