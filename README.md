# mygitconfig

Ever gotten tired of typing `git config user.name "John Doe"` and `git config  user.email "johndoe@example.com"` everytime you set up a new git repository.<br>

Introducing mygitconfig. Reduce the number of lines required  to configure a git  project from two to one.<br>

As a fellow programmer I am sure you would appreciate the one line decrease, seeing how much time it takes to make some extra keystrokes.

*This was tested only on Ubuntu 16.04 LTS*
## Commands:
- configure
  - Code:&ensp;`mygitconfig configure --name clientname`
  - This configures the current git project to use the client supplied via the argument name
- add
    - Code:&ensp;`mygitconfig add --client clientname --username username --useremail useremail`
    - This adds a new git client using the arguments supplied
    
 **NOTE:All commands take in two optional arguments `--configfilein` and `--configfileout`.
These arguments are paths to json files used for reading and saving git credentials respectively.They both default to the file `~/.gitclients_credentials.json`. If any the files passed in does not exist they are created**
