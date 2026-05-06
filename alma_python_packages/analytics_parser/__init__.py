import xmljson
from xml.etree.ElementTree import fromstring
import re
from collections import OrderedDict


class AlmaAnalyticsException(Exception):
    """Custom docstring"""


class AlmaAnalyticsParser:

    def __init__(self, i):
        def __parse_analytics__(xml_string):
            urn_schema = '{urn:schemas-microsoft-com:xml-analysis:rowset}'
            w3_schema = '{http://www.w3.org/2001/XMLSchema}'

            raw_data = xmljson.badgerfish.data(fromstring(xml_string))

            def __get_column_names__():
                snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')

                column_names = \
                raw_data['report']['QueryResult']['ResultXml'][urn_schema + 'rowset'][w3_schema + 'schema'][
                    w3_schema + 'complexType'][w3_schema + 'sequence'][w3_schema + 'element']

                temp_column_names = []
                for column in column_names[1:]:  # Remove first column since its just the integer
                    for attribute, attribute_value in column.items():
                        if attribute == '@{urn:saw-sql}columnHeading':
                            temp_column_names.append(
                                snake_case_pattern.sub('_', attribute_value).lower().replace(' ', ''))

                return temp_column_names

            def __get_rows__():
                try:
                    return raw_data['report']['QueryResult']['ResultXml'][urn_schema + 'rowset'][urn_schema + 'Row']
                except KeyError:
                    return []

            column_names = __get_column_names__()
            temp_table = []
            rows = __get_rows__()
            if type(rows) is list:  # More than one item in the list
                for row in __get_rows__():
                    row.popitem(last=False)  # Remove the integer column
                    temp_row = OrderedDict()
                    iter = 0
                    for column, column_value in row.items():
                        try:
                            temp_row[column_names[int(column[-1:])-1]] = column_value['$']
                        except ValueError:
                            raise (AlmaAnalyticsException('Failed to load column number'))

                    temp_table.append(temp_row)
            elif type(rows) is OrderedDict:
                rows.popitem(last=False)  # Remove the integer column
                temp_row = OrderedDict()
                iter = 0
                for column, column_value in rows.items():
                    try:
                        temp_row[column_names[iter]] = column_value['$']
                        iter = iter + 1
                    except ValueError:
                        raise (AlmaAnalyticsException('Failed to load column number'))

                temp_table.append(temp_row)

            return temp_table

        self.list = __parse_analytics__(i)

    def get_table(self):
        return self.list

    def get_column(self, column_name):
        temp_list = []
        try:
            for row in self.list:
                temp_list.append(row[column_name])
            return temp_list
        except IndexError:
            return None
