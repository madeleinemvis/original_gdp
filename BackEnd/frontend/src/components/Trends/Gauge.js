import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Gauge = props => {

    const[data, setData] = useState(props.data);

    const result = data['value']
    const threshold = 210

    const trace = [
      {
        domain: { x: [0, 1], y: [0, 1] },
        value: 450,
        title: { text: "Speed" },
        type: "indicator",
        mode: "gauge+number",
        delta: { reference: 400 },
        gauge: { axis: { range: [null, 500] }, 'bar': {'color': 'red'} }
      }
    ];


    const layout = { width: 600, height: 400 };

    const config = {
        responsive: true
    };

    return(
        <Plot
            data={trace}
            layout={layout}
            config={config}
        />
    );
}
export default Gauge;