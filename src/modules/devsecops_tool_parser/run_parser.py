import json
import logging
import os
import platform
import sys

# setting src path
sys.path.append("../../../src")
print(sys.path)

from lib.devsecops_tool_parser import parse_arguments, write_to_csv, write_to_json
from lib.logger import Log
from modules.devsecops_tool_parser.test_tools.truffle_hog3 import TruffleHog3
from modules.devsecops_tool_parser.test_tools.zap_scan import ZapScan
from modules.devsecops_tool_parser.test_tools.dependency_check import DependencyCheck
from modules.devsecops_tool_parser.test_tools.cis_audit import CISAudit
from modules.devsecops_tool_parser.test_tools.aws_cis_audit import AWSCISAudit


def run_parser(command_args):
    try:
        # Convert and replace test output filename with titlecase
        parser_class = command_args.test_name.title().replace(" ", "")
        logging.info(f"Tool parser class to run : {parser_class}")

        # Create an object of tool parser class
        parser_scan_output = None

        if parser_class.lower() == "zapscan":
            parser_scan_output = ZapScan(command_args)
        elif parser_class.lower() == "trufflehog3scan":
            parser_scan_output = TruffleHog3(command_args)
        elif parser_class.lower() == "dependencycheckscan":
            parser_scan_output = DependencyCheck(command_args)
        elif "cis-audit" in parser_class.lower():
            parser_scan_output = CISAudit(command_args)
        elif parser_class.lower() == "awscisaudit":
            parser_scan_output = AWSCISAudit(command_args)
        else:
            logging.fatal("No tool specified. Please provide correct arguments.")
            raise Exception("No tool specified. Please provide correct arguments.")

        # get data from test tool parser and convert to csv
        get_dict_data = parser_scan_output.get_data()
        logging.info("run_parser completed successfully.")
        return get_dict_data

    except Exception as e:
        logging.fatal(f"Exception occurred in run_parser : {e}")
        raise Exception(f"Exception occurred in run_parser ")


def configure_logger(input_file):
    # Create logs folder if not already present in a4mation directory
    log_path = "../../../logs"
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_filename = log_path + os.sep + input_file["log_filename"]

    logger = Log()

    if input_json["log_level"].lower() == "info":
        logger.logfile(log_filename, log_level=logging.INFO)
    else:
        logger.logfile(log_filename, log_level=logging.DEBUG)

    logging.info(f"logging level set to {input_file['log_level']}")
    logging.info(f"logger file path and name : {log_filename}")


if __name__ == "__main__":
    # Load input json file
    json_input_filepath = "../../testdata/devsecops_tool_parser/config.json"
    with open(json_input_filepath, 'r') as json_file:
        input_json = json.load(json_file)

    configure_logger(input_json)

    # Parse command line arguments
    cmd_args = parse_arguments()

    logging.info(f"System name : {platform.node()}")
    logging.info(f"Tool name : {cmd_args.test_name}")
    logging.info(f"Input file json or xml : {cmd_args.path}")
    logging.info(f"csv/json output file : {cmd_args.output}")

    # Parse the data and create csv
    get_dict_data_from_parser = run_parser(cmd_args)

    if "csv" in cmd_args.output.lower():
        write_to_csv(get_dict_data_from_parser, cmd_args, input_json)
    else:
        write_to_json(get_dict_data_from_parser, cmd_args)

    logging.info("===========================================")
