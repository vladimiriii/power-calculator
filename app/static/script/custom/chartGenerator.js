function createChartConfig() {
    return {
        // The type of chart we want to create
        type: 'line',

        // Data
        data: {
            labels: [],
            datasets: [],
        },

        // Configuration options go here
        options: {
            title: {
                display: true,
                fontSize: 18,
                fontStyle: "normal",
                text: ""
            },
            scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
                        labelString: ""
					}
				}],
				yAxes: [{
					display: true,
                    ticks: {
                        beginAtZero: true,
                        callback: function(value, index, values) {
                            return Number(value).toLocaleString();
                    }
                    },
					scaleLabel: {
						display: true,
                        labelString: ""
					}
				}]
			},
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label = data.datasets[tooltipItem.datasetIndex].label || '';
                        if (label) {
                            label += ': ';
                        };
                        label += Number(tooltipItem.yLabel).toLocaleString();
                        return label;
                    }
                }
            },
            annotation: {
                annotations: []
            }
        }
    };
}


function createChart(div, chartData) {
    const config = createChartConfig();
    const canvas = $('#' + div)[0].getContext('2d');
    const chart = new Chart(canvas, config);

    config['options']['title']['text'] = chartData['title'];
    config['options']['scales']['xAxes'][0]['scaleLabel']['labelString'] = chartData['xAxisLabel'];
    config['options']['scales']['yAxes'][0]['scaleLabel']['labelString'] = chartData['yAxisLabel'];
    config['data']['labels'] = chartData['labels'];
    config['data']['datasets'] = chartData['dataset'];

    if ("hidePoints" in chartData) {
        config['options']['elements']['point']['radius'] = 0;
        config['options']['tooltips']['enabled'] = false;
    }
    if ("verticalLine" in chartData) {
        annotation = {
            type: "line",
            mode: "vertical",
            scaleID: "x-axis-0",
            value: chartData['verticalLine']['position'],
            borderColor: "black",
            label: {
                content: chartData['verticalLine']['label'],
                enabled: true,
                position: "top"
            }
        };
        config['options']['annotation']['annotations'][0] = annotation;
    }

    chart.update();
}


function clearCharts() {
    const charts = $(".chart");
    for (const key in charts) {
        const id = charts[key]['id'];
        let blankCanvas = `<canvas class="chart" id="chart-${String(Number(key) + 1)}"></canvas>`
        $("#" + id).replaceWith(blankCanvas);
    }
}
