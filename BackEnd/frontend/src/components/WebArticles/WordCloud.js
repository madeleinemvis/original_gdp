import React, {useEffect, useState} from 'react'
import {TagCloud} from "react-tagcloud";
import {Row, Col, Container} from 'react-bootstrap';
import http from '../../http-common'
import Loading from "../Loading";

const WordCloud = props => {
    const[wordCloud, setWordCloud] = useState(props.wordCloud)



    useEffect(()=>{
        setWordCloud(props.wordCloud)    
    },[props.wordCloud])


    const options = {hue: 'blue'};
    return (
        <React.Fragment>
            <Container>
                <Row>
                    <Col>
                        <h3>Word Cloud of High-Ranking Keywords</h3>
                    </Col>
                </Row>
                <Row>
                    {wordCloud.length === 0 ?
                        <Col>
                            <Loading/>
                        </Col>
                        :
                        <Col>
                            {wordCloud.length === 0 ?
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