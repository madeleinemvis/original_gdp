import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Gauge = props => {

    const[data, setData] = useState(props.data);

    const result = data['value']
    const threshold = 210

    if (result < 0){
      const colour = 'white'
      const causal = 'Data Unavailable'
      const val = None
    } else if (result < threshold){
      const colour = 'rgb(51, 51, 51)'
      const causal = 'Causal Test Failed'
      const val = result
    } else {
      const colour = 'rgb(47, 79, 255)'
      const causal = 'Causal Test Passed'
      const val = result
    }

    const trace = [
      {
        domain: { x: [0, 1], y: [0, 1] },
        value: val,
        title: { text: causal },
        type: "indicator",
        mode: "gauge+number",
        gauge: { axis: { range: [null, 300] }, 'bar': {'color': colour},
        'steps': [
            {'range': [0, 300], 'color': 'rgb(235, 235, 235)'}, ],
        'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 1, 'value': threshold} }
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