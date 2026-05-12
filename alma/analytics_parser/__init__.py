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

            if type(rows) is not list:
                rows = [rows] if rows else []

            for row in rows:
                if not isinstance(row, OrderedDict):
                    continue

                # Remove the integer column (assumed to be the first one, e.g. Column0)
                # But it's safer to just skip Column0 explicitly if it's there
                temp_row = OrderedDict()
                for column, column_value in row.items():
                    # Column names are like '{urn:schemas-microsoft-com:xml-analysis:rowset}Column1'
                    # or just 'Column1' depending on how xmljson handled it.
                    # We want to extract the number N from 'ColumnN'
                    match = re.search(r'Column(\d+)$', column)
                    if match:
                        col_index = int(match.group(1))
                        if col_index == 0:
                            continue  # Skip the integer column
                        
                        # col_index is 1-based for data columns
                        if 0 <= col_index - 1 < len(column_names):
                            temp_row[column_names[col_index - 1]] = column_value.get('$', '')
                        else:
                            # Log or ignore unexpected column index? 
                            # The original raised AlmaAnalyticsException
                            pass
                
                if temp_row:
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
