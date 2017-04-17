# Update Server
![screeenshot](https://cloud.githubusercontent.com/assets/18072680/24416507/b0b2d82a-13ed-11e7-8cc9-f9cc1cc6d1c2.png)

It's an ssh wrapper, run ssh commands from web interface.

Start by pressing an 'Update your servers' button or a 'Projects' link at the top.
Select project by clicking on it. Or create a new one via 'Add new project' link.
In the project section navigate using tabs: 'Updates & Servers', 'Cron Jobs' and 'History'.

On the 'Updates & Servers' tab you can view, select and add new Updates & Servers.
'Edit' link brings you the edit form for the selected object.

On the 'Cron Jobs' tab you can view cron jobs scheduled for this project.
You can select them via click or by pressing 'Select All Jobs' button.
And cancel them by pressing 'Delete' button.

On the 'History' tab you can view history log. Events from cron marked light cyan. 
Events ended with errors marked red.

'Add' and 'Select' buttons duplicated at the bottom nav bar.
Available commands are in 'RUN' or 'CRON' menus. If you select command from 'RUN' menu it'l start right now.   
If you select command from 'CRON' menu, cron job will be created to start on current time + 1 minute(if time not set).
If you need exact date\time set it in the date\time widget.
