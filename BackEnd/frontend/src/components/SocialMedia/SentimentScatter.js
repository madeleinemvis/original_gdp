import React, {useEffect, useState} from 'react'
import {Spinner} from 'react-bootstrap';

import http from '../../http-common'
import Scatter from "./Scatter";
const SentimentScatter = props => {
    const[data, setData] = useState([]);
    const[isLoading, setIsLoading] = useState(true);

    useEffect(( ) => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/tweets/sentiment_scatter', formdata)

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

        fetchData();
    }, []);

    return <React.Fragment>
                {isLoading &&
                    <Loading/>
                }
                {!isLoading &&
                    <Scatter data={data}/>
                }
    </React.Fragment>;
}

const Loading = () => {
    return <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
    </Spinner>
}

export default SentimentScatter;