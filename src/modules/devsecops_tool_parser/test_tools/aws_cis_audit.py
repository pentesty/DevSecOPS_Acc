import json
import logging
import datetime
from datetime import date

logger = logging.getLogger()


class AWSCISAudit:

    def __init__(self, cmd_args):
        self.test = cmd_args.test_name
        self.filepath = cmd_args.path

    def get_data(self):
        try:
            logger.info("Entered AWS CIS Audit")
            logger.info(self.filepath)
            with open(self.filepath, 'r') as json_file:
                file_data = json.load(json_file)
            list_rows = list()

            today = date.today()
            logger.debug(f"Today's date is: {today}")

            # Returns the report date
            input_format = '%Y%m%d'
            parsed_date = file_data["account_info"]["date"].split('-')[0]
            report_date = (datetime.datetime.strptime(parsed_date, input_format)).date()
            logger.debug(f"Date retrieved from json file: {report_date}")

            # As aws cis audit test does not report cwe/severity, we are marking it as Unknown
            cwe_id = "Unknown"
            severity = "Unknown"

            for each_data in file_data["report"]:
                dict_data = dict()
                title = each_data["check"]
                logger.debug(f"Title : {title}")

                remediation = each_data["check"]
                logger.debug(f"Remediation info: {remediation}")

                description = self.get_description_data(each_data["data"])

                if description:
                    dict_data["date"] = str(report_date)
                    dict_data["cwe"] = cwe_id
                    dict_data["test"] = self.test
                    dict_data["severity"] = severity
                    dict_data["title"] = title
                    dict_data["remediation"] = remediation
                    dict_data["description"] = description

                    logger.debug(f"Print row data: {dict_data}")
                    list_rows.append(dict_data)
            logger.debug(f"Print row data: {list_rows}")
            return list_rows
        except Exception as e:
            logger.fatal(f"Exception occurred in {__name__}.get_data() : {e}")
            raise Exception(f"Exception occurred in {__name__}.get_data() ")

    def get_description_data(self, each_data, description=""):
        try:
            if type(each_data) == list:
                for each in each_data:
                    description = self.get_description_data(each, description)

            elif each_data["type"] == "WARNING":
                description += each_data["value"]
                description += "\n"

                logger.debug(f"Print row data: {description}")
            return description

        except Exception as e:
            logger.fatal(f"Exception occurred in {__name__}.get_dict_data() : {e}")
            raise Exception(f"Exception occurred in {__name__}.get_dict_data() ")
