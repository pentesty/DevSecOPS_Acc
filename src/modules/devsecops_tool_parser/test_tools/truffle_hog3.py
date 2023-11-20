import json
import logging

from dateutil import parser

logger = logging.getLogger()


class TruffleHog3:

    def __init__(self, cmd_args):
        self.test = "Trufflehog3 Scan"
        self.filepath = cmd_args.path

    def get_data(self):
        try:
            logger.info(self.filepath)
            with open(self.filepath, 'r') as json_file:
                file_data = json.load(json_file)
            list_rows = list()

            for json_data in file_data:
                if json_data.get("reason"):
                    row_data = self.get_dict_data(json_data)
                    list_rows.append(row_data)
                else:
                    raise ValueError("Format is not recognized for Trufflehog3")
            logger.debug(f"Print row data: {list_rows}")
            return list_rows
        except Exception as e:
            logger.fatal(f"Exception occurred in {__name__}.get_data() : {e}")
            raise Exception(f"Exception occurred in {__name__}.get_data() ")

    def get_dict_data(self, json_data):
        try:
            file = json_data["path"]
            reason = json_data["reason"]
            cwe_id = 798
            title = "Hard Coded " + reason + " in: " + file
            remediation = "Secrets and passwords should be stored in a secure vault and/or secure storage."

            parsed_date = parser.parse(json_data["date"]).date()
            logger.debug(f"Date retrieved from json file: {parsed_date}")

            description = f"[cwe-{cwe_id}] : "
            description += (
                "**Commit:** " + str(json_data.get("commit")).split("\n")[0] + "\n"
            )
            description += (
                "\n```\n"
                + str(json_data.get("commit")).replace("```", "\\`\\`\\`")
                + "\n```\n"
            )
            description += (
                "**Commit Hash:** " + str(json_data.get("commitHash")) + "\n"
            )
            description += "**Reason:** " + json_data["reason"] + "\n"
            description += "**Path:** " + file + "\n"

            severity = "High"
            if reason == "High Entropy":
                severity = "Info"
            elif "Oauth" in reason or "AWS" in reason or "Heroku" in reason:
                severity = "Critical"
            elif reason == "Generic Secret":
                severity = "Medium"

            strings_found = ""
            for string in json_data["stringsFound"]:
                strings_found += string + "\n"
            info = (strings_found[:4000] + '..') if len(strings_found) > 4000 else strings_found
            description += (
                "\n**Strings Found:**\n```\n" + info + "\n```\n"
            )

            dict_data = dict()
            dict_data["date"] = str(parsed_date)
            dict_data["cwe"] = cwe_id
            dict_data["test"] = self.test
            dict_data["severity"] = severity
            dict_data["title"] = title
            dict_data["remediation"] = remediation
            dict_data["description"] = description
            logger.debug(f"Print row data: {dict_data}")
            return dict_data
        except Exception as e:
            logger.fatal(f"Exception occurred in {__name__}.get_dict_data() : {e}")
            raise Exception(f"Exception occurred in {__name__}.get_dict_data() ")
