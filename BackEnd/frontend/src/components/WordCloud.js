import React from 'react'
import {TagCloud} from "react-tagcloud";

class WordCloud extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            keywords: {},
            wordCloud: [],
            isLoading: true,
        };
    }

    async componentDidMount() {
        const formdata = new FormData();
        formdata.append("uid", "some_random_hash");
        const requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow',
        };
        const url = "http://127.0.0.1:8080/api/frontend/wordcloud";
        await fetch(url, requestOptions)
            .then(function(response) {
                return response.text()
            })
            .then(data => {
                this.setState({
                    keywords: JSON.parse(data)
                });
                return data;
            })
        this.renderCloud();
    }

    renderCloud() {
        const wordCloud = []
        const keys = Object.keys(this.state.keywords);
        keys.forEach((key, i) => {
            wordCloud[i] = {value: key, count: this.state.keywords[key]}
        });
        this.setState({
            wordCloud: wordCloud,
            isLoading: false
        });
    }
    render() {
        return <div>
            {this.state.isLoading ?
                <div>Loading...</div>
                :
                <div>
                    <TagCloud
                        minSize={10}
                        maxSize={35}
                        tags = { this.state.wordCloud }/>
                </div>}
        </div>;
    }

}

export { WordCloud };
