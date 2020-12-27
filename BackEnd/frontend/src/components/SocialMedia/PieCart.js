import React, {useState} from "react";
import Plot from 'react-plotly.js';

const PieChart = props => {

    const[data, setData] = useState(props.data);

    const chart_data = {
        type: 'pie',
        values: [data['positive'], data['neutral'], data['negative']],
        labels: ["Positive", "Neutral", "Negative"],
        textinfo: "label+percent",
        textposition: "outside",
        automargin: true
    }

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