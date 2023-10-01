'''
title:          Google Photos Batch Rename.py
description:    this program allows me to traverse through my google
                photos folder and batch rename the files depending on
                the name of the folder while taking into account the
                files extension and number of files in said folder
author:         Martise Jones
date:           February 23, 2019
version:        2.1
notes:          1.  code refactoring in conjunction to adding .heic file
                    format to list of formats to keep
                2.  modified code to so that it can run in unix based
                    systems without overwriting files
                3.  create function that will determine if the file
                    exists or not so that the script does not accidently
                    overwrite the existing file
                4.  create a function that allows me to obtain contents
                    of a directory so that i'm not constantly using the
                    same 2-3 lines of code
python_version: 3.7.2
issues:         1.  refactor code to create a better menu experience
                    that uses less code throughout the entire script
                2.  functions that will utilize scan_dir:
                    1.  choose_directory
                    2.  does_subdirectory_exist
                    3.  rename_files
#=======================================================================

global variables:
-----------------
mainPath            default folder for unix/osx file systems
counter             used to show the number of folders/files in current
                    directory
directory           list that stores subdirectories
userDirectory       list that stores the user defined directory
testParameter       boolean used to test whether statement is true or
                    false
answer              string used to obtain generic user input
previousDirectory   string that stores the previous directory that the
                    script was in
'''

# import statements
import os
import sys
from pathlib import Pat

# initialize global variables
mainPath = os.path.expanduser('~/Google Drive/Google Photos')
directory = ''
userDirectory = ''
counter = 1
testParameter = False
answer = ''
previousDirectory = ''

# define functions

def screen_heading():
    '''
    Summary:
    --------
    this is a function that will display title of the application across
    the screen for appearance purposes

    Parameters:
    -----------
    none

    Returns:
    --------
    none

    Local Variables:
    ----------------
    none
    '''

    print('-' * 30 + 'Google Photos Batch Rename' + '-' * 30 \
        + '\n\n'
        )

def create_heading(folder):
    '''
    Summary:
    --------
    this is a function that will take the provided name of the folder
    and display it in a titular form with dashes running underneath.

    Parameters:
    -----------
    folder : string or pathlib.Path
        the full path of the current working directory

    Returns:
    --------
    none

    Local Variables:
    ----------------
    none
    '''

    print(folder.upper())
    print('-' * len(folder) + '\n')


def choose_directory(path):
    '''
    Summary:
    --------
    function that will store store all folders within a directory in a
    list and then display them on screen for the user.
    from there the I will have the ability to select which subdirectory
    I would like to enter into. loop through all subdirectories in the
    folder and append them to the directory list

    Parameters:
    -----------
    path : string or pathlib.Path
        allows for me to pass the specified path that the function will
        traverse through except for when traversing through the main
        Google Photos folder.        

    Returns:
    --------
    none

    Local Variables:
    ----------------
    none
    '''

    # call on scan_dir and assign the returned directories to directory
    directory = scan_dir(path, 'directories')
    
    # add an exit clause to directory
    directory.append('Exit')
    
    testParameter = False
    
    # traverses through the list and print the contents on screen for
    # the user to make a choice.
    while not testParameter:
        # exception handling test to ensure that the user only uses integers
        # when selecting a choice
        while True:
            os.system('clear')
            screen_heading()
            create_heading(path)
            counter = 1
            try:
                for subDir in directory:
                    print('{}.\t{}'.format(counter, subDir))
                    counter += 1
            
                answer = int(input(
                    '\n\nEnter Your Choice [1-{}]: '.format
                    ((len(directory)))
                    ))
                break
            except ValueError:
                os.system('clear')
                screen_heading()
                input(
                    'Not A Valid Entry. Choice Must Be Digits Only.\n'
                    '\nPress Any Key To Continue.'
                    )
                        
        if answer < 1 or answer > len(directory):
            os.system('clear')
            screen_heading()
            input('Invalid Entry. Please Try Again')
        elif answer == len(directory):
            while not testParameter:
                os.system('clear')
                screen_heading()
                answer = input(
                    '\n\nAre You Sure You Wish To Exit The Application? Enter'
                    ' "Y" or "N": '
                    )
                if answer.upper() == 'Y':
                    sys.exit()
                elif answer.upper() == 'N':
                    break
                else:
                    os.system('clear')
                    screen_heading()
                    input(
                        '\n\nNot a Valid Entry. Choice Must Be Either "Y" Or '
                        '"N". Press Any Key to Continue. '
                        )
                    testParameter = False
        else:
            testParameter = True
    
    return directory[answer - 1]
    
