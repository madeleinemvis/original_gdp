import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import DateImpactBarChart from "./DateImpactBarChart";
import Loading from "../Loading";
import Error from "../Error";

const DateImpact = props => {
    const[data, setData] = useState(JSON.parse(sessionStorage.getItem('dateImpact')));
    const[isLoading, setIsLoading] = useState(true);
    const[isError, setIsError] = useState(false);


    useEffect(( ) => {
        if(data === null){
            fetchData();
        }else{
            setIsLoading(false)
        }
        
    }, []);

    
    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets/date_impact_bar', formdata)
        .then(res => {
            const tweetsDf = res.data;
            setData(tweetsDf)
            console.log(tweetsDf)
            sessionStorage.setItem('dateImpact', JSON.stringify(tweetsDf))
            setIsLoading(false);
        })
        .catch(e => {
            setIsError(true);
            console.log(e)
        })
    }
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
                                <div className="date-impact">
                                    <DateImpactBarChart data={data}/>
                                </div>
                            </Col>
                        }
                    </Row>
                }
            </Container>
        </React.Fragment>
    );
}
export default DateImpact;