import React, {useEffect, useState} from 'react'
import {Container, Spinner, Row, Col} from 'react-bootstrap';
import Error from "../Error";

import http from '../../http-common'
import Loading from "../Loading";
const TweetSummary = props => {
    const[frequency, setFrequency] = useState(JSON.parse(sessionStorage.getItem('tweetFreq')));
    const[favourites, setFavourites] = useState(JSON.parse(sessionStorage.getItem('tweetFavourites')));
    const[retweets, setRetweets] = useState(JSON.parse(sessionStorage.getItem('retweets')));
    const[isLoading, setIsLoading] = useState(true);
    const[isError, setIsError] = useState(false);

    useEffect(( ) => {
        if(frequency === null || favourites === null || retweets === null){
            fetchData();
        }else{
            setIsLoading(false)
        }
    }, []);

    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets/tweet_summary', formdata)
            .then(res => {
                if(res.data[0] !== null){
                    setFrequency(res.data[0]);
                    sessionStorage.setItem('tweetFreq', JSON.stringify(res.data[0]))  
                }else{
                    setFrequency(0);
                      
                }

                if(res.data[1] !== null){
                    setFavourites(res.data[1])
                    sessionStorage.setItem('tweetFavourites', JSON.stringify(res.data[1]))  
                }else{
                    setFavourites(0)
                }

                if(res.data[2] !== null){
                    setRetweets(res.data[2])   
                    sessionStorage.setItem('retweets', JSON.stringify(res.data[2]))
                }else{
                    setRetweets(0)
                }
                
                console.log("frequency:", frequency, "favourites:", favourites, "retweets:", retweets)
                

                setIsLoading(false);
            })
            .catch(e => {
                setIsError(true);
                console.log(e)
            })

    }

    return <React.Fragment>
            <Container>
                {isError ?
                    <Row>
                        <Col>
                            <Error/>
                        </Col>
                    </Row>
                :
                    <Col>
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
                    </Col>
                }
            </Container>
    </React.Fragment>;
}

export default TweetSummary;