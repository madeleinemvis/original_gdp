import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Scatter = props => {

    const[data, setData] = useState(props.data);

    const positive_data = data['positive']
    const neutral_data = data['neutral']
    const negative_data = data['negative']

    const trace1 = {
        x: positive_data.map((el) =>
            el['x']),
        y: positive_data.map((el) =>
            el['y']),
        mode: 'markers',
        name: 'Positive Sentiment',
        type: 'scatter',
        marker: {color: 'green'}
    };

    const trace2 = {
        x: negative_data.map((el) =>
            el['x']),
        y: negative_data.map((el) =>
            el['y']),
        mode: 'markers',
        name: 'Negative Sentiment',
        type: 'scatter',
        marker: {color: 'red'}
    };

    const trace3 = {
        x: neutral_data.map((el) =>
            el['x']),
        y: neutral_data.map((el) =>
            el['y']),
        mode: 'markers',
        name: 'Neutral Sentiment',
        type: 'scatter',
        marker: {color: 'orange'}
    }

    const chart_data = [ trace1, trace2, trace3 ]


    const layout = {
        width: '100%',
        height: '100%',
        autosize: false,
        xaxis: {
        range: [ 0, Math.max(positive_data.map((el) => el['x'])
                .concat(negative_data.map((el) => el['x']))
                .concat(neutral_data.map((el) => el['x']))) ]
        },
        yaxis: {
        range: [0, Math.max(positive_data.map((el) => el['y'])
                .concat(negative_data.map((el) => el['y']))
                .concat(neutral_data.map((el) => el['y']))) ]
        },
        title:'Retweet Count vs Favorite Count',
        paper_bgcolor : '#f9f9f9',
        plot_bgcolor : '#f9f9f9'
    };

    const config = {
        responsive: true
    };

    return(
        <Plot
            data={chart_data}
            layout={layout}
            config={config}
        />
    );
}
export default Scatter;