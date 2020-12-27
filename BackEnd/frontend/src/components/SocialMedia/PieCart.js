import React, {useState} from "react";
import Plot from 'react-plotly.js';

const PieChart = props => {

    const[data, setData] = useState(props.data);

    const raw_data = {
        values: [data['positive'], data['neutral'], data['negative']],
        labels: ["Positive", "Neutral", "Negative"],
        marker: {
            colors: [
                'rgb(51,255,51)',
                'rgb(51,51,255)',
                'rgb(255,51,51)'
            ]
        },
        type: 'pie',
        textinfo: "label+percent",
        textposition: "outside",
        automargin: true

    }
    const chart_data = [raw_data]

    const layout = {
        width: '100%',
        autosize: true,
        showlegend: false
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