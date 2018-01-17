#!/usr/bin/env python
import json
import re
import os

import click

def valid_email(string):
    return re.match(r"\w+@\w+.*", string)


class Config(object):
    pass

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--configfilein",type=click.Path(),default="gitclients_credentials.json",required=False,help="Credentials file to read from")
@click.option("--configfileout",type=click.Path(),default="gitclients_credentials.json",required=False, help="Credentials file to write. This file would be used when adding new git clients")
@pass_config
# configfilein and configfileout must be passed in as full path that is  /home/user/file.json is correct and
# ~/file.json is wrong
def cli(config, configfilein, configfileout):
    config.configfile_in = configfilein
    config.configfile_out = configfileout


@cli.command("gitclient")
@click.option('--name', prompt='Name of git client',
              help='The name of the git client you want to configure your current git project for')
@pass_config
def gc(config, name):
    """
    This configures your current git project to use the git client
     you passed in with the name argument
    """
    gitclient = name.lower().replace(" ","")
    git_credentials = json.load(open(config.configfile_in))#get_cre()
    try:
        os.system('git config user.name ' + git_credentials[gitclient]["user.name"])
        os.system('git config user.email ' + git_credentials[gitclient]["user.email"] )               
        click.echo("Current git project configured for your " +gitclient +" account" )
    except KeyError:
        click.echo ("You have not added details for this client yet, please add it by running passing the add argument")

@cli.command('add',short_help="Use this to add new git client")
@click.option('--gc',prompt="Name of git client you want to add",help='Pass in the name of the new git client to pass like so github.Note everything passed in is converted to lower case and trimmed...ie GIT hub becomes github')
@click.option("--username",prompt="Username for this client",help="Add in  your username")
@click.option("--useremail",prompt="Email for this new client", help="Passing the email")
@pass_config
def add(config, gc,username,useremail):
    """
    Add credentials for a new git client
    """
    if not valid_email(useremail):
        raise Exception("Email {} is not valid".format(useremail))
    git_client = gc.lower().replace(" ", "")
    git_credentials = json.load(open(config.configfile_in))
    git_credentials[git_client] ={"user.name":username, "user.email":useremail}
    try:
        json.dump(git_credentials, open(config.configfile_out,"w"))
    except:
        click.echo("New client {} was not added".format(git_client))
    click.echo("New client {} has been added".format(git_client))

if __name__ == '__main__':
    cli()
    