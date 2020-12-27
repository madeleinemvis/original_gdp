import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Bar = props => {

    const[data, setData] = useState(props.data);

    const estimate = data['estimate'];
    const random = data['random'];
    const unobserved = data['unobserved'];
    const placebo = data['placebo'];
    const subset = data['subset'];

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

    const layout = { width: 475, height: 400, paper_bgcolor: 'rgb(249, 249, 249)', 
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
export default Bar;