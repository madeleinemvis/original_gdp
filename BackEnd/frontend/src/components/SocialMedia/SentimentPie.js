import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import PieChart from "./PieCart";
import Loading from "../Loading";
import Error from "../Error";

const SentimentPie = props => {
    const[data, setData] = useState([]);
    const[isLoading, setIsLoading] = useState(true);
    const[isError, setIsError] = useState(false);

    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets/sentiment_pie_chart', formdata)
        .then(res => {
            const tweetsDf = res.data;
            setData(tweetsDf)
            console.log(tweetsDf)

            setIsLoading(false);
        })
        .catch(e => {
            setIsError(true);
            console.log(e)
        })
    }

    useEffect(( ) => {
        fetchData();
    }, []);

    return(
        <React.Fragment>
            <Container>
                {isError ?
                    <Row>
                        <Col>
                            <Error/>
                        </Col>
                    </Row>
                :
                    <Row>
                        {isLoading ?
                            <Col>
                                <Loading/>
                            </Col>
                        :
                            <Col>
                                <div className="Pie-chart">
                                    <PieChart data={data}/>
                                </div>
                            </Col>
                        }
                    </Row>
                }
            </Container>
        </React.Fragment>
    );
}
export default SentimentPie;