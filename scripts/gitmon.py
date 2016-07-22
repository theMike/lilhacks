#!/bin/python


import ConfigParser
import subprocess
import os,sys
import re
import logging

REGEX_BCOUNT="(?<=behind.)\d{1,5}"
REGEX_BEHIND="\[behind\s\d{1,5}\]"

CLONEREPO="git clone"
UPDATEREMOTE="git remote update"
GETSTATUS="git status --porcelain -b"

def git_action(git_cmd):
    return subprocess.check_output(git_cmd,
                stderr=subprocess.STDOUT,
                shell=True)


def jenkins_build(jenkins_url,git_url):
    _jenkins_build = "curl " + jenkins_url + "/git/notifyCommit?url="+git_url

    ret = subprocess.check_output(_jenkins_build,
                stderr=subprocess.STDOUT,
                shell=True)
    return ret 


def git_clone(repository):
    _git_clone = "git clone "+repository
    return git_action(_git_clone)


def git_checkout(branch_name):
    _branch_name = "git checkout "+branch_name
    return git_action(_branch_name)


def git_remote_update():
    _remote_update = "git remote update"
    return git_action(_remote_update)


def git_status(): 
    _git_status = "git status -sb "
    return git_action(_git_status)


def git_pull(branch_name):
    _git_pull = "git pull"
    if branch_name:
        _git_pull += " origin "+branch_name
    
    return git_action(_git_pull)


def enum_commits(git_result_string):
    _change_count = 0
    _pattern = re.search(REGEX_BEHIND, git_result_string)
    if _pattern is not None:
        _pattern = re.search(REGEX_BCOUNT, git_result_string)
        _change_count = _pattern.group(0)

    return _change_count


def init_logger():
    logging.basicConfig(filename='gitmon.log',level=logging.INFO)
    logger = logging.getLogger('gitmon')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    frmtr = logging.Formatter('%(asctime)s: %(name)s: %(message)s')
    ch.setFormatter(frmtr)
    logger.addHandler(ch)
     
    return logger


def git_remote_log(branch_name,log_count,ignore_users):
    _git_remote_log = "git log origin/"+branch_name
    _git_remote_log += " --pretty --format=\"%cn\" -"+str(log_count)
    git_remote_update()
    commit_users = git_action(_git_remote_log).strip().split('\n')
    non_ignore_users = list(set(commit_users) - set(ignore_users))
    # Remove any null items
    non_ignore_users = [x for x in non_ignore_users if x != '']    
    return non_ignore_users


# Run main from here.
def main():
    Config = ConfigParser.ConfigParser()
    Config.read("gitmon.cfg")
    lmsg = init_logger()
    lmsg.info("*****************")
    _working_branch = Config.get("Repo","wbranch")
    os.chdir(Config.get("Repo","pwd"))
    _result = git_status()
    change_count = enum_commits(_result)
    ignore_users = ['Jenkins Continuous Build server']
    r= git_remote_log(_working_branch,change_count,ignore_users)

    if len(r) > 0:
        lmsg.info("We have new commits by the following user(s):")
        lmsg.info(r)
        #jenkins_build("ssh://git@jira.sigma-canada.com:7999/ou/omnicare-plus-ui.git")
        jenkins_build(Config.get("Repo","jenkinsurl"),Config.get("Repo","giturl"))
        
        git_pull(_working_branch)
    else:
        lmsg.info("No new commits from anyone we care about")
    
    lmsg.info("*****************")        


if __name__ == '__main__':
    main()

