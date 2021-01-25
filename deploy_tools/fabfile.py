import random
import paramiko, os
paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG) 
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run,task,settings
from fabric.context_managers import cd
from fabric import *

env.user="root"
env.password = "1236985"
env.key_filename=[r"C:/Users/dropletpuplic.pem"]
env.hosts=["165.232.110.163:22"]
env.port=22
env.use_ssh_config = True
REPO_URL = 'https://github.com/OMAR-EHAB777/todoapp.git'

    
def list_files():
        with cd('/root/stagetodoapp'):
            run('ls')
def site_folder():  
    code_dir ='/env.user/'
    with cd (code_dir):
        run('ls')      
def deploy():
    site_folder = '/root/stagetodoapp' 
    with cd(site_folder):
      run('mkdir -p {site_folder}')
      with cd(site_folder):
         _get_latest_source()
         _update_virtualenv()
         _create_or_update_dotenv()
         _update_static_files()
         _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.6 -m pipenv shell')
    run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')