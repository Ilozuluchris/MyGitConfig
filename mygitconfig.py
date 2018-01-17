#!/usr/bin/env python
import json
import re
import os

import click


def is_valid_email(string):
    return re.match(r"\w+@\w+.*", string)


def get_reply_to_create_file(file_name):
    reply = raw_input("File {} does not exist.Do you want to create it? Answer Y/N: ".format(file_name)).upper()
    if reply == "Y":
        return True
    elif reply == "N":
        return False
    else:
        click.echo("Did not understand reply {}, please try again.".format(reply))
        get_reply_to_create_file(file_name)


class Config(object):
    pass


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--configfilein", type=click.Path(), default="gitclients_credentials.json", required=False,
              help="Credentials file to read from")
@click.option("--configfileout", type=click.Path(), default="gitclients_credentials.json", required=False,
              help="Credentials file to write. This file would be used when adding new git clients")
@pass_config
# configfilein and configfileout must be passed in as full path that is  /home/user/file.json is correct and
# ~/file.json is wrong
def cli(config, configfilein, configfileout):
    if not os.path.isfile(configfilein):
        reply = get_reply_to_create_file(configfilein)
        if not reply:
            raise Exception("Stopped script since file {} was not created".format(configfilein))
        with open(configfilein, mode="w") as configfile:
            configfile.write("{}")
    config.configfile_in = configfilein
    config.configfile_out = configfileout


@cli.command("configure", short_help="Configure current git project to use client passed in with arg name")
@click.option('--name', prompt='Name of git client',
              help='The name of the git client you want to configure your current git project for')
@pass_config
def gc(config, name):
    gitclient = name.lower().replace(" ", "")
    git_credentials = json.load(open(config.configfile_in))
    try:
        os.system('git config user.name ' + git_credentials[gitclient]["user.name"])
        os.system('git config user.email ' + git_credentials[gitclient]["user.email"])
        click.echo("Current git project configured for your " + gitclient + " account")
    except KeyError:
        click.echo("You have not added details for this client yet, please add it by running passing the add argument")


@cli.command('add', short_help="Use this to add new git client")
@click.option('-client', prompt="Name of git client you want to add",
              help='Pass in the name of the new git client to pass like so github.Note everything passed in is '
                   'converted to lower case and trimmed...ie GIT hub becomes github')
@click.option("--username", prompt="Username for this client", help="Username to use for client")
@click.option("--useremail", prompt="Email for this new client", help="Email to use for client")
@pass_config
def add(config, client, username, useremail):
    if not is_valid_email(useremail):
        raise Exception("Email {} is not valid".format(useremail))
    git_client = client.lower().replace(" ", "")
    git_credentials = json.load(open(config.configfile_in))
    git_credentials[git_client] = {"user.name": username, "user.email": useremail}
    json.dump(git_credentials, open(config.configfile_out, mode="w"))
    click.echo("New client {} has been added".format(git_client))


if __name__ == '__main__':
    cli()
