var log_ready = false;

function load_div(div) {
    if (!log_ready) { $(div).load('/logs/{{ project.id }}/{{ key }}/{{ cmd }}/{{ cron }}/{{ date }}/'); }
}

function show_log() {
    setInterval(function() { load_div('.output'); }, 2000);
    $('.project').hide();
    load_div('.output');
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

function checker(box_id, body_id) {
    var box  = document.getElementById(box_id);
    var body = document.getElementById(body_id);
    if   ( box.checked == false )
         { box.checked =  true;  body.style.background = '#dff0d8'; }
    else { box.checked =  false; body.style.background = ''; }
}

function select_all(box_name, body_name, state) {
    var boxes  = document.getElementsByName(box_name);
    var bodies = document.getElementsByClassName(body_name);
    var color = ''; if ( state == true ) { var color = '#dff0d8'; }
    for (i = 0; i < boxes.length;  i++) { boxes[i].checked = state; }
    for (i = 0; i < bodies.length; i++) { bodies[i].style.background = color; }
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

$(function() {
    // Change tab on load
    var hash = window.location.hash;
    hash && $('ul.nav a[href="' + hash + '"]').tab('show');

    $('.nav-tabs a').click(function (e) {
        $(this).tab('show');
        var scrollmem = $('body').scrollTop();
        window.location.hash = this.hash;
        alert(window.pageYOffset);
        $('html,body').scrollTop(scrollmem);
    });

    // Change tab on hashchange
    window.addEventListener('hashchange', function() {
        var changedHash = window.location.hash;
        changedHash && $('ul.nav a[href="' + changedHash + '"]').tab('show');
    }, false);
});

$(document).ready(function() {
    $('.loader').hide();
    var scroll = getCookie('scrollmem');
    if (scroll > 0) { $('html,body').scrollTop(scroll); };
});