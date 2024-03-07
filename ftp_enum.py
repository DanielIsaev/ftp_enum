#!/usr/bin/python3
import argparse
import ftplib
import tempfile
import os
import signal
from time import sleep


def signal_handler(sig, frame):
    exit(1)


def is_dir(ftp, item):
    original_cwd = ftp.pwd()
    try:
        item_quoted = ftp.cwd(f"'{item}'") if ' ' in item else item
        ftp.cwd(item_quoted)
        return True
    except ftplib.all_errors:
        return False
    finally:
        ftp.cwd(original_cwd)


def print_dir(ftp, dir_path, read_perms, write_perms):
    print(f'====== {dir_path} ======\n')
    
    lines = []
    ftp.retrlines('LIST -a', lines.append)
    for line in lines:
        if not line.endswith('.'):
            print(line)
    
    perms = ', '.join(write_perms) if write_perms else "False"
    print(f'\nRead Access: {read_perms}')
    print(f'Write Access: {perms}\n')
    

def check_perms(ftp, dir_path):
    
    dir_path = os.path.join(dir_path, '')

    depth = dir_path.count('/')
    if recursion and depth > recursion:
        return

    read, write = False, [] 
    try:
        dir_path_quoted = f"'{dir_path}'" if ' ' in dir_path else dir_path
        ftp.cwd(dir_path_quoted)
        read = True
        try_ftp_op(ftp, "STOR d4cxQo8a", lambda: write.append('Files'))
        try_ftp_op(ftp, 'MKD xT4vf5oG', lambda: write.append('Directories'), is_mkd=True)
    except ftplib.all_errors as e:
        if "425" in str(e):                     # Handle pssive mode issues
            print("Had issues with passive mode, switching to active mode...\n")
            ftp.set_pasv(False)                 # Set FTP connection to active mode
            return check_perms(ftp, dir_path)   # Retry
        else:
            print(f"Error accessing directory {dir_path_quoted}: {e}")
            return
    
    print_dir(ftp, dir_path, read, write)       # Print results
    
    dir_contents = ftp.nlst(dir_path)
    for item in dir_contents:
        item_name = os.path.basename(item)
        item_path = os.path.join(dir_path, item_name)
        
        if is_dir(ftp, item_path):
            check_perms(ftp, item_path)


def try_ftp_op(ftp, command, action, is_mkd=False):
    # Test for write permissions
    with tempfile.TemporaryFile() as temp_file:
        try:
            ftp.storbinary(command, temp_file) if not is_mkd else ftp.mkd('temp_dir')
            action()                # The lambdas in check_perms
            if not is_mkd:
                ftp.delete("d4cxQo8a")
            else:
                ftp.rmd('xT4vf5oG')
        except ftplib.error_perm:
            pass


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='Check permissions for a given FTP server.')
    parser.add_argument('host', type=str, help='Hostname or IP address of the FTP server.')
    parser.add_argument('-u', '--username', type=str, help='Username for the FTP server.', \
            default='anonymous')
    parser.add_argument('-p', '--password', type=str, help='Password for the FTP server.', \
            default='anonymous')
    parser.add_argument('-r', '--recursion', type=int, help='Set the maximum recursion depth of the scan.')
    
    args = parser.parse_args()
    host = args.host
    username = args.username
    password = args.password
    recursion = args.recursion if args.recursion else None
    

    header = '''
       ____ ______ ___    ____                
      / __//_  __// _ \  / __/___  __ __ __ _ 
     / _/   / /  / ___/ / _/ / _ \/ // //  ' \\
    /_/    /_/  /_/    /___//_//_/\_,_//_/_/_/                                      
    '''
    
    print(header, '\n')
    
    with ftplib.FTP(host) as ftp:
                
        ftp.set_pasv(True)
        ftp.login(username, password)

        _os = ' '.join(ftp.sendcmd('SYST').split(' ')[1:])
        _type = " ".join(ftp.getwelcome().split(" ")[1:])
        print('=' * 50)
        print(f'Target info:\n\nOS: {_os}')
        print(f'Server: {_type}')
        print('=' * 50, '\n' * 2)

        try:
            check_perms(ftp, '/')
        except ftplib.all_errors as e:
            print(f'Encountered an unxepcted error: {e}')
        finally:
            try:
                ftp.quit()
            except ftplib.error_reply:  # Handle any exceptions when terminating with SIGINT
                sleep(0.2)
                ftp.quit()
