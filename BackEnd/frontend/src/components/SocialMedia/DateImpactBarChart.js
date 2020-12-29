import React, {useState} from "react";
import Plot from 'react-plotly.js';

const DateImpactBarChart = props => {

    const[data, setData] = useState(props.data);

    const raw_data = {
        x: data[0],
        y: data[1],
        type: 'bar'
    }
    const chart_data = [raw_data]

    const layout = {
        width: '100%',
        autosize: true,
        title: 'Daily Tweet Engagements',
        labels: {"x":"Date","y":"Total Tweet Engagments"}
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
export default DateImpactBarChart;