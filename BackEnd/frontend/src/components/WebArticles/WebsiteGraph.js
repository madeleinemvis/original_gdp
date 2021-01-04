import React, {useEffect, useState} from 'react'
import {Col, Container, Row} from 'react-bootstrap';
import http from '../../http-common'
import Loading from "../Loading";
import Graph from "./Graph";
import Error from "../Error";

const WebsiteGraph = props => {
    const [graph, setGraph] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);

    useEffect(() => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/documents/graph', formdata)
                .then(res => {
                    let tempGraph;
                    tempGraph = res.data;
                    let jsonGraph = JSON.parse(tempGraph);
                    setGraph(jsonGraph);
                    setIsLoading(false);
                })
                .catch(e => {
                    setIsError(true);
                    console.log(e);
                })
        }
        fetchData();
    }, []);

    return (
        <React.Fragment>
            <Container>
                <Row>
                    <Col>
                        <h3>Graph of Websites Crawled</h3>
                    </Col>
                </Row>
                {isLoading &&
                <Row>
                    <Col>
                        <Loading/>
                    </Col>
                </Row>
                }
                {!isLoading &&
                <Row>
                    {isError ?
                        <Col>
                            <Error/>
                        </Col>
                        :
                        <Col>
                            <svg></svg>
                            <Graph graph={graph}/>
                        </Col>
                    }
                </Row>
                }
            </Container>
        </React.Fragment>
    );
}

export default WebsiteGraph;