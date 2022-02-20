$(document).ready(function() {
    console.log('PageContext is : ', page_context);
    $.ajaxSetup({ cache: false });
    fillTable();
});

function deleteTask(id, title){
    console.log('Deletion for id ' + id);

    bootbox.confirm('Are you sure to delete task "'+title+'"!', function(result){
        console.log('result is : ' + result);
        if(result === true)
            deleteTaskWithoutConfirmation(id);
    });
    return false;
}

function deleteTaskWithoutConfirmation(id){
    let ajaxObject = {
        url : page_context.taskDeleteApi + id,
        type : 'delete',

        success: function(result) {
            console.log('Task with id ' + id +' has been deleted!', result);
            window.location.href = page_context.taskListPage;
        },
        error : function(xhr,status,error) {
            alert('Url failed with error : ' + xhr.status + ', Description: ' + error);
        }
    };

    $.ajax(ajaxObject);
}


function getColumns(){
    let columns = [{"data": "title"},{"data": "status_str"},{"data": "description"}];
    if(page_context.isUserAuthenticated){
        columns.push({"data": "edit"},{"data": "delete"});
    }
    return columns;
}

function fillTable(){
    $.getJSON(page_context.taskListApi, function(data){
        data = prepareData(data);
        $('#tasklist').DataTable( {
            data: data,
            columns:getColumns(),
        });
    });
}

function prepareData(data){
    console.log('prepareData arg is : ', data);
    if(page_context.isUserAuthenticated){
        for ( var i=0; i < data.length ; i++ ) {
            if(data[i].owner_id == page_context.userId){
                data[i].edit = `<a href="${page_context.taskDetailPage}${data[i].id}"><i class="fas fa-edit"></i></a>`;
                data[i].delete = `<a href="#" onclick="return deleteTask(${data[i].id}, '${data[i].title}')"><i class="fa fa-trash"></i></a>`;
            } else {
                data[i].edit = '<div />';
                data[i].delete = '<div />';
            }
        }
    }
    console.log('prepareData result is : ', data);
    return data;
}

/*
function fillTable(){
    $('#tasklist').DataTable({
        "serverSide": true,
        ajax: {
            url: page_context.taskListApi,
            method: 'GET',
            type: 'GET',
            dataType: 'json',
            data: {
                "contentID": "contentID1"
            },
            dataFilter: function(data) {
                console.log("dataFilter arg is : " + data);
                var jData = JSON.parse(data);
                var json = {};
                json.draw = 1;
                json.data = jData.results;
                json.recordsFiltered = jData.count;
                json.recordsTotal = jData.count;
                var dtData = JSON.stringify(json);
                return dtData;
            },
            "dataSrc": prepareDataWithPagination,
        },
        "columns": getColumns(),
    });
}
function prepareDataWithPagination(json) {
    return prepareData(json.data);
}
*/