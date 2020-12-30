import React, {useEffect, useState} from 'react'
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Loading from "../Loading";
import Graph from "./Graph";

const WebsiteGraph = props => {
    const [graph, setGraph] = useState({});
    const [isLoading, setIsLoading] = useState(true);

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
                    console.log(e)
                })
        }
        fetchData();
    }, []);

    return (
        <React.Fragment>
            {isLoading &&
            <Container>
                <Loading/>
            </Container>
            }
            {!isLoading &&
            <Container>
                <Row>
                    <Col>
                        <h3>Graph of Discovered Websites</h3>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        {graph === {} ?
                            <p>No Websites Found</p>
                            :
                            <Graph graph={graph}/>
                        }
                    </Col>
                </Row>
            </Container>
            }
        </React.Fragment>
    );
}

export default WebsiteGraph;