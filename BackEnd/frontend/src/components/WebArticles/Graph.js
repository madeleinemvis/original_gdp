import React from 'react'
import * as d3 from 'd3'

function drawChart(graph) {
    const svg = d3.select("svg"),
        width = svg.attr("width"),
        height = svg.attr("height");

    const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    const linkedByIndex = {};

    const link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke-width", function (d) {
            return Math.sqrt(d.value);
        });

    const node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("r", scaledSize)
        .attr("fill", function (d) {
            return color(d.degree);
        })
        .on("mouseover", mouseOver(.7))
        .on("mouseout", mouseOut)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    svg.selectAll("circle").on("click", function (d) {
        let name = "Website: " + d.name.toUpperCase();

        let country = document.getElementById("website");
        country.innerHTML = name;
    });

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });
    }

    const nodeDegrees = {};

    graph.links.forEach(function (d) {
        if (d.source.index in linkedByIndex) {
            linkedByIndex[d.source.index][d.target.index] = 1;
        } else {
            let val = {};
            val[d.target.index] = 1;
            linkedByIndex[d.source.index] = val;
        }

        if (d.source.index in nodeDegrees) {
            let val = nodeDegrees[d.source.index];
            nodeDegrees[d.source.index] = (val + 1);
        } else {
            nodeDegrees[d.source.index] = 1;
        }
    });

    function isConnected(a, b) {
        if (linkedByIndex[a.index][b.index] === 1) {
            return 1;
        }
    }

    function scaledSize(d) {
        return d.degree * 0.5;
    }

    function mouseOver(opacity) {
        return function (d) {
            // check all other nodes to see if they're connected
            // to this one. if so, keep the opacity at 1, otherwise
            // fade
            div.transition()
                .duration(200)
                .style("opacity", .9);

            div.html(d.name)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");

            node.style("stroke-opacity", function (o) {
                return isConnected(d, o) ? 1 : opacity;
            });

            node.style("fill-opacity", function (o) {
                return isConnected(d, o) ? 1 : opacity;
            });
            // also style link accordingly
            link.style("stroke-opacity", function (o) {
                return o.source === d ? 1 : opacity;
            });

            link.style("stroke", function (o) {
                return o.source === d ? "rgb(255, 0, 0)" : "#ddd";
            });

            link.style("stroke-width", function (o) {
                return o.source === d ? 3 : 1;
            });
        };
    }

    function mouseOut() {
        div.transition()
            .duration(500)
            .style("opacity", 0);

        node.style("stroke-opacity", 1);
        node.style("fill-opacity", 1);
        link.style("stroke-opacity", 1);
        link.style("stroke", "#ddd");
        link.style("stroke-width", 1);
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

export function Graph(props) {
    return (<div>{drawChart(props.graph)}</div>);
}

export default Graph;