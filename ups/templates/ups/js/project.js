var log_ready = false;
var SS = "Selected servers: ";
var SU = "Selected updates: ";
//var SS = "";
//var SU = "";


function logs_to_div(div) {
    if (!log_ready) { $(div).load('/logs/{{ project.id }}/{{ key }}/{{ cmd }}/{{ cron }}/{{ date }}/'); }
}

function show_log() {
    setInterval(function() { logs_to_div('.output'); }, 2000);
    $('.project').hide();
    logs_to_div('.output');
}

function show_loader() {
    $('.output_bottom').show();
    $('.project').hide();
    $('.loader').show();
}

function go_up() {
    document.body.scrollTop = 0; // For Chrome, Safari and Opera
    document.documentElement.scrollTop = 0; // For IE and Firefox
}

function go_down() {
    var jump = $(document).height();
    document.body.scrollTop = jump; // For Chrome, Safari and Opera
    document.documentElement.scrollTop = jump; // For IE and Firefox
}

function run_or_cron(check, uncheck) {
    var enable  = document.getElementById(check);
    var disable = document.getElementById(uncheck);
    disable.checked = false
    enable.checked  = true
}

function select_server(box_id, body_id, server_name) {
    var box  = document.getElementById(box_id);
    var body = document.getElementById(body_id);
    if ( box.checked == false ) {
        box.checked =  true;  body.style.background = '#dff0d8';
        SS = SS + '<a onclick=\"select_server(\'' + box_id + '\', \'' + body_id + '\', \'' +
        server_name + '\')\">' + server_name + '</a>, ';
        document.getElementById("SS").innerHTML = SS;
    }
    else {
        box.checked =  false; body.style.background = '';
        SS = SS.replace('<a onclick=\"select_server(\'' + box_id + '\', \'' + body_id + '\', \'' +
        server_name + '\')\">' + server_name + '</a>, ', "");
        document.getElementById("SS").innerHTML = SS;
    }
}

function select_update(box_id, body_id, update_name) {
    var box  = document.getElementById(box_id);
    var body = document.getElementById(body_id);
    if ( box.checked == false ) {
        box.checked =  true;  body.style.background = '#dff0d8';
        SU = SU + '<a onclick=\"select_update(\'' + box_id + '\', \'' + body_id + '\', \'' +
        update_name + '\')\">' + update_name + '</a>, ';
        document.getElementById("SU").innerHTML = SU;
    }
    else {
        box.checked =  false; body.style.background = '';
        SU = SU.replace('<a onclick=\"select_update(\'' + box_id + '\', \'' + body_id + '\', \'' +
        update_name + '\')\">' + update_name + '</a>, ', "");
        document.getElementById("SU").innerHTML = SU;
    }
}

function select_all_servers(box_name, body_name, state) {
    var boxes  = document.getElementsByName(box_name);
    var bodies = document.getElementsByClassName(body_name);
    var color = ''; if ( state == true ) { var color = '#dff0d8'; }
    SS = 'Selected servers: ';
    for (i = 0; i < boxes.length;  i++) {
        data = boxes[i].dataset;
        boxes[i].checked = state;
        bodies[i].style.background = color;
        if ( state == true ) { SS = SS + '<a onclick=\"select_server(\'' + boxes[i].id + '\', \'' +
            bodies[i].id + '\', \'' + data.target + '\')\">' + data.target + '</a>, '; }
        else { SS = ''; }
    }
    document.getElementById("SS").innerHTML = SS;
    SS = "Selected servers: ";
}

function select_all_updates(box_name, body_name, state) {
    var boxes  = document.getElementsByName(box_name);
    var bodies = document.getElementsByClassName(body_name);
    var color = ''; if ( state == true ) { var color = '#dff0d8'; }
    SU = 'Selected updates: ';
    for (i = 0; i < boxes.length;  i++) {
        data = boxes[i].dataset;
        boxes[i].checked = state;
        bodies[i].style.background = color;
        if ( state == true ) { SU = SU + '<a onclick=\"select_update(\'' + boxes[i].id + '\', \'' +
            bodies[i].id + '\', \'' + data.target + '\')\">' + data.target + '</a>, '; }
        else { SU = ''; }
    }
    document.getElementById("SU").innerHTML = SU;
    SU = "Selected updates: ";
}

function setCookie(cname, cvalue) {
    var d = new Date();
    document.cookie = cname + "=" + cvalue;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function Validation(box, srv, upd, job) {

    if (job) {
        var jobs = document.getElementsByName('selected_jobs');
        for (i = 0; i < jobs.length; i++) { if (jobs[i].checked) { var selected_jobs = true; break; }}
        if  (!selected_jobs) { alert('Job(s) not selected.'); return false; }}

    if (upd) {
        var updates = document.getElementsByName('selected_updates');
        for (i = 0; i < updates.length; i++) { if (updates[i].checked) { var selected_updates = true; break; }}
        if  (!selected_updates) { alert('Update(s) not selected.'); return false; }}

    if (srv) {
        var servers = document.getElementsByName('selected_servers');
        for (i = 0; i < servers.length; i++) { if (servers[i].checked) { var selected_servers = true; break; }}
        if  (!selected_servers) { alert('Server(s) not selected.'); return false; }}

    setCookie('scrollmem', window.pageYOffset); show_loader();
    if (box) { document.getElementById(box).checked = true; document.getElementById('selector').submit(); }
}

function restoreScroll() {
    var scroll = getCookie('scrollmem');
    if (scroll > 0) { $('html,body').scrollTop(scroll); };
    setCookie('scrollmem', 0);
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

$(document).ready(function() { $('.loader').hide(); });