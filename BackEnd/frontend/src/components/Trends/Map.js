import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Map = props => {

    const[data, setData] = useState(props.data);

    const estimate = 1;
    const random = 1;
    const unobserved = 1;
    const placebo = 1;
    const subset = 1;

    const trace = [
      {
        x: ['estimate', 'random', 'unobserved', 'placebo', 'subset'],
        y: [estimate, random, unobserved, placebo, subset],
        marker:{
          color: ['rgb(47, 79, 255)', 'rgb(47, 79, 255)', 'rgb(47, 79, 255)', 'rgb(51, 51, 51)', 'rgb(47, 79, 255)']
        },
        type: 'bar'
      }
    ];

    const layout = { width: 475, height: 400, 
      yaxis: {
        title: 'Estimate Value' }};

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
export default Map;