import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Scatter = props => {

    const[data, setData] = useState(props.data);

    const positive_data = data['positive']
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
            el['favorite_count']),
        y: negative_data.map((el) =>
            el['retweet_count']),
        mode: 'markers',
        name: 'Negative Sentiment',
        type: 'scatter',
        marker: {color: 'red'}
    };

    const chart_data = [ trace1, trace2 ]


    const layout = {
      xaxis: {
        range: [ 0, Math.max(positive_data.map((el) =>
            el['x']).concat(negative_data.map((el) =>
            el['x']))) ]
      },
      yaxis: {
        range: [0, Math.max(positive_data.map((el) =>
            el['y']).concat(negative_data.map((el) =>
            el['y']))) ]
      },
      title:'Retweet Count vs Favorite Count'
    };

    const config = {
        response: true
    };

    return(
        Plotly.newPlot('fc_rt_scatter', chart_data, layout, config)
    );
}
export default Scatter;