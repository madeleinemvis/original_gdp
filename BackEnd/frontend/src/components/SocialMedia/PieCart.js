import React, {useState} from "react";
import Plot from 'react-plotly.js';

const PieChart = props => {

    const[data, setData] = useState(props.data);

    const raw_data = {
        values: [data['positive'], data['neutral'], data['negative']],
        labels: ["Positive", "Neutral", "Negative"],
        type: 'pie',
    }
    const chart_data = [raw_data]

    const layout = {
        width: '100%',
        autosize: true,
        title:'Tweet Sentiment Pie Chart',
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
export default PieChart;