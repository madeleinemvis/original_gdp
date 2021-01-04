import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Bar from "./Bar";
import Loading from "../Loading";
import Error from "../Error";
const EconBar = props => {
    const[data, setData] = useState(JSON.parse(sessionStorage.getItem('econ')));
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
        http.post('/trends/econ_bar', formdata)
        .then(res => {
            const causalDf = res.data;
            setData(causalDf)
            console.log("causal:"+ causalDf)

            sessionStorage.setItem('econ', JSON.stringify(causalDf))
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
                    <Col><h3>Economics Causal Results</h3></Col>
                </Row>
                <Row>
                {isError ?
                            <Col>
                                <Error/>
                            </Col>
                            :
                            <Col>
                                <Bar data={data}/>
                            </Col>
                        }
                </Row>
              </Container>
          }
        </React.Fragment>
    );
}
export default EconBar;