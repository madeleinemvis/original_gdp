import React from "react";
import {Container, Row, Col} from "react-bootstrap";

const Error = props => {
    return(
        <Container>
            <Row>
                <Col>
                    <p><strong>ERROR OCCURRED</strong></p>
                    <p>Oops! Something went wrong! Process could not be completed.</p>
                </Col>
            </Row>
        </Container>
    );
}

export default Error;