
var raw_data = [];

// render_data = raw_data;
var start_date; // = getFirstDate(raw_data); // = new Date();
var end_date; // = getLastDate(raw_data); // = raw_data Date();


/*
    This function gets called with window.onload and populates the dropdowns
    with options. Consider calling this whenever new data is added to the database.
*/
function renderSelects() {
    // var id_options = $.unique(raw_data.map(function (d) {return d.project_id}));
    var id_options = [];
    $.each(raw_data, function(i, el) {
        if($.inArray(el.project_id, id_options) === -1) id_options.push(el.project_id);
    });
    $('#project_id').append(
        $.map(id_options, function(item, index) {
            return '<option value="' + item + '">' + item + '</option>';
        }).join());

    // id_options = $.unique(raw_data.map(function (d) {return d.sensor_id}));
    // $('#project_id').append(
    //     $.map(id_options, function(item, index) {
    //         return '<option value="' + item + '">' + item + '</option>';

    var type_options = $.unique(raw_data.map(function (d) {return d.data_type}));
    $('#data_type').append(
        $.map(type_options, function(item, index) {
            return '<option value="' + item + '">' + item + '</option>';
        }).join());      
}


/*
    Fill the HTML table with the data set as determined by filterData

    Add a feature for users to choose timestamp format
*/
function renderTable(set_dates=false) {
    var timestamp;

    render_data = filterData(set_dates);

    $('#table-content').html(
        $.map(render_data, function(item, index) {
            if($('#exp_time').prop('checked')) {
                time = item.timestamp.format('x')/1000;
            } else {
                time = item.timestamp.format('MMMM Do YYYY, h:mm:ss a');
            }
            return '<tr><td>' + item.project_id + '</td><td>' + time + '</td><td>' + item.value + '</td><td>' + item.data_type + '</td></tr>';
        }).join());

    // var sensor_options = $.unique(render_data.map(function (d) {return d.sensor_id}));
    // $('#sensor_id').append(
    //     $.map(type_options, function(item, index) {
    //         return '<input type="checkbox" value="Sensor ' + item + '"><label>Sensor ' + item + '</label><br>';
    //     }).join()); 
    console.log("done rendering table");
}

/*
    Start with the set of all data and only keep data points that match the 
    options selected with the dropdowns. When the argument set_dates is passed
    as true this function calls autoSetDates to find the first and last date 
    in the new data set (stored in render_data). If the start and end dates 
    have already been set    
*/
function filterData(set_dates=false) {
    var render_data = raw_data;

    // filter by project ID
    var filter_id = document.getElementById("project_id").value;
    if (filter_id != "Select Project ID" && filter_id != "") {
        render_data = render_data.filter(function (el) {
                return el.project_id == filter_id;
            });
    }
    
    // filter by data type
    var filter_type = document.getElementById("data_type").value;
    if (filter_type != "Select Data Type" && filter_type != "") {
        render_data = render_data.filter(function (el) { // var filter_by_id = 
                return el.data_type == filter_type;
            });
    }

    if(set_dates) {
        _autoSetDates(render_data);
    }

    // filter by date
    if(!$('#exp_time').prop('checked') && start_date && end_date) {
        render_data = render_data.filter(function (el) {  //filterDate(render_data);
            timestamp = moment(el.timestamp);
            return (timestamp.isAfter(start_date-1) && timestamp.isBefore(end_date+1));
        });
    }

    return render_data;
}


/* 
    Find the earliest timestamp in a data set.
*/
function _getFirstDate(data_array) {
    var first_date = moment(data_array[0].timestamp);
    for(i=1; i<data_array.length; i++) {
        if(moment(data_array[i].timestamp).isBefore(first_date)) {
            first_date = moment(data_array[i].timestamp);
        }
    }
    return first_date;
}


/* 
    Find the last timestamp in a data set.
*/
function _getLastDate(data_array) {
    var last_date = moment(data_array[0].timestamp);
    for(i=1; i<data_array.length; i++) {
        if(moment(data_array[i].timestamp).isAfter(last_date)) {
            last_date = moment(data_array[i].timestamp);
        }
    }
    return last_date;
}

