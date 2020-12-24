import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Scatter from "./Scatter";
import Loading from "../Loading";
const SentimentScatter = props => {
    const[data, setData] = useState([]);
    const[isLoading, setIsLoading] = useState(true);

    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/trends/sentiment_scatter', formdata)
        .then(res => {
            const tweetsDf = res.data;
            setData(tweetsDf)
            console.log(tweetsDf)

            setIsLoading(false);
        })
        .catch(e => {
            console.log(e)
        })
    }

    useEffect(( ) => {
        fetchData();
    }, []);

    return(
        <React.Fragment>
          {isLoading ?
              <Container>
                  <Loading/>
              </Container>
          :
              <Container>
                <Row>
                    <Col><h3>Retweet Count vs Favorite Count</h3></Col>
                </Row>
                <Row>
                    <Col><Scatter data={data}/></Col>
                </Row>
              </Container>
          }
        </React.Fragment>
    );
}
export default SentimentScatter;