import React, {useEffect, useState} from 'react'
import {Container, Row, Col} from 'react-bootstrap';


import Loading from "../Loading";
const TweetFreq = props => {
    const[frequency, setFrequency] = useState(0);
    const[isLoading, setIsLoading] = useState(true);
    const[isEmpty, setIsEmpty] = useState(false);

    useEffect(() => {
        setIsLoading(true)
        setFrequency(props.tweetsFreq)
        setIsLoading(false)        
    }, [props.tweetsFreq]);

    return <React.Fragment>
            <Container>
                <Row>
                    <Col>
                        <h4>Number of Tweets Collected</h4>
                    </Col>
                </Row>
                <Row>
                    {frequency === 0 ?
                        <Col>
                            <Loading/>
                        </Col>
                        :
                        <Col>
                            <h1>{frequency}</h1>
                        </Col>
                    }
                </Row>
            </Container>
    </React.Fragment>;
}

export default TweetFreq;