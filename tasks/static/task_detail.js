$(document).ready(function() {
    $.ajaxSetup({ cache: false });
    console.log('page_context', page_context);
    if(page_context.pk){
        $("#updateButton").show();
        $("#updateButton").click(update);
        $("#createButton").hide();
        fetchTask();
    } else {
        $("#createButton").show();
        $("#createButton").click(create);
        $("#updateButton").hide();
    }
});



function fetchTask() {
    console.log('Requesting JSON');
    $.getJSON(page_context.taskRetrieveApi, function(task){
        page_context.task = task;
        fillPage(task);
    });
}

function update(){
    console.log('Update is running...');
    let task = makeTaskObjectFromUi();
    task.id = page_context.task.id;
    let ajaxObject = makeAjaxObjectForUpdate(task);
    $.ajax(ajaxObject);
    return false;
}

function makeAjaxObjectForUpdate(task){
    let ajaxObject = makeAjaxObject(task);
    ajaxObject.url = page_context.taskUpdateApi;
    ajaxObject.method = 'PUT';
    return ajaxObject;
}

function create(){
    console.log('Creation is running...');
    let task = makeTaskObjectFromUi();
    let ajaxObject = makeAjaxObjectForCreate(task);
    $.ajax(ajaxObject);
    return false;
}

function makeAjaxObjectForCreate(task){
    let ajaxObject = makeAjaxObject(task);
    ajaxObject.url = page_context.taskCreateApi;
    ajaxObject.method = 'POST';
    return ajaxObject;
}

function makeAjaxObject(task){
    let ajaxObject = {
        data: JSON.stringify(task),
        contentType: "application/json",
        dataType: "json",
        success: successSubmission,
        error : ajaxFailed
    };
    console.log('Ajax object is : ', ajaxObject);
    return ajaxObject;
}

function successSubmission(result) {
    console.log('Update was successful and result is : ', result);
    window.location.href = page_context.taskListPage;
}

function ajaxFailed(xhr,status,error) {
    alert('Create failed with error : ' + xhr.status + ', Description: ' + error);
    console.log("xhr is : ", xhr);
}

function fillPage(task){
    console.log('JSON', task);
    $('#title').val(task.title);
    $('#status').val(task.status);
    $('#description').val(task.description);
}

function makeTaskObjectFromUi(){
    let task = {
        'title' : $('#title').val(),
        'status' : $('#status').val(),
        'description' : $('#description').val()
    }
    console.log('Task from ui is :', task);
    return task;
}