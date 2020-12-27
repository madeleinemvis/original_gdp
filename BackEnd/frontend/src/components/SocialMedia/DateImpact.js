import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import DateImpactBarChart from "./DateImpactBarChart";
import Loading from "../Loading";

const DateImpact = props => {
    const[data, setData] = useState([]);
    const[isLoading, setIsLoading] = useState(true);

    const fetchData = () => {
        const formdata = new FormData();
        formdata.append("uid", props.uid);
        http.post('/tweets/date_impact_bar', formdata)
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
                    <Col><DateImpactBarChart data={data}/></Col>
                </Row>
              </Container>
          }
        </React.Fragment>
    );
}
export default DateImpact;