def does_subdirectory_exist(dir):
    '''
    Summary:
    --------
    this is a function that will parse through the current directory and
    determine whether a subdirectory exists. if a subdirectory does not
    exist then the function will return a bool of False. if a
    subdirectory does exist the the function will prompt the user to
    display the the files in the directory or the subdirectories.

    Parameters:
    -----------
    dir : string or pathlib.Path
        the dir input argument is the current working directory passed
        to the function from the main() function

    Returns:
    --------
    boolean True or False

    Local Variables:
    ----------------
    none
    '''

    directory = sorted(next(os.walk(dir))[1])
    directory = [d for d in directory if not d == '.']
    testParameter = False
    if not directory:
        return False
    else:
        while testParameter is not True:
            os.system('clear')
            screen_heading()
            create_heading(dir)
            answer = input(
                '\n\nThere Are {} Subdirectories Inside of {}. Enter "Y" To '
                'View The Subdirectories Or Enter "N" To Rename Files Inside '
                'of {}: '.format(
                    len(directory),
                    os.path.split(dir)[1], 
                    os.path.split(dir)[1]
                    )
                )
            if answer.upper() == 'Y':
                return True
            elif answer.upper() == 'N':
                return False
            else:
                input(
                    '\n\nNot a Valid Entry. Choice Must Be Either "Y" Or "N" '
                    '. Press Any Key to Continue. '
                    )
                testParameter = False
     
def scan_dir(path, scanFor):
    '''
    Summary:
    --------
    function that will scan the contents of a directory and return a
    list of files/subdirectories inside the original directory.

    Parameters:
    -----------
    path : string or pathlib.Path
        path that the function is supposed to parse through.
    scanFor : string
        determines whether or not to scan for a file or directory

    Returns:
    --------
    directories
    files

    Local Variables:
    ----------------
    directories list that contains a list of directories in path
    files       list that contains a list of files in path
    '''

    # if the script needs to scan for directories, then scan path and
    # obtain the directories in the path
    if scanFor.lower() == 'directories':
        directories = sorted(next(os.walk(path))[1])
        directories = [d for d in directory if not d == '.']
        return directories
    # if the script needs to scan for files, then scan path and obtain
    # files in directory excluding hidden files (files that start with
    # '.')
    elif scanFor.lower() == 'files':
        files = next(os.walk(path))[2]
        files = [f for f in fileListing if not f[0] == '.']
        return files
    # otherwise return error
    else:
        raise ValueError("Wrong Value Entered. scanFor Must be 'Directories'"
            "or 'Files'")
        )

def does_file_exist(file):
    '''
    Summary:
    --------
    this is a function that is used to take a file that is passed to the
    function and determine if the file already exists. if the file does
    in fact exist, then return a boolean value of False so that the
    calling functinon (rename_files) does not overwrite the existing
    file

    Parameters:
    -----------
    file : string or pathlib.Path
        the file that needs to be checked if it exists or not

    Returns:
    --------
    True or False

    Local Variables:
    ----------------
    '''

    # check to see if file exist
    if os.path.isfile(file):
        return True
    else:
        return False