/*
    Set the start_date and end_date variables with the first and last dates
    in the data set. Usually this gets called after the data has already been
    filtered based on the dropdown options
*/
function _autoSetDates(render_data) {
    start_date = _getFirstDate(render_data);
    end_date = _getLastDate(render_data);
    $('#datepicker span').html(start_date.format('MMMM D, YYYY') + ' - ' + end_date.format('MMMM D, YYYY'));
}

function _showMetaForm(data_types) {
    if(raw_data[0].timestamp == 0) {
        // if timestamps start at 0 find a start time such that the last sample was just taken
        var end_time = raw_data[raw_data.length -1].timestamp;
        $('#start-date').val(moment().subtract(end_time.format('X'), 'seconds').format('YYYY-MM-DD'));
        $('#start-time').val(moment().subtract(end_time.format('X'), 'seconds').format('HH:mm'));
    } else {
        $('#start-date').val(raw_data[0].timestamp.format('YYYY-MM-DD'));   
        $('#start-time').val(raw_data[0].timestamp.format('HH:mm'));    
    }

    $('#data-types').append(
        $.map(data_types, function(item) {
            return "<p>" + item + ": <input type='text' class='type-change' id='" + item + "' placeholder='" + item + "' />";
        }).join());
    // $.map(data_types, function(item) {
    //     $('#' + item).focusout(_changeType);
    // });

    var path_parts = $('#file-select').val().split('\\');
    var file_name = path_parts[path_parts.length-1];

    $('#project-name').val(file_name.split('.')[0]);

    $('#meta-form').show();
}

function _changeType() {
    var og_type = $(this).attr('id');
    var new_type = $(this).val();
    console.log('replacing type ' + og_type + ' with ' + new_type);
}

function changeTypes() {
    var change_types = [];
    $.map($('.type-change'), function(item) {
        if(item && item.value != "" && item.value != item.id)
            console.log('replace ' + item.id + ' with ' + item.value);
            change_types.push([item.id, item.value]);
    });

    $.map(raw_data, function(item) {
        $.map(change_types, function(pair) {
            if(item.data_type == pair[0])
                item.data_type = pair[1];
        });
    });
    renderTable();
}

/* 
    Configure the datarangepicker object using start_date and end_date
    This variables can be set manually or by calling autoSetDates()
    date range picker config from www.daterangepicker.com 
*/
$(function() {
    var start = moment().subtract(29, 'days'); //start_date; 
    var end = moment(); // end_date;

    function cb(start, end) {
        $('#datepicker span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        // console.log("A new date range was chosen: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
        // filterDate(start, end);
        start_date = start;
        end_date = end;
        renderTable();
    }

    $('#datepicker').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);
});

$('#ev3_data').click(function() {
    if(!$('#exp_time').prop('checked') && $(this).prop('checked')) 
        $('#exp_time').click();
})

$('#exp_time').click(function() {
    if($(this).prop('checked')) {
        $('#time').html("Time (s)");
    } else {
        $('#time').html("Timestamp");
    }
});

/* Parse .csv files using PapaParse
    Import a local file, check its contents, and add them to raw_data
    Full doc at: https://www.papaparse.com/docs
*/
$('#submit').click(function() {
    var config = buildConfig();
    if (!$('#file-select')[0].files.length)
    {
        alert("Please choose at least one file to parse.");
        return;
    }

    $('#file-select').parse({
        config: config,
        //     // base config to use for each file
        // },
        before: function(file, inputElem)
        {
            // executed before parsing each file begins;
            // what you return here controls the flow
        },
        error: function(err, file, inputElem, reason)
        {
            // alert('error parsing file');
            // executed if an error occurs while loading the file,
            // or if before callback aborted for some reason
        },
        complete: function()
        {
            // alert('parsing file complete!');
            // executed after all files are complete
        }
    });
    // var results = Papa.parse()
});

$('#clear').click(function() {
    raw_data = [];
    renderTable();
    $('#data-types').html('Rename Data Types?');
    $('#meta-form').hide();
});

