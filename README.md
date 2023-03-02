# backupPY
This is a work in progress and is incomplete, however it is currently funtional.
If you don't want to compile things yourself then a download can be found [here] ().

## setup
running the file will create an empty .txt file in it's directory named "locations",
this is file is used to store the locations you would like to backup as well as some other data.
The first line is for what day you would like it to backup (1 = monday, 2 = tuesday, etc.) currently it only suports one day and will repeat the backup weekly.
The second line if for the backup directory, or where you want the files to go when they are backed up.
The rest of the lines are for directories you want backed up, put as many as you like.
The resulting file will be a .zip file to save you storage

## limitations
Currently backupPY only supports weekly repeat backups on one day but more options are coming shortly.
I only support .zip files as the final backup product but raw folders will be coming *soon*™.
I will also be adding a UI system to make this program much more intuitive and easy to use.
