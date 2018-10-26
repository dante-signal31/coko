# coko
Tool to overwrite directories using files from a different owners but keeping original owners and permissions.
____
Sometimes you have a directory full of files you want to overwrite periodically. 

You may not want to edit those files directly but let other users edit a local copy of those files to copy them over original ones. 

Problem there is that local copies may have changed their owners or permissions to be edited so those metadata are carried over original directory overwriting it.

This tools let you take an snapshot of your files metadata in a particular directory in order to restore those metadata after files have been restored.
