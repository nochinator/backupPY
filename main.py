import shutil
import datetime
import os
import time
import zipfile

while True:
    # Define the source and destination directories
    if not os.path.exists('locations.txt'):
        open('locations.txt', 'w').close()

    with open('locations.txt') as f:
        backup_interval = float(next(f).strip())
        destination_dir = next(f).strip()
        source_dirs = [line.strip() for line in f]

    # Get the current date
    today = datetime.date.today()

    # Calculate the date of the last backup
    last_backup = today - datetime.timedelta(days=backup_interval)

    # Check if a backup is needed
    if not os.path.exists(os.path.join(destination_dir, last_backup.strftime('%Y-%m-%d'))):
        # Create a new backup folder with the current date
        backup_folder = os.path.join(destination_dir, today.strftime('%Y-%m-%d'))
        os.makedirs(backup_folder)

        # Backup each source directory
        for i, source_dir in enumerate(source_dirs, 1):
            print(f"Backing up {source_dir} ({i}/{len(source_dirs)})...")
            shutil.copytree(source_dir, os.path.join(backup_folder, os.path.basename(source_dir)))
            print(f"Backup of {source_dir} complete.")

        # Create a ZIP archive of the backup folder
        print("zipping")
        with zipfile.ZipFile(os.path.join(destination_dir, today.strftime('%Y-%m-%d') + '.zip'), 'w',
                             zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_folder):
                for file in files:
                    zipf.write(os.path.join(root, file))

        # Print a message indicating that the backup was successful
        print(
            f"Backup created at {backup_folder} and compressed to {os.path.join(destination_dir, today.strftime('%Y-%m-%d') + '.zip')}")

    else:
        # Wait for some time before checking again
        time.sleep(7200)  # 2 hours in seconds
