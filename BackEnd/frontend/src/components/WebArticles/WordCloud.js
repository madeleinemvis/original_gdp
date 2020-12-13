import React, {useEffect, useState} from 'react'
import {TagCloud} from "react-tagcloud";
import {Spinner} from 'react-bootstrap';

import http from '../../http-common'
const WordCloud = props => {
    const[wordCloud, setWordCloud] = useState({});
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
                    setIsLoading(false);
                })
                .catch(e => {
                    console.log(e)
                })

        }

        fetchData();
    }, []);

    return <React.Fragment>
                {isLoading &&
                    <Loading/>
                }
                {!isLoading &&
                    <TagCloud
                        minSize={10}
                        maxSize={35}
                        tags = { wordCloud }/>
                }
    </React.Fragment>;
}

const Loading = () => {
    return <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
    </Spinner>
}

export default WordCloud;