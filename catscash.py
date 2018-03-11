#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: catscash.py
    Arguments:
        -v, --verbose: print status on stdout
        -c, --config-file: alternativbe configuration file.
    					   Default is catscash.conf in same directory as script
        -q, --qif-file: QIF file to integrate in the database 
    Description:
        Parse the given QIF file and upload it in the database with the right
        categories and payees 
    Requirements:
"""


# Standards imports
import os
import argparse
import configparser
from pathlib import Path
from qifparse.parser import QifParser, QifParserException

__version__ = "0.0.1"
__date__ = "2018-03-03"
__author__ = "Denis Lambolez"
__contact__ = "denis.lambolez@gmail.com"
__license__ = "LGPL-3.0"


# Class definition
class Error(Exception):
    """Class: base class for exceptions in this module."""
    pass


# Functions
def get_parameter(configuration, section_name, parameter_name, default_value, is_verbose):
    """ Get parameter value from the config file """
    try:
        parameter_value = configuration.get(section_name, parameter_name)
    except configparser.Error as err:
        if isinstance(err, configparser.NoOptionError) and not default_value is None:
            parameter_value = default_value
        else:
            print("Fatal - {} error with error: {}"
                  .format(parameter_name, str(err)))
            exit(1)
    if is_verbose:
        print("\t{}: {}".format(parameter_name, parameter_value))
    return parameter_value

def main():
    """ Script main function """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Upload QIF file in database"
                                     + "with right categories and payees")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-c", "--config-file", help="Alternative configuration file",
                        default=Path(__file__).stem + ".conf")
    parser.add_argument("-q", "--qif-file", help="QIF file to upload",
                        default=Path(__file__).stem + ".qif")
    args = parser.parse_args()

    # Get configuration file from prameters
    config_file = args.config_file.strip()
    if args.verbose:
        print("Reading configuration from: " + config_file)
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except configparser.Error as err:
        print("Fatal - configuration reading error: " + err.message)
        exit(1)

    # Parse QIF file
    if args.verbose:
        print("Parsing QIF file: " + args.qif_file)
    try:
        with open(args.qif_file,'r') as f:
            qif = QifParser.parse(f)
    except (IOError, QifParserException) as err:
        print("Fatal - QIF file parsing error: " + str(err))
        exit(1)
    print(str(qif))
    
# Main
if __name__ == "__main__":
    main()
