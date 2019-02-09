
        /*
            When the page loads for the first time populate the raw_data variable using the Jinja2 
            template for loop. Also find the first and last timestamps in the table and store 
            them in start_date and end_date. These variables will continue to be updated as new 
            data is fetched from the server.
        */
        const URL_STRING = 'https://wmsinh.org/scratchx';
        var raw_data = [];
        var project_names = [];
        // var timestamp_temp;

        var last_pull = moment(); //.subtract(moment().utcOffset(), 'minutes');
        var render_data = raw_data;
        var start_date;// = _getFirstDate(raw_data); // = new Date();
        var end_date;// = _getLastDate(raw_data); // = raw_data Date();

        // pull new data from the server every 5 seconds 
        // save the timestamp of the most recent post for comparison on the server
        // $(function() {
        //     // var since = getLastDate(raw_data).unix();
        //     setInterval(function() {
        //         if(document.getElementById("auto_refresh").checked) {
        //             refreshData();
        //         }
        //     }, 5000);
        // });

        /*
            Refresh data in the table without reloading the page or any controls. 
            This function is triggered by the 'Refresh Data' button
        */
        function refreshData() {//last_pull=last_pull) {
            console.log('last pull: ' + last_pull.format());
            $.ajax("{{ url_for('get_new_data') }}?since=" + last_pull).done(
                function(new_data) {
                    // console.log('get data since ' + last_pull);
                    for (var i = 0; i < new_data.length; i++) {
                        console.log('new timestamp: ' + new_data[i].timestamp);
                        new_data[i].timestamp = moment(new_data[i].timestamp); //_formatTimestamp(moment(new_data[i].timestamp));
                        // console.log(JSON.stringify(new_data[i]));
                        raw_data.unshift(new_data[i]);
                    }
                    last_pull = moment(); //.subtract(moment().utcOffset(), 'minutes');
                    // console.log('new since: ' + last_pull);
                    end_date = last_pull;
                    renderTable(true);
                }
            );
        }

        /*
            This function gets called with window.onload and populates the dropdowns
            with options. Consider calling this whenever new data is added to the database.
        */
        function renderSelects(prefix='') {
            // var id_options = $.unique(raw_data.map(function (d) {return d.project_id}));
            // var id_options = [];
            // var project_names = _getProjectNames();
            // $.each(raw_data, function(i, el) {
            //     if($.inArray(el.project_id, id_options) === -1) id_options.push(el.project_id);
            // });
            // id_options = id_options.sort((a, b) => a - b);

            _resetOptions(prefix + 'project_name');
            $('#' + prefix + 'project_name').append(
                $.map(project_names, function(item, index) {
                    return '<option value="' + item + '">' + item + '</option>';
                }).join());

            var value = $('#' + prefix + 'data_type').val()
            var data_types = $.unique(raw_data.map(function (d) {return d.data_type}));
            _resetOptions(prefix + 'data_type');
            $('#' + prefix + 'data_type').append(
                $.map(data_types, function(item, index) {
                    return '<option value="' + item + '">' + item + '</option>';
                }).join());    
            if(data_types.includes(value)) $('#' + prefix + 'data_type').val(value);     
        }


        /* 
            Render only the data types that exist in the selected project
        */
        function renderDataTypes(prefix='') {
            var project_id = project_names.indexOf($('#' + prefix + 'project_name').val());//document.getElementById(prefix + "project_id").value;
            var render_data = raw_data;
            var data_types = [];

            if (project_id != -1) {//"Select Project ID" && project_id != "") {
                render_data.filter(function (el) {
                    if(el.project_id == project_id && !data_types.includes(el.data_type)) {
                        data_types.push(el.data_type);
                    }
                    // return el.project_id == filter_id;
                });

                var value = $('#' + prefix + 'data_type').val()
                _resetOptions(prefix + 'data_type');
                $('#' + prefix + 'data_type').append(
                    $.map(data_types, function(item, index) {
                        return '<option value="' + item + '">' + item + '</option>';
                    }).join());
                if(data_types.includes(value)) $('#' + prefix + 'data_type').val(value);
            } else {
                renderSelects();
            }

        }
        
        /*
            Fill the HTML table with the data set as determined by filterData
        */
        function renderTable(set_dates=false) {
            render_data = filterData(set_dates);
            renderDataTypes();

            $('#table-content').html(
                $.map(render_data, function(item, index) {
                    return '<tr><td>' + item.project_id + '</td><td>' + item.timestamp.format('MMMM Do YYYY, h:mm:ss a') + '</td><td>' + item.value + '</td><td>' + item.data_type + '</td></tr>';
                }).join());

            renderChart(render_data);
        }

        /*
            Start with the set of all data and only keep data points that match the 
            options selected with the dropdowns. When the argument set_dates is passed
            as true this function calls _autoSetDates to find the first and last date 
            in the new data set (stored in render_data). If the start and end dates 
            have already been set    
        */
        function filterData(set_dates=false) {
            render_data = raw_data;

            // filter by project ID
            var filter_id = project_names.indexOf($('#project_name').val());//document.getElementById("project_name").value;
            if (filter_id != "Select Project ID" && filter_id != -1) {
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
            if(start_date && end_date) {
                render_data = render_data.filter(function (el) {  //filterDate(render_data);
                    // timestamp = el.timestamp;
                    return (el.timestamp.isAfter(start_date-1) && el.timestamp.isBefore(end_date+1));
                });
            }

            return render_data;
        }

        /*
            Toggle the Archive Project form between hidden and visible
        */
        function openForm(form_name) {
            // renderSelects('archive_');
            var show_form = document.getElementById(form_name);
            if(show_form.style.display == "block") {
                show_form.style.display = "none";
                return;
            }

            if(form_name == "cropForm") {
                if($('#project_name').val() == "") {
                    alert('Please select a project to crop');
                    return;
                }
                _fillCropFields();
            } else {
                _resetOptions(form_name + '_project_name');
                $("#" + form_name + "_project_name").append(
                    $.map(project_names, function(item, index) {
                        return '<option value="' + item + '">' + item + '</option>';
                    }).join());
            }
            show_form.style.display = "block";
        }

        /*
            Hide the Archive Project form
        */ 
        function closeForm(form_name) {
            document.getElementById(form_name).style.display = "none";
        }

        /*
            Archive some data so it doesn't appear on this page.
            For now the only option is to archive an entire project, but we could
            add support for archiving individual data sets. When a project has become archived,
            users can continue to add new values to the project and only the new values will appear on the page
        */
        function archiveData() {
            var project_id = project_names.indexOf($('#archiveForm_project_name').val());//document.getElementById('archiveForm_project_id').value;
            if(project_id == -1) {
                alert('Please select a project to archive');
                return;
            }

            var post_data = new FormData();
            post_data.append('project_id', project_id);
            $.ajax({
                url: 'https://wmsinh.org/data-story',
                data: post_data,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function(data){
                    alert(data);
                    closeForm();
                }
            });
        }

        function getMetaData() {
            var project_id = project_names.indexOf($('#metadataForm_project_name').val());//$('#metadataForm_project_id').val();
            if(project_id == -1) {
                return;
            }
            var query_string = URL_STRING + '?project_id=' + String(project_id) + '&pmd=true&data=false';

            $.ajax({
                url: query_string,
                dataType: 'json',
                // processData: false,
                // contentType: false,
                // type: 'GET',
                success: function(data) {
                    console.log(JSON.stringify(data));
                    $('#edit_project_name').val(data.name);
                    $('#project_description').val(data.description);
                    $('#project_miscellaneous').val(data.miscellaneous);
                }
            });
        }

        /*
            Edit metadata for a project in the database.
        */
        function editMetadata() {
            var edit_data = new FormData();
            var project_id = $('#metadataForm_project_id').val();
            if(project_id == '') {
                alert('Please select a project to edit');
                return;
            }

            edit_data.append('project_id', project_id);
            if($("#project_name").val() != "")
                    edit_data.append('name', $('#project_name').val());
            if($("#project_description").val() != "")
                    edit_data.append('description', $('#project_description').val());
            if($("#project_miscellaneous").val() != "")
                    edit_data.append('miscellaneous', $('#project_miscellaneous').val());
            edit_data.append('pmd', true);

            $.ajax({
                url: URL_STRING,
                data: edit_data,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function(data){
                    alert(data);
                    closeForm('metadataForm');
                }
            });
        }

        function cropProject() {
            crop_project = new FormData();
            // if($('#crop_project_name').val())
            crop_project.append('name', $('#crop_project_name').val());
            crop_project.append('desc', $('#crop_project_description').val());
            crop_project.append('misc', $('#crop_project_miscellaneous').val());
            crop_project.append('data', JSON.stringify(filterData()))

            $.ajax({
                url: URL_STRING,
                data: crop_project,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function(data){
                    alert(data);
                    closeForm('cropForm');
                }
            });
        }

        function _fillCropFields() {
            var og_name = $('#project_name').val();
            var project_id = project_names.indexOf(og_name);
            var crop_type = $('#data_type').val();
            var crop_string = 'Cropped project ' + og_name;
            $('#crop_project_name').val(crop_string)

            if(crop_type != "")
                crop_string += ' with data type ' + crop_type;

            crop_string += ' starting on ' + start_date.format('YYYY-MM-DD') + ' at ' + start_date.format('HH:mm');
            crop_string += ' and ending on ' + end_date.format('YYYY-MM-DD') + ' at ' + end_date.format('HH:mm');

            $('#cropForm_project_name').append(og_name);
            $('#crop_project_description').val('Cropped View of project ' + og_name + ' taken on ' + moment().format('YYYY-MM-DD'));
            $('#crop_project_miscellaneous').val(crop_string);
        }

        /*
            Show or hide the chart based on user input
        */
        function showChart() {
            // console.log('setting view to ' + $('#show-chart').is(":checked"));
            // if($('#show-chart').is(":checked")) {
            if($('#chart-container').css('display') == 'none') {
                $('#chart-container').show();
                $('#show-chart').html('Hide Chart');
                resizeChart();
            } else {
                $('#chart-container').hide();
                $('#show-chart').html('Show Chart');
            }
            console.log('setting view to ' + $('#chart-container').css("display"));
        }

        /* 
            re-size the chart based on user input
        */
        function resizeChart() {
            var width = $('#chart-width').val();
            var height = width;//*.67;//$('#chart-height').val();

            $('#chart-container').css('width', width + 'vw');
            $('#chart-container').css('height', height + 'vh');
            renderChart();
        }

        /*
            set start and end date times based on use input
        */
        function setTimes() {
            start_date.hour($('#start-time').val().split(':')[0]);
            start_date.minute($('#start-time').val().split(':')[1]);
            end_date.hour($('#end-time').val().split(':')[0]);
            end_date.minute($('#end-time').val().split(':')[1]);
            renderTable();
        }

        /*
            Get a list of all project names from the database
        */
        function _getProjectNames() {
            var query_string = URL_STRING + '?project_names=true';

            $.ajax({
                url: query_string,
                dataType: 'json',
                // processData: false,
                // contentType: false,
                // type: 'GET',
                success: function(data) {
                    console.log('project_names: ' + JSON.stringify(data));
                }
            });

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
            Format a timestamp from the database to match the user's timezone
            Still not clear why this needs to be coded explicitly
        */
        function _formatTimestamp(db_timestamp) {
            return db_timestamp.add(moment().utcOffset(), 'minutes');
        }

        /*
            Reset the options for a dropdown menu while keeping the default option the same
        */
        function _resetOptions(id) {
            var default_option = document.getElementById(id).options[0];
            $('#' + id + ' option').remove();
            $('#' + id).append(default_option);
            // var select_options = document.getElementById(id);
            // for(var i=1; i<select_options.options.length; i++) {
            //     select_options.remove(i);
            // }
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
            $('#start-time').val(start_date.format("HH:mm"));
            $('#end-time').val(end_date.format("HH:mm"));
        }

        /* 
            Configure the datarangepicker object using start_date and end_date
            These variables can be set manually or by calling _autoSetDates()
            Ref: www.daterangepicker.com 
        */
        $(function() {
            var start = start_date ? start_date : _getFirstDate(raw_data); //moment().subtract(29, 'days');
            var end = end_date ? end_date : _getLastDate(raw_data); ; //moment();
            $('#start-time').val(start.format("HH:mm"));
            $('#end-time').val(end.format("HH:mm"));

            function cb(start, end) {
                start.hour($('#start-time').val().split(':')[0]);
                start.minute($('#start-time').val().split(':')[1]);
                end.hour($('#end-time').val().split(':')[0]);
                end.minute($('#end-time').val().split(':')[1]);
                $('#datepicker span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                console.log("A new date range was chosen: " + start.format('YYYY-MM-DD HH:mm') + ' to ' + end.format('YYYY-MM-DD HH:mm'));
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

    /*
        
    */
    $('#csv-action').click(function() {
        var config = buildConfig();
        // var print_data = render_data; 
        if($('#csv-action').html().split(' ')[0] == 'Import') {
            console.log('import file');
            var contents = Papa.parse($('#file-select').prop('files')[0], {
                complete: function(results) {
                    console.log(results);
                    return results;
                }
            });
            return;
        }   
        $.map(render_data, function(item, index) {
            item.timestamp = item.timestamp.format();
        });
        var csv = Papa.unparse(render_data);
        $.map(render_data, function(item, index) {
            item.timestamp = moment(item.timestamp);
        });
        // console.log("Results: ", csv);
        
        if (!csv.match(/^data:text\/csv/i)) {
            csv = 'data:text/csv;charset=utf-8,' + csv;
        }
        var data = encodeURI(csv);

        var link = document.createElement('a');
        link.setAttribute('href', data);
        link.setAttribute('download', 'export.csv');
        link.click();
    });

    $('#file-select').change(function() {
        var button_text = $('#csv-action').val();
        var file_val = $('#file-select').val();
        console.log('focus out with file val ' + file_val);
        if(file_val != "" && button_text != "Import .csv File")
            $('#csv-action').html("Import .csv File");
        else if(file_val == "" && button_text != "Export .csv File")
            $('#csv-action').html("Export .csv File");
    });

    /* Config and callback function for export CSV Parse */
    function buildConfig() {
        return {
            // delimiter: $('#delimiter').val(),
            // header: $('#header').prop('checked'),
            // dynamicTyping: $('#dynamicTyping').prop('checked'),
            // skipEmptyLines: $('#skipEmptyLines').prop('checked'),
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

    function completeFn(results) {
        // var end = now();

        if (results && results.errors)
        {
            if (results.errors)
            {
                errorCount = results.errors.length;
                firstError = results.errors[0];
            }
            if (results.data && results.data.length > 0)
                rowCount = results.data.length;
        }

        console.log("Parse complete");
        console.log("    Results:", results);

        // icky hack
        // setTimeout(enableButton, 100);
    }

// socketio uses websocket, which is not supported by apache
// if we reach the point of requiring immediate server updates
// we could look into implementing this

        // var socket = io.connect('https://' + document.domain + ':' + location.port);
        // console.log('socket at https://' + document.domain + ':' + location.port);
        // socket.on('connect', function() {
        //     socket.emit('my event', {data: 'I\'m connected!'});
        //     console.log('socket connected');
        // });
        // socket.on('test response', function() {
        //     console.log('test response');
        // });
        // socket.on('new value', function(data) {
        //     var new_val = JSON.parse(data);
        //     raw_data.push({
        //         "project_id": new_val.project_id,
        //         "sensor_id": new_val.sensor_id,
        //         "timestamp": moment(new_val.timestamp, "ddd DD-MM-YYYY HH:mm:ss"),
        //         "value": new_val.value,
        //         "data_type": new_val.data_type
        //     });
        //     console.log('new val: ', raw_data[raw_data.length-1]);
        //     renderTable(true);
        //     if(document.getElementById("auto_refresh").checked) {
        //         renderChart();
        //     }
        // });