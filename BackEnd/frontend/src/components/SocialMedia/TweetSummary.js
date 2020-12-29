import React, {useEffect, useState} from 'react'
import {Container, Spinner, Row, Col} from 'react-bootstrap';

import http from '../../http-common'
import Loading from "../Loading";
const TweetSummary = props => {
    const[frequency, setFrequency] = useState(0);
    const[favourites, setFavourites] = useState(0);
    const[retweets, setRetweets] = useState(0);
    const[isLoading, setIsLoading] = useState(true);
    const[isEmpty, setIsEmpty] = useState(false);

    useEffect(( ) => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/tweets/tweet_summary', formdata)
                .then(res => {
                    setFrequency(res.data[0]);
                    setFavourites(res.data[1])
                    setRetweets(res.data[2])
                    console.log("frequency:", frequency, "favourites:", favourites, "retweets:", retweets)
                    setIsLoading(false);
                })
                .catch(e => {
                    console.log(e)
                })

        }

        fetchData();
    }, []);

    return <React.Fragment>
            <Container>
                <Row>
                    <Col>
                        <h4>Number of Tweets Collected</h4>
                    </Col>
                </Row>
                <Row>
                    {isLoading ?
                        <Col>
                            <Loading/>
                        </Col>
                        :
                        <Col>
                            <h1>{frequency}</h1>
                        </Col>
                    }
                </Row>
                <Row>
                    <Col>
                        <h4>Total Favourites</h4>
                    </Col>
                </Row>
                <Row>
                    {isLoading ?
                        <Col>
                            <Loading/>
                        </Col>
                        :
                        <Col>
                            <h1>{favourites}</h1>
                        </Col>
                    }
                </Row>
                <Row>
                    <Col>
                        <h4>Total Retweets</h4>
                    </Col>
                </Row>
                <Row>
                    {isLoading ?
                        <Col>
                            <Loading/>
                        </Col>
                        :
                        <Col>
                            <h1>{retweets}</h1>
                        </Col>
                    }
                </Row>
            </Container>
    </React.Fragment>;
}

export default TweetSummary;