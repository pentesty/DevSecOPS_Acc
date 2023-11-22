import csv
import json
import logging
import os
import platform

from argparse import ArgumentParser

logger = logging.getLogger()


def parse_arguments():
    try:
        description = "This script transforms data received from tool to csv format."
        epilog = "Provides help for the commandline options"
        parser = ArgumentParser(description=description, epilog=epilog)
        parser.add_argument('-t', '--test_name', action='store', help='provide the test name')
        parser.add_argument('-p', '--path', action='store', help='provide the path for test output file')
        parser.add_argument('-o', '--output', action='store', default='consolidated_test_output.json',
                            help='creates csv/json from the test output file')

        cmd_args = parser.parse_args()
        logger.info(f"Arguments parsed successfully : {cmd_args}")
        return cmd_args
    except Exception as e:
        logger.fatal(f"Arguments are not correctly provided. : {e}")
        raise Exception("Arguments are not correctly provided.")


def check_header(filename):
    try:
        with open(filename) as f:
            first = f.read(1)
            return first not in '.-0123456789'
    except Exception as e:
        logger.fatal(f"Exception occurred in check_header : {e}")
        raise Exception(f"Exception occurred in check_header ")


def get_output_filename(filename):
    try:
        # Create folder output_files if not already present in a4mation directory
        output_files_path = "../../../output_files"
        if not os.path.exists(output_files_path):
            os.mkdir(output_files_path)

        # Create test tool output file with system name in prefix
        file_path = os.path.join(output_files_path, filename)
        logger.debug(f"output filepath : {file_path}")
        return file_path
    except Exception as e:
        logger.fatal(f"Exception occurred in get_output_filename : {e}")
        raise Exception(f"Exception occurred in get_output_filename ")


def write_to_csv(dict_data, cmd_args, input_json):
    try:
        # Create folder output_files if not already present and get log filename having system name in prefix
        file_path = get_output_filename(cmd_args.output)
        system_name = platform.node()

        if "cis" in cmd_args.test_name.lower():
            json_file_name = os.path.split(cmd_args.path)[1]

            # Get the ip and system details from json file
            sys_details = json_file_name.split("_")
            system_name = sys_details[2] + "_" + sys_details[1]
            logger.info(f"system name details in format os name and IP : {system_name}")

        for each in dict_data:
            each['system_name'] = system_name
        logger.info(dict_data)
        with open(file_path, 'a+', newline='') as csvfile:
            headers = check_header(file_path)
            writer = csv.DictWriter(csvfile, fieldnames=input_json['csv_headers'])
            if not headers:
                writer.writeheader()
            writer.writerows(dict_data)
        logger.info("Dictionary data successfully written to csv")
    except Exception as e:
        logger.fatal(f"Failed to write to csv file : {e}")
        raise Exception("Failed to write to csv file")


def add_data_to_json_file(dict_data, json_file):
    try:
        # Create folder output_files if not already present and get log filename having system name in prefix
        file_path = get_output_filename(json_file)

        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            logger.info("json file exists and is readable")
            with open(file_path, 'r+') as outfile:
                # First we load existing data into a dict.
                file_data = json.load(outfile)
                # Join new_data with file_data inside emp_details
                logger.debug(f"Write to json : {file_data}")
                file_data.extend(dict_data)
                # Sets file's current position at offset.
                outfile.seek(0)
                # convert back to json.
                json.dump(file_data, outfile, indent=4)
        else:
            with open(file_path, 'w') as outfile:
                json.dump(dict_data, outfile)
        logger.info("Dictionary data successfully written to transformed json file")
    except Exception as e:
        logger.fatal(f"Failed to write/append to json file : {e}")
        raise Exception("Failed to write/append to json file")


def write_to_json(dict_data, cmd_args):
    try:
        # Create/append json file for individual test
        system_name = platform.node()

        if "cis" in cmd_args.test_name.lower():
            # Get the json file name from file path
            json_file_name = os.path.split(cmd_args.path)[1]
            scan_test_filename = "transformed_" + json_file_name
            logger.info(f"Write to transformed json file : {scan_test_filename}")

            # Get the ip and system details from json file
            sys_details = json_file_name.split("_")
            system_name = sys_details[2] + "_" + sys_details[1]
            logger.info(f"system name details in format os name and IP : {system_name}")

        else:
            scan_test_filename = platform.node() + "_" + cmd_args.test_name.title().replace(" ", "") + ".json"
        add_data_to_json_file(dict_data, scan_test_filename)

        # Create/append json file for all test
        for each in dict_data:
            each['system_name'] = system_name
        add_data_to_json_file(dict_data, cmd_args.output)

    except Exception as e:
        logger.fatal(f"Failed to write to json file : {e}")
        raise Exception("Failed to write to json file")
