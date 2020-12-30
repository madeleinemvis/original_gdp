import React, {useEffect, useState} from 'react'
import {Container, Spinner, Row, Col} from 'react-bootstrap';

import http from '../../http-common'
import Loading from "../Loading";
const DocumentFreq = props => {
    const[frequency, setFrequency] = useState(0);
    const[isLoading, setIsLoading] = useState(true);

    useEffect(( ) => {
        setFrequency(props.docFreq)
    }, [props.docFreq]);

   

    return(
        <React.Fragment>
            <Container>
                <Row>
                    <Col><h4>Number of Documents Collected</h4></Col>
                </Row>
                <Row>
                    {frequency === 0 ?
                        <Col>
                            <Loading/>
                        </Col>
                    :
                         <Col><h1>{frequency}</h1></Col>
                    }
                </Row>
                </Container>
        </React.Fragment>);
}
export default DocumentFreq;