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
    var cron_button = document.getElementById('CRON_BUTTON');
    var run_type = document.getElementById('run_type');
    var current_run_type = run_type.value;

    function color_button(cron) {
        if (cron == 'CRON') {
            cron_button.classList.remove('btn-default');
            cron_button.classList.add('btn-danger');
        } else {
            cron_button.classList.add('btn-default');
            cron_button.classList.remove('btn-danger');
        }
    }

    if (type) {
        run_type.value = type;
    } else {
        if (current_run_type == '')     { run_type.value = 'CRON'; color_button('CRON'); }
        if (current_run_type == 'RUN')  { run_type.value = 'CRON'; color_button('CRON'); }
        if (current_run_type == 'CRON') { run_type.value = 'RUN';  color_button('RUN');  }
    }
}

function show_or_hide_this(btn_id, pnl_id) {
    var btn = document.getElementById(btn_id);
    var pnl = document.getElementById(pnl_id);

    function show_info() {
        btn.classList.remove('glyphicon-menu-down');
        btn.classList.add('glyphicon-menu-up');
        pnl.classList.remove('hidden');
    }

    function hide_info() {
        btn.classList.remove('glyphicon-menu-up');
        btn.classList.add('glyphicon-menu-down');
        pnl.classList.add('hidden');
    }

    if (btn.classList.contains('glyphicon-menu-down')) { show_info(); } else { hide_info(); }
}

function show_or_hide_all(id, panel, button, set) {

    var pluses = document.getElementsByClassName(button);
    var panels = document.getElementsByClassName(panel);
    var button = document.getElementById(button);
    var status = document.getElementById(id);

    function show_info() {
        if (status) { status.checked = true; }
        if (button) { button.value = 'Info On'; }
        for (i = 0; i < panels.length; i++) { panels[i].classList.remove('hidden'); }
        for (i = 0; i < pluses.length; i++) {
            pluses[i].classList.add('glyphicon-menu-up');
            pluses[i].classList.remove('glyphicon-menu-down');
        }
    }

    function hide_info() {
        if (status) { status.checked = false; }
        if (button) { button.value = 'Info Off'; }
        for (i = 0; i < panels.length; i++) { panels[i].classList.add('hidden'); }
        for (i = 0; i < pluses.length; i++) {
            pluses[i].classList.add('glyphicon-menu-down');
            pluses[i].classList.remove('glyphicon-menu-up');
        }
    }

    if (set == 'show') { show_info(); }
    if (set == 'hide') { hide_info(); }
    if (!set) {
        if (status.checked) {
            hide_info();
        } else {
            show_info();
        }
    }
}

//function show_or_hide_this(box_id, panel_id) {
//    var box = document.getElementById(box_id);
//    var panel = document.getElementById(panel_id);
//
//    if (box.checked) { panel.classList.remove('hidden'); } else { panel.classList.add('hidden'); }
//}
//
//function show_or_hide_all(id, panel, button, set) {
//
//    var cboxes = document.getElementsByClassName(button);
//    var panels = document.getElementsByClassName(panel);
//    var button = document.getElementById(button);
//    var status = document.getElementById(id);
//
//    function show_info() {
//        if (status) { status.checked = true; }
//        if (button) { button.value = 'Info On'; }
//        for (i = 0; i < cboxes.length; i++) { cboxes[i].checked = true; }
//        for (i = 0; i < panels.length; i++) { panels[i].classList.remove('hidden'); }
//    }
//
//    function hide_info() {
//        if (status) { status.checked = false; }
//        if (button) { button.value = 'Info Off'; }
//        for (i = 0; i < cboxes.length; i++) { cboxes[i].checked = false; }
//        for (i = 0; i < panels.length; i++) { panels[i].classList.add('hidden'); }
//    }
//
//    if (set == 'show') { show_info(); }
//    if (set == 'hide') { hide_info(); }
//    if (!set) {
//        if (status.checked) {
//            hide_info();
//        } else {
//            show_info();
//        }
//    }
//}

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
    if (cmd) {
        document.getElementById('selected_command').value = cmd;
        document.getElementById('selector').submit();
    }
}

function filter_by(id, value) {
    document.getElementById('selected_command').value = '';
    document.getElementById(id).value = value;
    document.getElementById('selector').submit();
}

$(function() {

    var selected_command = document.getElementById('selected_command');
    if (selected_command) { selected_command.value = ''; }

    // Change tab on load
    var hash = window.location.hash;
    var tabs = document.getElementById('id_tab');
    if (tabs) { if (tabs.value) { hash = '#' + tabs.value; } }
    hash && $('ul.nav a[href="' + hash + '"]').tab('show');

    function servers(hash) {
        show_or_hide_all('dummy', 'servers_tab', 'dummy', 'hide');
        if (tabs) {tabs.value = hash.replace('#', '');}
        if (hash == '#scripts' || hash == '#updates' || hash == '#dumps' || hash == '') {
            show_or_hide_all('dummy', 'servers_tab', 'dummy', 'show');
        }
    }

    // Change tab on click
    $('.nav-tabs a').click(function() {
        $(this).tab('show');
        window.location.hash = this.hash;
        servers(hash);
        go_up();
    });

    // Change tab on hashchange
    window.addEventListener('hashchange', function() {
        var changedHash = window.location.hash;
        changedHash && $('ul.nav a[href="' + changedHash + '"]').tab('show');
        servers(changedHash);
        go_up();
    }, false);

    servers(hash);
});

$(document).ready(function() {

    go_up();
    if (document.getElementById('id_server_info')) {
        if (document.getElementById('id_server_info').checked) {
               show_or_hide_all('id_server_info', 'server-panel', 'sshow', 'show'); }
        else { show_or_hide_all('id_server_info', 'server-panel', 'sshow', 'hide'); }

        if (document.getElementById('id_script_info').checked) {
               show_or_hide_all('id_script_info', 'script-panel', 'xshow', 'show'); }
        else { show_or_hide_all('id_script_info', 'script-panel', 'xshow', 'hide'); }

        if (document.getElementById('id_update_info').checked) {
               show_or_hide_all('id_update_info', 'update-panel', 'ushow', 'show'); }
        else { show_or_hide_all('id_update_info', 'update-panel', 'ushow', 'hide'); }

        if (document.getElementById('id_dbdump_info').checked) {
               show_or_hide_all('id_dbdump_info', 'dbdump-panel', 'dshow', 'show'); }
        else { show_or_hide_all('id_dbdump_info', 'dbdump-panel', 'dshow', 'hide'); }
    }
});