$('#upload').click(function() {
    if(moment.isMoment(raw_data[0].timestamp)) {
        $.map(raw_data, function(item, index) {
            item.timestamp = item.timestamp.format();
        });
    }
    $.ajax(POST_DATA_URL, {
        dataType: 'text',
        data: JSON.stringify(raw_data),
        contentType: 'application/json',
        type: 'POST',
        processData: false,
        success: function( data, textStatus, jQxhr ){
            alert(data);
        },
        error: function( jqXhr, textStatus, errorThrown ){
            console.log( errorThrown );
        }
    });
});

function buildConfig() {
    return {
        // delimiter: $('#delimiter').val(),
        header: true,
        // dynamicTyping: $('#dynamicTyping').prop('checked'),
        skipEmptyLines: true,
        // preview: parseInt($('#preview').val() || 0),
        // step: $('#stream').prop('checked') ? stepFn : undefined,
        // encoding: $('#encoding').val(),
        // worker: $('#worker').prop('checked'),
        // comments: $('#comments').val(),
        complete: completeFn,
        // error: errorFn,
        download: true
    };
}

function completeFn(results, next_id) {
    // var end = now();
    var data_types = [];
    if($('#no_nan').prop('checked')) {
        _deleteNan(results);
    }

    if($('#ev3_data').prop('checked')) {
        data_types = _parseEv3(results);
    } else {
        data_types = _parseDDS(results);
    }

    if (results && results.errors) {
        if (results.errors)
        {
            errorCount = results.errors.length;
            firstError = results.errors[0];
        }
        if (results.data && results.data.length > 0)
            rowCount = results.data.length;
    }
    if(raw_data[0].project_id == undefined)
        _getNextID();

    console.log("Parse complete");
    console.log("    Results:", results);

    _showMetaForm(data_types);

    var set_dates = !$('#exp_time').prop('checked');
    renderTable(set_dates);
}

function _deleteNan(results) {
    var nan_keys = [];
    $.map(results.data, function(item, index) {
        for(key in item) {
            if(item[key] == "NaN") {
                delete item[key]; 
                if(!nan_keys.includes(key)){
                    nan_keys.push(key);
                }
            }
            if(key == "_parsed_extra") {
                delete item[key];
            }
        }
    });
    nan_keys.forEach(function(value) {
        var i =results.meta.fields.indexOf(value); 
        results.meta.fields.splice(i,1);
    });
}

function _parseEv3(results, next_id) {
    var data_types = [];
    var project_id = next_id;//prompt("Please choose a Project ID for this data set","0");
    var sensor_id = 0; // if we start using this field we can prompt("Please choose a Sensor ID for this data set","1");
    var format = '';
    if($('#exp_time').prop('checked')) {
        format = 'X';
    }

    for(let i=1; i < results.meta.fields.length; i++) {
        var type = results.meta.fields[i];
        if(!data_types.includes(type))
            data_types.push(type);
        $.map(results.data, function(item, index) {
            var temp = {};
            temp.timestamp = moment(item["Time"], format);
            temp.value = item[type];
            temp.data_type = type;
            temp.project_id = project_id;
            temp.sensor_id = sensor_id;
            raw_data.push(temp);
            // delete item;
        });
    }

    // $('#project-id').attr('placeholder', next_id + ' (New Project)');
    return data_types;
}

function _parseDDS(results) {
    var format = '';
    var data_types = [];
    if($('#exp_time').prop('checked')) {
        format = 'X';
    }

    $.map(results.data, function(item, index) {
        if(!data_types.includes(item.data_type))
            data_types.push(item.data_type);
        item.project_id = parseInt(item.project_id);
        item.sensor_id = parseInt(item.sensor_id);
        item.timestamp = moment(item.timestamp, format);
        item.value = parseFloat(item.value);
        raw_data.push(item);
        // delete item;
    });
    return data_types;
}

function _getNextID() {
    $.get(GET_ID_URL, function(next_id, textStatus) {
        console.log('next id: ' + next_id);
        $('#project-id').attr('placeholder', next_id + ' (New Project)');
        return next_id;
    });
}

// function errorFn(results) {
//     console.log(errors);
// }

// Document-wide error handling
window.addEventListener('error', function (e) {
  var error = e.error;
  console.log(error);
});
