import React, {useEffect, useState} from 'react'
import {TagCloud} from "react-tagcloud";
import {Spinner} from 'react-bootstrap';

const WordCloud = () => {
    const[wordCloud, setWordCloud] = useState({});
    const[isLoading, setIsLoading] = useState(true);


    useEffect(( ) => {
        const fetchData = () => {
            const formdata = new FormData();
            formdata.append("uid", "some_random_hash");
            const requestOptions = {
                method: 'POST',
                body: formdata,
                redirect: 'follow',
            };
            const url = "http://127.0.0.1:8080/api/documents/wordcloud";
            fetch(url, requestOptions)
                .then(function(response) {
                    console.log("Response:", response);
                    return response.text()
                })
                .then(data => {
                    const tempCloud = []
                    let keywords;
                    keywords = JSON.parse(data);
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

    console.log("Word Cloud:", wordCloud);
    console.log("IsLoading:", isLoading);

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