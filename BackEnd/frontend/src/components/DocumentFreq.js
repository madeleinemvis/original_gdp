import React, {useEffect, useState} from 'react'
import {Container, Spinner, Row, Col} from 'react-bootstrap';

import http from '../http-common'
const DocumentFreq = props => {
    const[frequency, setFrequency] = useState(0);
    const[isLoading, setIsLoading] = useState(true);
    const[isEmpty, setIsEmpty] = useState(false);

    useEffect(( ) => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/documents/freq', formdata)

                .then(res => {
                    setFrequency(res.data);
                    console.log("frequency:", frequency)
                    if(frequency == 0){
                        setIsEmpty(true);
                    }
                    setIsLoading(false);
                    console.log("isEmpty:", isEmpty)
                })
                .catch(e => {
                    console.log(e)
                })

        }

        fetchData();
    }, []);

    return <React.Fragment>
                {isLoading &&
                    <Loading/>
                }
                {!isLoading &&
                    <Container>
                        <Row>
                            <Col> <h4>Number of Documents Collected</h4></Col>
                        </Row>
                        <Row>
                            <Col><h1>{frequency}</h1></Col>
                        </Row>
                    </Container>



                }
    </React.Fragment>;
}

const Loading = () => {
    return <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
    </Spinner>
}

export default DocumentFreq;