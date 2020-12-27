import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Gauge = props => {

    const[data, setData] = useState(props.data);

    const result = data['value']
    const threshold = 210

    if (result < 0){
      var colour = 'white';
      var causal = 'Data Unavailable';
      var val = None;
    } else if (result < threshold){
      var colour = 'rgb(51, 51, 51)';
      var causal = 'Causal Test Failed';
      var val = result;
    } else {
      var colour = 'rgb(47, 79, 255)';
      var causal = 'Causal Test Passed';
      var val = result;
    }

    const trace = [
      {
        domain: { x: [0, 1], y: [0, 1] },
        value: val,
        title: { text: causal, font: { size: 24 } },
        number: {'suffix': "/300<br>Tests Passed", 'font': {'size': 50}},
        type: "indicator",
        mode: "gauge+number",
        gauge: { axis: { range: [null, 300] }, 
        bar: {'color': colour},
        threshold: {
          line: { color: "black", width: 4 },
          thickness: 1,
          value: 210
        } }
      }
    ];


    const layout = { width: 475, height: 400, paper_bgcolor: 'rgb(249, 249, 249)'};

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