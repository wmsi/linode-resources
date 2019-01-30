
/* 
    This script deals with rendering the chart using the chart.js interface.
    This works with an HTML canvas element (defined above) and a set of data stored
    in render_data
*/
const canvas = document.getElementById('chartCanvas');
const ctx = document.getElementById('chartCanvas').getContext('2d');
ctx.fillStyle = 'black';
ctx.fillRect(0, 0, canvas.width, canvas.height);
var myChart;
// window.onload = renderChart();

function renderChart() {
    render_data = filterData();
    // ctx.fillStyle = 'black';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white';
    // if(document.getElementById('project_id').value == "Select Project ID") {
    //     console.log("please choose a project");
    //     ctx.font = "36px Roboto";
    //     ctx.fillText("Please select a Project ID",10,50);
    //     ctx.fillText(" to render a chart",10,90);
    //     return;
    // }
    if(!singleType(render_data)) {
        ctx.font = "36px Roboto";
        ctx.fillText("Please select a single Data Type",10,50);
        ctx.fillText(" to render a chart",10,90);
        return;
    }

    // add data type error handling here

    // The list of line colors defines the order of colors in which lines
    // will be plotted on the chart
    const line_colors = ['#F15854', '#5DA5DA', '#DECF3F', '#B276B2', '#B2912F', '#F17CB0', '#60BD68', '#FAA43A', '#4D4D4D'];
    var y_label = render_data[0].data_type;
    var chart_projects = [];
    var data = {
        labels: [],
        // labels: [new Date(getFirstDate(test_data)), new Date(getLastDate(test_data))],
        datasets: [],
    }

    render_data.map(function(item) {
        if(!chart_projects.includes(item.project_id)) {
            var index = chart_projects.length;
            chart_projects.push(item.project_id);
            data.labels.push(new Date(item.timestamp));
            data.datasets.push({
                fill: false,
                label: item.data_type + " from Project " + item.project_id,
                data: [item.value],
                borderColor: line_colors[index],
                backgroundColor: line_colors[index],
                lineTension: 0,
            });
        } else {
            var index = chart_projects.indexOf(item.project_id);
            data.labels.push(new Date(item.timestamp));
            data.datasets[index].data.push(item.value);
        }
    });

    var options = {
        maintainAspectRatio: false,
        type: 'line',
        data: data,
        options: {
            fill: false,
            responsive: true,
            scales: {
                xAxes: [{
                    type: 'time',
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: "Date",
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: false,
                    },
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: y_label,
                    }
                }]
            }
        }
    }
    if(myChart) {
        console.log("updating chart");
        myChart.data.labels = data.labels;
        $.map(data.datasets, function(ds, i) {
            myChart.data.datasets[i] = ds;
        });
        for(var i=data.datasets.length; i < myChart.data.datasets.length; i++) {
            myChart.data.datasets.splice(i, 1);
        }
        myChart.update();
    } else {
        myChart = new Chart(ctx, options);
    }
}

function singleType(data) {
    var type = data[0].data_type;
    for(var i in data) {
        if(data[i].data_type != type) {
            return false;
        }
    }
    return true;
}
