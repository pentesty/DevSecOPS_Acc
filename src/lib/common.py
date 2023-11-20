import configparser
import logging
import os

import rapidjson as json
import toml

log = logging.getLogger(__name__)


class Common:

    @staticmethod
    def read_ini_file(file_path: str) -> configparser:
        """Function to read any .ini file and return a parser object

        Args:
            file_path (str): Name of ini file in /modules/ui/object_repo

        Returns:
            (dict): JSON file in dictionary format.
        """
        full_file_path = f"{file_path}.ini"
        try:
            parser = configparser.ConfigParser()
            parser.read(full_file_path)
            return parser
        except Exception as e:
            raise Exception(f"Unable to read file {full_file_path}. Exception: {e}")

    @staticmethod
    def read_json_file(json_file: str) -> dict:
        """To convert json file to dictionary

        Args:
            json_file (str): Name of config_file in /tests/data/

        Returns:
            (dict): JSON file in dictionary format.
        """
        try:
            with open(Common.get_file_path(json_file)) as f:
                return json.load(f)
        except FileNotFoundError:
            with open(os.path.abspath(json_file)) as f:
                return json.load(f)

    @staticmethod
    def read_aws_testdata_json_file(json_file: str) -> dict:
        """To convert json file to dictionary

        Args:
            json_file (str): Name of config_file in /testdata/aws/

        Returns:
            (dict): JSON file in dictionary format.
        """
        try:
            with open(Common.get_aws_testdata_file_path(json_file)) as f:
                return json.load(f)
        except FileNotFoundError:
            with open(os.path.abspath(json_file)) as f:
                return json.load(f)

    @staticmethod
    def read_data_generator_json_file(json_file: str) -> dict:
        """To convert json file to dictionary

        Args:
            json_file (str): Name of config_file in /tests/data/

        Returns:
            (dict): JSON file in dictionary format.
        """
        try:
            with open(Common.get_data_generator_file_path(json_file)) as f:
                return json.load(f)
        except FileNotFoundError:
            with open(os.path.abspath(json_file)) as f:
                return json.load(f)

    @staticmethod
    def get_file_path(config_file: str) -> str:
        """Create Absolute filepath of given config file.

        Args:
            config_file (str): Name of config_file in /tests/data

        Returns:
            (str): Absolute filepath of given config file.
        """
        return os.path.join(Common.project_path(), "testdata/api", config_file)

    @staticmethod
    def get_aws_testdata_file_path(config_file: str) -> str:
        """Create Absolute file path of given config file.

        Args:
            config_file (str): Name of config_file in /tests/data

        Returns:
            (str): Absolute file path of given config file.
        """
        return os.path.join(Common.project_path(), "testdata/aws", config_file)

    @staticmethod
    def get_data_generator_file_path(config_file: str) -> str:
        """Create Absolute file path of given config file.

        Args:
            config_file (str): Name of config_file in /tests/data

        Returns:
            (str): Absolute file path of given config file.
        """
        return os.path.join(Common.project_path(), "testdata/data_generator", config_file)

    @staticmethod
    def set_config(dictionary: dict, config_file: str, absolute: bool = False) -> None:
        """Convert Dictionary to JSON File

        Args:
            dictionary (dict):
            config_file (dict): Python Dictionary to save to file.
            absolute (bool)
        """
        if absolute:
            with open(os.path.abspath(config_file), "w") as f:
                f.write(json.dumps(dictionary, indent=4))
        else:
            with open(Common.get_file_path(config_file), "w") as f:
                f.write(json.dumps(dictionary, indent=4))

    @staticmethod
    def get_toml_file(toml_file: str) -> dict:
        try:
            toml_dict = toml.load(Common.get_file_path(toml_file))
        except FileNotFoundError:
            toml_dict = toml.load(os.path.abspath(toml_file))

        log.debug(json.dumps(toml_dict, indent=4))
        return toml_dict

    @staticmethod
    def project_path():
        """ Get the project path for the current file"""
        try:
            project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            return project_path
        except Exception:
            raise Exception("Unable to get project path")

    @staticmethod
    def read_test_data_file(file_name):
        try:
            with open(os.path.join(Common.project_path(), "testdata/aws", file_name)) as f:
                return f.read()
        except FileNotFoundError:
            with open(os.path.abspath(file_name)) as f:
                return f.read()

    @staticmethod
    def get_a_file_path_from_aws_testdata(file_name):
        try:
            file_path = os.path.join(Common.project_path(), "testdata/aws", file_name)
            return file_path
        except FileNotFoundError:
            file_path = os.path.abspath(file_name)
            return file_path


if __name__ == "__main__":
    print(Common.read_json_file("config.json"))
