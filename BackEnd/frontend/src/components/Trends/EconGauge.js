import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Gauge from "./Gauge";
import Loading from "../Loading";
const EconGauge = props => {
    const[data, setData] = useState([]);
    const[isLoading, setIsLoading] = useState(true);

    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/trends/econ_gauge', formdata)
        .then(res => {
            const causalDf = res.data;
            setData(causalDf)
            console.log(causalDf)

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
                    <Col><h3>Economics Causal Test</h3></Col>
                </Row>
                <Row>
                    <Col><Gauge data={data}/></Col>
                </Row>
              </Container>
          }
        </React.Fragment>
    );
}
export default EconGauge;