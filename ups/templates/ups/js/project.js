function color(body_id, ec, cron) {
    var body = document.getElementById(body_id);
    if (cron  ) { body.classList.add('cron');   }
    if (ec > 0) {
        body.classList.remove('cron');
        body.classList.add('danger');
    }
    else if (cron == 'False') { body.classList.remove('cron'); }
    else if (cron == 'True' ) { body.classList.add('cron');    }
}

function show_loader() {
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

function run_or_cron(type) {
    $('#run_type').val(type);
}

function selector(box_id, body_id, name, obj) {
    var body = document.getElementById(body_id);
    var box  = document.getElementById(box_id);
	var div = document.getElementById(obj);
    var txt = '<a title=\"Deselect ' + name + '\" href=\"javascript:;\" onclick=\"selector(\''
        + box_id + '\', \'' + body_id + '\', \'' + name + '\', \''+ obj + '\')\">' + name + '</a> | '

    function change(list) {
        if ( box.checked == false ) {
            box.checked = true; body.classList.add('selected');
            window[list] = window[list] + txt;
            div.innerHTML = window[list];
        }
        else {
            box.checked = false; body.classList.remove('selected');
            window[list] = window[list].replace(txt, '');

            if ( window[list] == pref ) { div.innerHTML = ''; }
            else { div.innerHTML = window[list]; }
        }
    }

	if      ( obj == 'SS' ) { pref = 'Selected servers: '; window.slist = window.slist || pref; change('slist'); }
	else if ( obj == 'SU' ) { pref = 'Selected updates: '; window.ulist = window.ulist || pref; change('ulist'); }
	else if ( obj == 'SX' ) { pref = 'Selected scripts: '; window.xlist = window.xlist || pref; change('xlist'); }
	else if ( obj == 'SD' ) { pref = 'Selected dumps: ';   window.dlist = window.dlist || pref; change('dlist'); }
	else if ( obj == 'SJ' ) { pref = 'Selected jobs: ';    window.jlist = window.jlist || pref; change('jlist'); }
}

function select_all(box_name, body_name, state, obj) {
    var boxes  = document.getElementsByName(box_name);
    var bodies = document.getElementsByClassName(body_name);

    for (i = 0; i < boxes.length;  i++) {
        data = boxes[i].dataset;
        if ( boxes[i].checked != state ) { selector(boxes[i].id, bodies[i].id, data.target, obj); }
    }
}

function Validation(cmd, srv, upd, job, scr, dmp, dgr) {

    var server_names = '';

    if (job) {
        var jobs = document.getElementsByName('selected_jobs');
        for (i = 0; i < jobs.length; i++) { if (jobs[i].checked) { var selected_jobs = true; break; }}
        if  (!selected_jobs) { alert('Job(s) not selected.'); return false; }}

    if (scr) {
        var updates = document.getElementsByName('selected_scripts');
        for (i = 0; i < updates.length; i++) { if (updates[i].checked) { var selected_updates = true; break; }}
        if  (!selected_updates) { alert('Script(s) not selected.'); return false; }}

    if (upd) {
        var updates = document.getElementsByName('selected_updates');
        for (i = 0; i < updates.length; i++) { if (updates[i].checked) { var selected_updates = true; break; }}
        if  (!selected_updates) { alert('Update(s) not selected.'); return false; }}

    if (dmp) {
        var dumps = document.getElementsByName('selected_dumps');
        for (i = 0; i < dumps.length; i++) { if (dumps[i].checked) { var selected_dumps = true; break; }}
        if  (!selected_dumps) { alert('Dump(s) not selected.'); return false; }}

    if (srv) {
        var servers = document.getElementsByName('selected_servers');
        for (i = 0; i < servers.length; i++) {
            data = servers[i].dataset;
            if (servers[i].checked) {
                var selected_servers = true;
                server_names = '\n\t' + data.target + server_names;
            }
        }
        if  (!selected_servers) { alert('Server(s) not selected.'); return false; }}

    if (dgr) {
        var sure = confirm(
            '\nYou are trying to run command:\n\t'
                + cmd +
            '\n\nOn server(s): '
                + server_names +
            '\n\nAre you sure?'
        );
        if (! sure) { return false; }
    }

    show_loader();
    if (cmd) { $('#selected_command').val(cmd); document.getElementById('selector').submit(); }
}

function select_server(server) {
    $('#selected_command').val('');
    $('#id_servers').val(server);
    $('#selector').submit();
}

function hide_info(id, panel, hb, sb) {
    $(panel).hide(); $(hb).hide(); $(sb).show();
    document.getElementById(id).checked = false
};

function show_info(id, panel, hb, sb) {
    $(panel).show(); $(hb).hide(); $(sb).show();
    document.getElementById(id).checked = true
};

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
    $('#run_type').val('')
    $('#selected_command').val('')
    select_all('selected_servers', 'server-body', false, 'SS');
    select_all('selected_updates', 'update-body', false, 'SU');
    select_all('selected_scripts', 'script-body', false, 'SX');
    select_all('selected_dumps',   'dump-body',   false, 'SD');
    select_all('selected_jobs',    'job-body',    false, 'SJ');

    if (document.getElementById('id_server_info').checked) {
           show_info('id_server_info', '.server-panel', '.sshow', '.shide'); }
    else { hide_info('id_server_info', '.server-panel', '.shide', '.sshow'); }

    if (document.getElementById('id_script_info').checked) {
           show_info('id_script_info', '.script-panel', '.xshow', '.xhide'); }
    else { hide_info('id_script_info', '.script-panel', '.xhide', '.xshow'); }

    if (document.getElementById('id_update_info').checked) {
           show_info('id_update_info', '.update-panel', '.ushow', '.uhide'); }
    else { hide_info('id_update_info', '.update-panel', '.uhide', '.ushow'); }

    if (document.getElementById('id_dbdump_info').checked) {
           show_info('id_dbdump_info', '.dbdump-panel', '.dshow', '.dhide'); }
    else { hide_info('id_dbdump_info', '.dbdump-panel', '.dhide', '.dshow'); }
});