import React, {useState} from "react";
import Plot from 'react-plotly.js';

const Map = props => {

    const[data, setData] = useState(props.data);

    const countries = data['countries'];
    const trends = data['trends'];

    const trace = [{
      type: 'choropleth',
      locations: countries,
      z: trends,
      colorscale: [
          [0,'rgb(229,236,246)'],[1.0,'rgb(47, 79, 255)']],
      autocolorscale: false,
      marker: {
          line: {
              color: 'rgb(51, 51, 51)',
              width: 0.02
          }
      },
      tick0: 0,
      zmin: 0,
      dtick: 1000,
      colorbar: {
          autotic: false,
          title: 'Trends<br>Value'
      }
    }];

    const layout = { width: 1000, height: 600, paper_bgcolor: 'rgb(249, 249, 249)',
                    geo:{
                        showframe: false,
                        showcoastlines: false,
                        showocean: true, 
                        oceancolor: 'rgb(249, 249, 249)',
                        projection:{
                            type: 'equirectangular'
                        }
                    }};

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