def rename_files(path, title):
    '''
    Summary:
    --------
    this is a function that is used to parse through the contents of the
    folder then find and rename all files using the following naming
    convention: "Folder Name - item number.extension". 

    the Function will also find any heic files found in folder and
    rename them as to not accidently rename them to to the wrong format
    
    Parameters:
    -----------
    path : string or pathlib.Path
        the path input argument is simply the path that the function is
        supposed to parse through.
    title : string 
        the title input argument is needed to pass through the folder
        name.

    Returns:
    --------
    none

    Local Variables:
    ----------------
    fileListing list that contains the names of all of the files stored
                in the current directory
    '''

    # initialize counter to 1
    counter = 1
    
    # create list that stores all of the files in directory excluding
    # hidden files (files that start with '.')
    fileListing = next(os.walk(path))[2]
    fileListing = [f for f in fileListing if not f[0] == '.']

    # parse through the list and rename files to path name + counter
    for f in fileListing:
        # if counter is less than ten then add a zero to counter for display
        # purposes
        if counter < 10:
            # check to see if file uses apple's new HEIC extension. if it does
            # then manually provide the file extension. otherwise obtain
            # the extension from the file itself
            if '.HEIC' not in f:
                extension = f[-3:]  # stores the last three letters
                                    # (extension) of the file
                os.rename(f, '{}-0{}.{}'.format(title, counter, extension))
            else:
                os.rename(f, '{}-0{}.HEIC'.format(title, counter))
            counter += 1
        else:
            # check to see if file uses apple's new HEIC extension. if it does
            # then manually provide the file extension. otherwise obtain
            # the extension from the file itself
            if '.HEIC' not in f:
                extension = f[-3:]   # stores the last three letters of file
                os.rename(f, '{}-{}.{}'.format(title, counter, extension))
            else:
                os.rename(f, '{}{}.HEIC'.format(title, counter))
            counter += 1
            
##############################################################################
# reverse_or_exit(title, directory)
# this is a function that will display a message informing the user that all
# files have been successfully renamed and then prompt the user to either exit
# the program or allow the user to go up one directory from the current
# directory. the title input argument is used to feed the name of the current
# folder to create_heading(). the directory input argument is used to display
# the name of the previous folder
def reverse_or_exit(title, directory):
    testParameter = False
    
    # prompt the user to exit the program or go back one directory
    while not testParameter:
        os.system('clear')
        screen_heading()
        create_heading(title)
        
        answer = input(
            'All Files Have Successfully Been Renamed.\n\nPress "Y" To Go Back'
            ' To {}, Or "N" To Exit The Program: '.format
            (os.path.split(directory)[1])
            )
            
        # test to ensure that that the user enters in only "Y" or "N". if the
        # users enters "Y", then go back one directory. otherwise exit the
        # program
        if answer.upper() == 'Y':
            return True
        elif answer.upper() == 'N':
            sys.exit()
        else:
            os.system('clear')
            screen_heading()
            answer = input(
                '\n\nNot a Valid Entry. Choice Must Be Either "Y" Or "N" '
                '. Press Any Key to Continue. '
                )
            testParameter = False
            
##############################################################################
# main()
# this is a function that is used to run the main part of the program calling
# on various other functions in the script to parse through folders and rename
# the files inside of said folders
def main():
    # change directories to the mainPath
    os.chdir(mainPath)
    testParameter = False
    
    # call on choose_directory function to have the user select the
    # subdirectory that they would like to enter into, then pass that
    # value to variable userDirectory.
    userDirectory = choose_directory(mainPath)
    
    # join userDirectory and mainPath to create a new path
    userDirectory = os.path.join(mainPath, userDirectory)
    
    # traverse through directories until the user decides not to enter into
    # the subdirectory or there are no other subdirectories to enter in to
    while not testParameter:
        # change directories to the new path
        os.chdir(userDirectory)
        
        # call on does_subdirectory_exist() to determine if there are any
        # subdirectories.
        if does_subdirectory_exist(userDirectory):
            # store userDirectory to previousDirectory in the even that there
            # are subdirectories in the current directory, that way the user
            # can go up one directory if they choose to
            previousDirectory = userDirectory
            
            # call on choose_directory() to have the user select the
            # subdirectory that they would like to enter into, then pass that
            # value to variable userDirectory
            userDirectory = choose_directory(previousDirectory)
            userDirectory = os.path.join(previousDirectory, userDirectory)
        # if there are not any more subdirectories or the user elects not to
        # go any further in the directory tree
        else:
            # call on rename_files() to start renaming all of the files in the
            # current directory
            rename_files(userDirectory, os.path.split(userDirectory)[1])
            
            # set previousDirectory to the directory up one path so that the
            # user can go up one directory
            previousDirectory = os.path.abspath(os.path.join(os.getcwd(),".."))
            
            # if reverse or exit returns a value of true then go up one
            # directory
            if reverse_or_exit(userDirectory, previousDirectory):
                userDirectory = previousDirectory
                testParameter = False

# END CREATE AND DEFINE METHODS

# MAIN PROGRAM
if __name__ == '__main__':
    main()
