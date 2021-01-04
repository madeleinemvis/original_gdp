import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import PieChart from "./PieChart";
import Loading from "../Loading";
import Error from "../Error";

const ArticlePie = props => {
    const[data, setData] = useState(JSON.parse(sessionStorage.getItem('artPie')));
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
        http.post('/documents/pie_chart', formdata)
        .then(res => {
            const articleDf = res.data;
            setData(articleDf)
            console.log(articleDf)
            sessionStorage.setItem('sentPie', JSON.stringify(articleDf))
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
export default ArticlePie;