# backupPY
This program is in beta, it's main functions work and it is functional however there are currently some major limitations.

## setup
running the file will create an empty .txt file in it's directory named "locations",
this is file is used to store the locations you would like to backup as well as some other data, deleteing or moving it deletes save data.
The UI that pops up when run by the user should be self explanitory, and the data is saved to the locations.txt file in it's directory.
The first line is the day the the data will be backed up on (1=monday, 2=tuesday, etc.)
The second line is where the data will go when it is backup.
Every line after that is a location that is going to be copyed to the location stated by the second line.
You MUST press save if you want the data to be save, there is currently no prevention of data loss.

## limitations
Currently backupPY only supports weekly repeat backups on one day but more options are coming *soon*™.
I only support .zip files as the final backup product but raw folders will be coming *soon*™.
The UI *may* have bugs in it however there should be no major program breaking bugs.
