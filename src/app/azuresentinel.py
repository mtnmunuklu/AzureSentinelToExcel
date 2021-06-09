
import os
import glob
import yaml
import logging
from src.app.logger import Logger
from src.config import Config
from xlwt import Workbook, XFStyle, Font, Borders, Alignment

class AzureSentinel:
    """
    Used for sigma converter operations
    """
    rules = list()


    def __init__(self):
        """
        Constructor Method
        :param: none
        :return: none
        """
        self.file_directory = Config.FILE_DIRECTORY
        self.file_format = Config.FILE_FORMAT
        self.output = Config.OUTPUT
        self.logger = Logger('AzureSentinel')

    def read_from_file(self):
        """
        Used for read packets in given directory
        :param: none
        :return: none
        """
        try:
            for file_path in glob.iglob(self.file_directory + self.file_format, recursive=True):
                if os.path.exists(file_path):
                    self.parse_yml(file_path)
        except Exception as e:
            self.logger.log(logging.WARNING, "File read error")
            self.logger.log(logging.ERROR, e)

    def parse_yml(self, file_path):
        """
        Used for parse xml file
        :param file_path: yaml file path
        :type file_path: str
        :return: none
        """
        try:
            with open(file_path, encoding="utf8") as file:
                doc = yaml.safe_load(file)
                self.rules.append(doc)
        except Exception as e:
                self.logger.log(logging.WARNING, "YML parse error")
                self.logger.log(logging.ERROR, e)

    def write_to_excel(self):
        """
        Used for write sigma rules to excel
        :param: none
        :return: none
        """
        try:
        # Workbook is created 
            wb = Workbook()
            column_style = self.set_style_column("Arial", 200, True)

            sheet1 = wb.add_sheet('Rules')
            sheet1.write(0, 0, "ID", column_style) #id
            sheet1.write(0, 1, "Name", column_style) #name
            sheet1.write(0, 2, "Description", column_style) #description
            sheet1.write(0, 3, "Severity", column_style) #severity
            sheet1.write(0, 4, "Connector ID - Data Types", column_style) #connectorId:dataTypes
            sheet1.write(0, 5, "Tactics", column_style) #tactics
            sheet1.write(0, 6, "Techniques", column_style) #relevantTechniques
            sheet1.write(0, 7, "Query", column_style) #query

            index = 1
            for rule in self.rules:
                print(str(rule))
                if rule.get("id"):
                    id = rule.get("id")
                    sheet1.write(index, 0, str(id))
                if rule.get("name"):
                    name = rule.get("name")
                    sheet1.write(index, 1, str(name))
                if rule.get("description"):
                    description = rule.get("description").strip().strip("'")
                    sheet1.write(index, 2, str(description))
                if rule.get("severity"):
                    severity = rule.get("severity")
                    sheet1.write(index, 3, str(severity))
                if rule.get("requiredDataConnectors"):
                    requiredDataConnector = ", ".join("{} - {}".format(requiredDataConnector.get("connectorId"),
                    requiredDataConnector.get("dataTypes")) for requiredDataConnector in rule.get("requiredDataConnectors"))
                    sheet1.write(index, 4, str(requiredDataConnector))
                if rule.get("tactics"):
                    tactics = ", ".join(tactic for tactic in rule.get("tactics"))
                    sheet1.write(index, 5, str(tactics))
                if rule.get("relevantTechniques"): 
                    techniques = ", ".join(technique for technique in rule.get("relevantTechniques"))
                    sheet1.write(index, 6, str(techniques))
                if rule.get("query"):
                    query = rule.get("query")
                    sheet1.write(index, 7, str(query))
                index += 1

            wb.save(self.output)
        except Exception as e:
                self.logger.log(logging.WARNING, "Excel create error")
                self.logger.log(logging.ERROR, e)

        
    def set_style_column(self, name, height, bold=False):
        """
        Used to set style of excel
        :param name: font name
        :type name: str
        :param height: font height
        :type height: str
        :return: excel style
        :rtype: XFStyle
        """
        style = XFStyle()
        font = Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

