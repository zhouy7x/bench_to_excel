# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import datetime
import os
import subprocess
import signal
import pandas as pd

config = None
RepoPath = None
BenchmarkPath = None
DriverPath = None
Timeout = 15*60
PythonName = None
Includes = None
Excludes = None


class FolderChanger:
    def __init__(self, folder):
        self.old = os.getcwd()
        self.new = folder

    def __enter__(self):
        os.chdir(self.new)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old)


def chdir(folder):
    return FolderChanger(folder)


class ExcelWriter:
    def __init__(self, name):
        self.file_name = name
        self.output_dir = "data"
        self.writer = None

    def __enter__(self):
        print(self.file_name)
        if not os.path.isdir(self.output_dir):
            os.system('rm -rf data')
            os.mkdir(self.output_dir)
        self.writer = pd.ExcelWriter(os.path.join(self.output_dir, self.file_name))
        return self.writer

    def __exit__(self, type, value, traceback):
        self.writer.save()


def touch_excel(name):
    return ExcelWriter(name)


def check_folder(foo):
    def _inside(folder):
        if os.path.exists(folder):
            print("Folder '%s' already exists! Exit." % folder)
            return
        foo(folder)
    return _inside


@check_folder
def mkdir(folder):
    Run(['mkdir', '-p', folder])


def Run(vec, env=os.environ.copy()):
    print(">> Executing in " + os.getcwd())
    print(' '.join(vec))
    # print("with: " + str(env))
    try:
        o = subprocess.check_output(vec, stderr=subprocess.STDOUT, env=env)
    except subprocess.CalledProcessError as e:
        print('output was: ' + e.output)
        print(e)
        raise e
    o = o.decode("utf-8")
    try:
        print(o)
    except:
        print("print exception...")
    return o


def Shell(string):
    print(string)
    status, output = subprocess.getstatusoutput(string)
    print(output)
    return status, output


def config_get_default(section, name, default=None):
    if config.has_option(section, name):
        return config.get(section, name)
    return default


class TimeException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeException()


class Handler:
    def __init__(self, signum, lam):
        self.signum = signum
        self.lam = lam
        self.old = None

    def __enter__(self):
        self.old = signal.signal(self.signum, self.lam)

    def __exit__(self, type, value, traceback):
        signal.signal(self.signum, self.old)
        
    
def RunTimedCheckOutput(args, env=os.environ.copy(), timeout=None, **popenargs):
    if timeout is None:
        timeout = Timeout
    if type(args) == list:
        print('Running: "'+ '" "'.join(args) + '" with timeout: ' + str(timeout)+'s')
    elif type(args) == str:
        print('Running: "'+ args + '" with timeout: ' + str(timeout) + 's')
    else:
        print('Running: ' + args)
    try:
        if type(args) == list:
            print("list......................")
            p = subprocess.Popen(args, bufsize=-1,  env=env, close_fds=True, preexec_fn=os.setsid, 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, **popenargs)

            with Handler(signal.SIGALRM, timeout_handler):
                try:
                    signal.alarm(timeout)
                    output = p.communicate()[0]
                    # if we get an alarm right here, nothing too bad should happen
                    signal.alarm(0)
                    if p.returncode:
                        print("ERROR: returned" + str(p.returncode))
                except TimeException:
                    # make sure it is no longer running
                    # p.kill()
                    os.killpg(p.pid, signal.SIGINT)
                    # in case someone looks at the logs...
                    print ("WARNING: Timed Out 1st.")
                    # try to get any partial output
                    output = p.communicate()[0]
                    print ('output 1st =', output)

                    # try again.
                    p = subprocess.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True,
                                             preexec_fn=os.setsid,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, **popenargs)
                    try:
                        signal.alarm(timeout)
                        output = p.communicate()[0]
                        # if we get an alarm right here, nothing too bad should happen
                        signal.alarm(0)
                        if p.returncode:
                            print("ERROR: returned" + str(p.returncode))
                    except TimeException:
                        # make sure it is no longer running
                        # p.kill()
                        os.killpg(p.pid, signal.SIGINT)
                        # in case someone looks at the logs...
                        print ("WARNING: Timed Out 2nd.")
                        # try to get any partial output
                        output = p.communicate()[0]

        else:
            # import subprocess32
            p = subprocess.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True, preexec_fn=os.setsid,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, **popenargs)
            # with Handler(signal.SIGALRM, timeout_handler):
            try:
                output = p.communicate(timeout=timeout)[0]
                # if we get an alarm right here, nothing too bad should happen
                if p.returncode:
                    print("ERROR: returned" + str(p.returncode))
            except subprocess.TimeoutExpired:
                # make sure it is no longer running
                # p.kill()
                os.killpg(p.pid, signal.SIGINT)
                # in case someone looks at the logs...
                print ("WARNING: Timed Out 1st.")
                # try to get any partial output
                output = p.communicate()[0]
                print ('output 1st =',output)

                # try again.
                p = subprocess.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True, preexec_fn=os.setsid,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, **popenargs)
                try:
                    output = p.communicate(timeout=timeout)[0]
                    # if we get an alarm right here, nothing too bad should happen
                    if p.returncode:
                        print("ERROR: returned" + str(p.returncode))
                except subprocess.TimeoutExpired:
                    # make sure it is no longer running
                    # p.kill()
                    os.killpg(p.pid, signal.SIGINT)
                    # in case someone looks at the logs...
                    print ("WARNING: Timed Out 2nd.")
                    # try to get any partial output
                    output = p.communicate()[0]

        print ('output final =', output)
        return output
    except Exception as e:
        pass


def get_available_memory():
    cmd = "cat /proc/meminfo | grep MemAvailable"
    try:
        free_mem = int(os.popen(cmd).read().split()[1])
    except Exception as e:
        print(e)
        free_mem_final = '8g'
    else:
        kw = 'k'
        if free_mem > 1024:
            kw = 'm'
            free_mem = free_mem / 1024
            if free_mem > 1024:
                kw = 'g'
                free_mem = free_mem / 1024
        free_mem_final = str(int(free_mem * 0.8)) + kw
    print(free_mem_final)
    return free_mem_final


def timezone():
    return datetime.datetime.now().strftime("%y%m%d-%H%M%S")
