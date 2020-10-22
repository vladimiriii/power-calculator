let configOne = null;
let configTwo = null;
let chartOne = null;
let chartTwo = null;

const sampleData = {
    title: "Chart 1",
    xAxisLabel: "Month",
    yAxisLabel: "Score",
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    dataset: [
        {
            label: "Lower Powers",
            data: [0, 10, 5, 2, null, null, null]
        },
        {
            label: "Higher Powers",
            data: [null, null, null, 2, 20, 30, 45]
        }
    ]
}

const chartColors = [
    {
        "line": "#d9486e",
        "background": "#e3bfc8"
    },
    {
        "line": "#325d88",
        "background": "#d3dee8"
    }
];


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
                fontSize: 24,
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
					scaleLabel: {
						display: true,
                        labelString: ""
					}
				}]
			},
            legend: {
                display: false
            }
        }
    };
}


function generateChart(id, config) {
    const div = $('#' + id)[0].getContext('2d');
    return new Chart(div, config)
}


function generateDatasets(data) {
    for (let i = 0; i < data.length; ++i) {
        data[i]['backgroundColor'] = chartColors[i]['background'];
        data[i]['borderColor'] = chartColors[i]['line'];
    }
    return data;
}


function updateChart(chart, config, chartData) {
    config['options']['title']['text'] = chartData['title'];
    config['options']['scales']['xAxes'][0]['scaleLabel']['labelString'] = chartData['xAxisLabel'];
    config['options']['scales']['yAxes'][0]['scaleLabel']['labelString'] = chartData['yAxisLabel'];
    config['data']['labels'] = chartData['labels'];
    config['data']['datasets'] = generateDatasets(chartData['dataset']);
	chart.update();
}
    // const div = $('#' + id)[0].getContext('2d');
    // const chart = new Chart(div, {
    //     // The type of chart we want to create
    //     type: 'line',
    //
    //     // The data for our dataset
    //     data: {
    //         labels: options['labels'],
    //         datasets: generateDatasets(options['dataset']),
    //     },
    //
    //     // Configuration options go here
    //     options: {
    //         title: {
    //             display: true,
    //             fontSize: 24,
    //             fontStyle: "normal",
    //             text: options['title']
    //         },
    //         scales: {
	// 			xAxes: [{
	// 				display: true,
	// 				scaleLabel: {
	// 					display: true,
	// 					labelString: options['xAxisLabel']
	// 				}
	// 			}],
	// 			yAxes: [{
	// 				display: true,
	// 				scaleLabel: {
	// 					display: true,
	// 					labelString: options['yAxisLabel']
	// 				}
	// 			}]
	// 		},
    //         legend: {
    //             display: false
    //         }
    //     }
    // });
