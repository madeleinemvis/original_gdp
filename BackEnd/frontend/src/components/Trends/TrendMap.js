import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Map from "./Map";
import Loading from "../Loading";
import Error from "../Error";
const TrendMap = props => {
    const[data, setData] = useState(JSON.parse(sessionStorage.getItem('trend')));
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
        http.post('/trends/trend_map', formdata)
        .then(res => {
            const causalDf = res.data;
            setData(causalDf)
            console.log("causal:"+ causalDf)
            sessionStorage.setItem('trend', JSON.stringify(causalDf))
            setIsLoading(false);
        })
        .catch(e => {
            setIsError(true)            
            console.log(e)
        })
    }

    return(
        <React.Fragment>
          {isLoading ?
              <Container>
                  <Loading/>
              </Container>
          :
              <Container>
                <Row>
                    <Col><h3>World Trend Map</h3></Col>
                </Row>
                <Row>
                {isError ?
                            <Col>
                                <Error/>
                            </Col>
                            :
                            <Col>
                                <Map data={data}/>
                            </Col>
                        }
                </Row>
              </Container>
          }
        </React.Fragment>
    );
}
export default TrendMap;