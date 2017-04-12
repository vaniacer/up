function run_cron(check, uncheck) {
    var enable  = document.getElementById(check);
    var disable = document.getElementById(uncheck);

    enable.checked = true
    disable.checked = false
}

function checker(box_id, body_id) {
    var box  = document.getElementById(box_id);
    var body = document.getElementById(body_id);
    if   ( box.checked == false )
         { box.checked = true;  body.style.background = '#dff0d8'; }
    else { box.checked = false; body.style.background = '';}
}

function select_all(box_name, body_name, state) {
    var color = ''; if ( state == true ) { var color = '#dff0d8'; }
    var boxes  = document.getElementsByName(box_name);
    var bodies = document.getElementsByClassName(body_name);
    for (i = 0; i < boxes.length;  i++) { boxes[i].checked = state; }
    for (i = 0; i < bodies.length; i++) { bodies[i].style.background = color; }
}

function topFunction() {
    document.body.scrollTop = 0; // For Chrome, Safari and Opera
    document.documentElement.scrollTop = 0; // For IE and Firefox
}

function goBack() {
    history.back();
    hide_loader();
}

function hide_page() {
    $(".whole_page").hide();
    $(".loader").show();
}

function hide_loader() {
    $(".whole_page").show();
    $(".loader").hide();
}

function NameValidation(name) {

    var selected = false;

    var objects =  document.getElementsByName(name);

    for (i = 0; i < objects.length; i++) { if (objects[i].checked) { selected = true; } }

    if (selected == false) {
        alert('None selected.');
        return false;
    }

    hide_page();
}

function SelectValidation() {

    var selected = false;

    var updates =  document.getElementsByName('selected_updates');
    var servers =  document.getElementsByName('selected_servers');

    for (i = 0; i < updates.length; i++) { if (updates[i].checked) { selected = true; } }
    for (i = 0; i < servers.length; i++) { if (servers[i].checked) { selected = true; } }

    if (selected == false) {
        alert('None selected.');
        return false;
    }

    hide_page();
}

function JobValidation() {

    var selected = false;

    var jobs =  document.getElementsByName('selected_jobs');

    for (i = 0; i < jobs.length; i++) { if (jobs[i].checked) { selected = true; } }

    if (selected == false) {
        alert('None selected.');
        return false;
    }

    hide_page();
}

function Validation(box) {

    var cron = document.getElementById('CRON');
    var selected_updates = false;
    var selected_servers = false;

    var updates =  document.getElementsByName('selected_updates');
    var servers =  document.getElementsByName('selected_servers');

    var date =  document.getElementById('selected_date');
    var time =  document.getElementById('selected_time');

    for (i = 0; i < updates.length; i++) { if (updates[i].checked) { selected_updates = true; } }
    for (i = 0; i < servers.length; i++) { if (servers[i].checked) { selected_servers = true; } }

    if (selected_updates == false) {
        alert('Update(s) not selected.');
        return false;
    }

    if (selected_servers == false) {
        alert('Server(s) not selected.');
        return false;
    }

    if (cron.checked) {
        if (date.value) {
             if (!time.value) {
                alert('Time not selected.');
                return false;
             }
        }

        if (time.value) {
            if (!date.value) {
                alert('Date not selected.');
                return false;
            }
        }
    }

    hide_page();
    document.getElementById(box).checked = true;
    document.getElementById('selector').submit();
}

$(function() {
  // Change tab on load
  var hash = window.location.hash;
  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  $('.nav-tabs a').click(function (e) {
    $(this).tab('show');
    var scrollmem = $('body').scrollTop();
    window.location.hash = this.hash;
    $('html,body').scrollTop(scrollmem);
  });

  // Change tab on hashchange
  window.addEventListener('hashchange', function() {
    var changedHash = window.location.hash;
    changedHash && $('ul.nav a[href="' + changedHash + '"]').tab('show');
  }, false);
});

$(document).ready(function() {
    hide_loader();
});

$('.datepicker').datepicker();