#
#    Copyright (C) 2014 Alexandre Viau <alexandre@alexandreviau.net>
#
#    This file is part of python-pass.
#
#    python-pass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    python-pass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with python-pass.  If not, see <http://www.gnu.org/licenses/>.
#

import click
import os
import subprocess


@click.group()
def main():
    pass


@main.command()
@click.option('--path', '-p',
              type=click.Path(file_okay=False, resolve_path=True),
              default='~/.password-store',
              help='Where to create the password store.')
@click.argument('gpg-id', type=click.STRING)
def init(path, gpg_id):
    print ('path: ' + path)
    print ('gpg_id: ' + gpg_id)

    # Create a folder at the path
    if not os.path.exists(path):
        os.makedirs(path)

    # Create .gpg_id and put the gpg id in it
    with open(os.path.join(path, '.gpg_id'), 'w') as gpg_id_file:
        gpg_id_file.write(gpg_id)


@main.command()
@click.argument('path', type=click.STRING)
def insert(path):

    # TODO: Don't hardcode ~/.password-store
    passfile_path = os.path.realpath(
        os.path.join(
            os.path.expanduser('~/.password-store'),
            path + '.gpg'
        )
    )

    password = click.prompt(
        'Enter the password',
        type=str,
        confirmation_prompt=True
    )

    gpg = subprocess.Popen(
        [
            'gpg',
            '-R',
            '3CCC3A3A', # TODO: Get user's key
            '--batch',
            '--no-tty',
            '-o', passfile_path,
            '-e',
        ],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    gpg.stdin.write(password)
    gpg.stdin.close()

    #print gpg.stderr.read().strip()
    #print gpg.stdout.read().strip()


if __name__ == '__main__':
    main()