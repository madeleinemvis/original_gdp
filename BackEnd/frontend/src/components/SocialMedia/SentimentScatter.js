import React, {useEffect, useState} from 'react'
import {Spinner} from 'react-bootstrap';

import http from '../../http-common'
const SentimentScatter = props => {
    // const[sentimentScatter, setSentimentScatter] = useState({});
    const[isLoading, setIsLoading] = useState(true);

    useEffect(( ) => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", props.uid);
            http.post('/tweets/sentiment_scatter$', formdata)

                .then(res => {
                    const tweetsDf = res.data;
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
                    <h1>Here is a scatter plot</h1>
                }
    </React.Fragment>;
}

const Loading = () => {
    return <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
    </Spinner>
}

export default SentimentScatter;