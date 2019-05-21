function copy_to_clipboard(id) {
  /* Get the text field */
  var copyText = document.getElementById(id);

  /* Select the text field */
  copyText.select();

  /* Copy the text inside the text field */
  document.execCommand("copy");
}

function show_loader() {
    document.getElementById('project-body').classList.add('hidden');
    document.getElementById('loader-max').classList.remove('hidden');
}

function go_up() {
    var tabs = document.getElementById('id_tab');
    if (tabs) {
        var active_tab = document.getElementById(tabs.value + '_roller');
        var server_tab = document.getElementById('servers_roller');
        active_tab.scrollTop = 0;
        server_tab.scrollTop = 0;
    }

    document.body.scrollTop = 0;
}

function go_down() {
    var tabs = document.getElementById('id_tab');
    var jump = document.body.scrollHeight;
    if (tabs) {
        var active_tab = document.getElementById(tabs.value + '_roller');
        var server_tab = document.getElementById('servers_roller');
        active_tab.scrollTop = active_tab.scrollHeight;
        server_tab.scrollTop = server_tab.scrollHeight;
    }

    document.body.scrollTop = jump;
}

function run_or_cron(type) {
    var cron_button = document.getElementById('CRON_BUTTON');
    var run_type = document.getElementById('run_type');
    var current_run_type = run_type.value;

    function color_button(cron) {
        if (cron == 'CRON') {
            cron_button.classList.add('btn-danger');
        } else {
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

    var pluses = Array.from(document.getElementsByClassName(button));
    var panels = Array.from(document.getElementsByClassName(panel));
    var button = document.getElementById(button);
    var status = document.getElementById(id);

    function show_info() {
        if (status) { status.checked = true; }
        if (button) { button.value = 'Hide'; }

        panels.forEach( function(item) { item.classList.remove('hidden'); });
        pluses.forEach( function(item) {
            item.classList.add('glyphicon-menu-up');
            item.classList.remove('glyphicon-menu-down');
        });
    }

    function hide_info() {
        if (status) { status.checked = false; }
        if (button) { button.value = 'Show'; }

        panels.forEach( function(item) { item.classList.add('hidden'); });
        pluses.forEach( function(item) {
            item.classList.remove('glyphicon-menu-up');
            item.classList.add('glyphicon-menu-down');
        });
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

function selector(box_id, body_id, name, obj) {
    var body = document.getElementById(body_id);
    var box  = document.getElementById(box_id);
	var div = document.getElementById(obj);
    var txt = '<a title=\"Deselect ' + name + '\" href=\"javascript:;\" onclick=\"selector(\''
        + box_id + '\', \'' + body_id + '\', \'' + name + '\', \''+ obj + '\')\">' + name + '</a> | '

    if (!box) { return; }
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
    var boxes  = Array.from(document.getElementsByName(box_name));
    var bodies = Array.from(document.getElementsByClassName(body_name));

    boxes.forEach( function (box, i) {
        if ( box.checked != state ) { selector(box.id, bodies[i].id, box.dataset.target, obj); }
    });
}

function Validation(cmd, srv, upd, job, scr, dmp, dgr) {

    var check = function(item) { return item.checked; }

    if (job) {
        var jobs = Array.from(document.getElementsByName('selected_jobs'));
        if (!jobs.some(check)) { alert('Job(s) not selected.'); return false; }
    }

    if (scr) {
        var scripts = Array.from(document.getElementsByName('selected_scripts'));
        if (!scripts.some(check)) { alert('Script(s) not selected.'); return false; }
    }

    if (upd) {
        var updates = Array.from(document.getElementsByName('selected_updates'));
        if (!updates.some(check)) { alert('Update(s) not selected.'); return false; }
    }

    if (dmp) {
        var dumps = Array.from(document.getElementsByName('selected_dbdumps'));
        if (!dumps.some(check)) { alert('Dump(s) not selected.'); return false; }
    }

    if (srv) {
        var server_names = '';
        var servers = Array.from(document.getElementsByName('selected_servers'));
        if (!servers.some(check)) { alert('Server(s) not selected.'); return false; }
        servers.forEach(function(S) { if (S.checked) { server_names = '\n\t' + S.dataset.target + server_names; }});
    }

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
        document.getElementById('run_cmnd').value = cmd;
        document.getElementById('selector').submit();
    }
}

function filter_by(id, value) {
    var run_cmnd = document.getElementById('run_cmnd');
    if (run_cmnd) { run_cmnd.value = ''; }

    document.getElementById(id).value = value;
    document.getElementById('selector').submit();
}

function filter_selected(id, name) {
    var selected_names = []
    var array = Array.from(document.getElementsByName(name));
    array.forEach(function(S) {if (S.checked) {selected_names.push(S.dataset.target);}});
    filter_by(id, selected_names.join('|'))
}

function show_commands(name) {

    var cmdlist = document.getElementById(name);

    Array.from(document.getElementsByClassName('hidden_commands')).forEach(
        function(item) { item.classList.add('hidden'); }
    );
    if (cmdlist) { cmdlist.classList.remove('hidden'); }
}

function show_hide_commands(name) {

    var cmdlist = document.getElementById(name);
    if (cmdlist) {
        if (cmdlist.classList.contains('hidden')) { cmdlist.classList.remove('hidden'); }
        else { cmdlist.classList.add('hidden'); }
    }
}

window.onload = function() {

    var roller_list = Array.from(document.getElementsByClassName('roller'));
    var run_cmnd = document.getElementById('run_cmnd');
    var updown = document.getElementById('updown');
    var tabs = document.getElementById('id_tab');
    var hash = window.location.hash;

    // Deselect all on load
    select_all('selected_jobs',    'job-body',    false, 'SJ');
    select_all('selected_dbdumps', 'dump-body',   false, 'SD');
    select_all('selected_scripts', 'script-body', false, 'SX');
    select_all('selected_servers', 'server-body', false, 'SS');
    select_all('selected_updates', 'update-body', false, 'SU');

    // Empty command just in case)
    if (run_cmnd) { run_cmnd.value = ''; }

    // Show\hide fast scrolling buttons
    window.onscroll = function() { if (document.body.scrollTop > 10) { updown.classList.remove('hidden'); }
                                                                else { updown.classList.add('hidden'); }  }
    roller_list.forEach( function(item) { item.onscroll = function() {
                                            if (item.scrollTop > 10) { updown.classList.remove('hidden'); }
                                                                else { updown.classList.add('hidden');    } }});
    // Change tab on load
    if (!hash) { hash = '#scripts'; }
    if (tabs)  {
        tabs.value = hash.replace('#', '');
        show_commands(tabs.value + '_commands');
        go_up();
    }
    hash && $('ul.nav a[href="' + hash + '"]').tab('show');

    // Change tab on click
    $('.nav-tabs a').click(function() {
        $(this).tab('show');
        window.location.hash = this.hash;
        tabs.value = this.hash.replace('#', '');
        show_commands(tabs.value + '_commands');
        go_up();
    });

    // Change tab on hashchange
    window.addEventListener('hashchange', function() {
        var changedHash = window.location.hash;
        tabs.value = changedHash.replace('#', '');
        changedHash && $('ul.nav a[href="' + changedHash + '"]').tab('show');
        show_commands(tabs.value + '_commands');
        go_up();
    }, false);

    // Show\hide objects info
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

        if (document.getElementById('id_job_info').checked) {
               show_or_hide_all('id_job_info', 'job-panel', 'jshow', 'show'); }
        else { show_or_hide_all('id_job_info', 'job-panel', 'jshow', 'hide'); }
    }
}