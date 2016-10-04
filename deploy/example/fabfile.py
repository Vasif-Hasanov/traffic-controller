from fabric.api import env
from fabric.operations import run, put

env.hosts = ['ubuntu@192.168.0.105']

def load():
    run('mkdir -p /home/ubuntu/tmp')
    put('hello.py', '/home/ubuntu/tmp')

def execute():
    run('python ~/tmp/hello.py')

def cleanUp():
    run('rm -r ~/tmp')

def test():
    load()
    execute()
    cleanUp()
