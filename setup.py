#!/usr/bin/env python
# -*- coding: utf-8 -*-

import distutils
import os
import sys
import glob
import subprocess

from distutils.command.install import install
from setuptools import setup
from distutils.extension import Extension

PO_DIR = 'po'
MO_DIR = os.path.join('build', 'mo')


class InstallAndUpdateDataDirectory(install):

    def run(self):
        # Run parent install method
        install.run(self)

        # Run shell script to install data files
        get_command_output('sh ./install_data.sh %s' % self.prefix)

        # Compile and install languages
        for po in glob.glob (os.path.join (PO_DIR, '*.po')):
            lang = os.path.basename(po[:-3])
            mo = os.path.join(MO_DIR, lang, 'guake.mo')

            directory = os.path.dirname(mo)
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                rc = subprocess.call(['msgfmt', '-o', mo, po])
                if rc != 0:
                    raise Warning, "msgfmt returned %d" % rc
            except Exception, e:
                sys.exit(1)


def parse_pkg_config(command, components, options_dict=None):
    """ Calls pkg-config (command) for the desired library (components and
    return the appropriate compilation information.
    """
    if options_dict is None:
        options_dict = {
            'include_dirs': [],
            'library_dirs': [],
            'libraries': [],
            'extra_compile_args': []
        }
    commandLine = "%s --cflags --libs %s" % (command, components)
    output = get_command_output(commandLine).strip()
    for comp in output.split():
        prefix, rest = comp[:2], comp[2:]
        if prefix == '-I':
            options_dict['include_dirs'].append(rest)
        elif prefix == '-L':
            options_dict['library_dirs'].append(rest)
        elif prefix == '-l':
            options_dict['libraries'].append(rest)
        else:
            options_dict['extra_compile_args'].append(comp)

    commandLine = "%s --variable=libdir %s" % (command, components)
    output = get_command_output(commandLine).strip()

    return options_dict


def get_command_output(cmd, warnOnStderr=True, warnOnReturnCode=True):
    """Wait for a command and return its output.  Check for common
    errors and raise an exception if one of these occurs.
    """
    p = subprocess.Popen(cmd, shell=True, close_fds=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if warnOnStderr and stderr != '':
        raise RuntimeError("%s outputted the following error:\n%s" %
                           (cmd, stderr))
    if warnOnReturnCode and p.returncode != 0:
        raise RuntimeError("%s had non-zero return code %d" %
                           (cmd, p.returncode))
    return stdout


gtk_config = parse_pkg_config('pkg-config','gtk+-2.0')
globalhotkeys = Extension(
                "guake.globalhotkeys",
                ['src/globalhotkeys/globalhotkeys.c',
                 'src/globalhotkeys/keybinder.c',
                 'src/globalhotkeys/eggaccelerators.c'],
                **gtk_config)


setup(
    name='guake',
    version='0.4.3',
    license='GPL-2',
    author='Lincoln de Sousa',
    author_email='lincoln@guake.org',
    description='Drop-down terminal for GNOME',
    long_description='''Guake is a drop-down terminal for Gnome Desktop 
Environment, so you just need to press a key to invoke him, and press 
again to hide.''',
    url='http://guake.org',
    package_dir = {'guake': 'src'},
    packages = ['guake'],
    scripts=['src/guake'],
    cmdclass={'install': InstallAndUpdateDataDirectory},
    ext_modules=[globalhotkeys]
    )
