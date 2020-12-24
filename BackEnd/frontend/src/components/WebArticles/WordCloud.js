import React, {useEffect, useState} from 'react'
import {TagCloud} from "react-tagcloud";
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Loading from "../Loading";

const WordCloud = props => {
    const[wordCloud, setWordCloud] = useState({});
    const[isEmpty, setIsEmpty] = useState(true);
    const[isLoading, setIsLoading] = useState(true);

    useEffect(( ) => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/documents/wordcloud', formdata)
                .then(res => {
                    const tempCloud = []
                    let keywords;
                    keywords = res.data;
                    
                    let x = 0;
                    for (let k in keywords) {
                        tempCloud[x] = {value: k, count: keywords[k]};
                        x += 1;
                    }
                    setWordCloud(tempCloud);
                    if (wordCloud !== {}){
                        setIsEmpty(false);
                    }
                    setIsLoading(false);
                })
                .catch(e => {
                    console.log(e)
                })
        }
        fetchData();
    }, []);

    const options = {hue: 'blue'};

    console.log("colors:", options)
    return (
        <React.Fragment>
            <Container>
                <Row>
                    <Col>
                        <h3>Word Cloud of High-Ranking Keywords</h3>
                    </Col>
                </Row>
                <Row>
                    {isLoading ?
                        <Col>
                            <Loading/>
                        </Col>
                        :
                        <Col>
                            {isEmpty ?
                                <p>No Documents Found</p>
                                :
                                <TagCloud
                                    colorOptions={options}
                                    minSize={10}
                                    maxSize={35}
                                    tags={wordCloud}/>

                            }
                        </Col>
                    }
                </Row>
            </Container>
        </React.Fragment>
    );
}

export default WordCloud;