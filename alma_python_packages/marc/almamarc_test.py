import unittest
import alma_marc


almamarc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><bib><mms_id>990001434230503831</mms_id><record_format>marc21</record_format><linked_record_id/><title>Testboken : så testas systemen /</title><author>żŻ</author><network_numbers><network_number>(LIBRIS)990001434230503831</network_number><network_number>(LIBRIS)54738695</network_number><network_number>(Aleph)000143423JUL01</network_number></network_numbers><date_of_publication>2003</date_of_publication><holdings link="https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/990001434230503831/holdings"/><created_by>import</created_by><created_date>2017-09-05Z</created_date><last_modified_by>exl_api</last_modified_by><last_modified_date>2019-03-20Z</last_modified_date><suppress_from_publishing>true</suppress_from_publishing><originating_system>ILS</originating_system><originating_system_id>000143423-JUL01</originating_system_id><cataloging_level desc="Default Level">00</cataloging_level><record><leader>00771nam  2200265 a 4500</leader><controlfield tag="001">990001434230503831</controlfield><controlfield tag="005">20190320132831.0</controlfield><controlfield tag="008">030321s2003    sw            000 0 swe d</controlfield><datafield ind1=" " ind2=" " tag="035"><subfield code="a">(Aleph)000143423JUL01</subfield></datafield><datafield ind1=" " ind2=" " tag="035"><subfield code="a">(LIBRIS)54738695</subfield></datafield><datafield ind1=" " ind2=" " tag="035"><subfield code="a">(LIBRIS)990001434230503831</subfield></datafield><datafield ind1="0" ind2=" " tag="041"><subfield code="a">swe</subfield></datafield><datafield ind1=" " ind2=" " tag="082"><subfield code="a">025.4310715</subfield><subfield code="b">23/swe [MAPPED]</subfield></datafield><datafield ind1="0" ind2=" " tag="130"><subfield code="a">Huvuduppslag - uniform titel</subfield></datafield><datafield ind1="0" ind2="0" tag="245"><subfield code="a">Testboken :</subfield><subfield code="b">så testas systemen /</subfield><subfield code="c">Eva Törnblom</subfield></datafield><datafield ind1=" " ind2=" " tag="260"><subfield code="c">2003</subfield></datafield><datafield ind1=" " ind2="7" tag="650"><subfield code="a">Evas andra hänvisning</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="650"><subfield code="a">Evas testterm (153)</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="650"><subfield code="a">Evas headertest</subfield><subfield code="2">jon</subfield></datafield><datafield ind1="1" ind2=" " tag="700"><subfield code="a">żŻ</subfield></datafield><datafield ind1=" " ind2=" " tag="900"><subfield code="a">BK</subfield></datafield><datafield ind1=" " ind2="7" tag="953"><subfield code="a">Evas andra hänvisning</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="953"><subfield code="a">Evas testterm (153)</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="953"><subfield code="a">Evas headertest</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2=" " tag="999"><subfield code="a">54738695</subfield></datafield></record></bib>'
normalmarc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><record><leader>00771nam  2200265 a 4500</leader><controlfield tag="001">990001434230503831</controlfield><controlfield tag="005">20190320132831.0</controlfield><controlfield tag="008">030321s2003    sw            000 0 swe d</controlfield><datafield ind1=" " ind2=" " tag="035"><subfield code="a">(Aleph)000143423JUL01</subfield></datafield><datafield ind1=" " ind2=" " tag="035"><subfield code="a">(LIBRIS)54738695</subfield></datafield><datafield ind1=" " ind2=" " tag="035"><subfield code="a">(LIBRIS)990001434230503831</subfield></datafield><datafield ind1="0" ind2=" " tag="041"><subfield code="a">swe</subfield></datafield><datafield ind1=" " ind2=" " tag="082"><subfield code="a">025.4310715</subfield><subfield code="b">23/swe [MAPPED]</subfield></datafield><datafield ind1="0" ind2=" " tag="130"><subfield code="a">Huvuduppslag - uniform titel</subfield></datafield><datafield ind1="0" ind2="0" tag="245"><subfield code="a">Testboken :</subfield><subfield code="b">så testas systemen /</subfield><subfield code="c">Eva Törnblom</subfield></datafield><datafield ind1=" " ind2=" " tag="260"><subfield code="c">2003</subfield></datafield><datafield ind1=" " ind2="7" tag="650"><subfield code="a">Evas andra hänvisning</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="650"><subfield code="a">Evas testterm (153)</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="650"><subfield code="a">Evas headertest</subfield><subfield code="2">jon</subfield></datafield><datafield ind1="1" ind2=" " tag="700"><subfield code="a">żŻ</subfield></datafield><datafield ind1=" " ind2=" " tag="900"><subfield code="a">BK</subfield></datafield><datafield ind1=" " ind2="7" tag="953"><subfield code="a">Evas andra hänvisning</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="953"><subfield code="a">Evas testterm (153)</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2="7" tag="953"><subfield code="a">Evas headertest</subfield><subfield code="2">jon</subfield></datafield><datafield ind1=" " ind2=" " tag="999"><subfield code="a">54738695</subfield></datafield></record>'



def strip_white_space(string):
    return string.replace(' ', '').replace('\t', '').replace('\n', '')


class RecordSetup(unittest.TestCase):

    def setUp(self):
        self.record = alma_marc.AlmaMARCRecord(almamarc_xml)

    def test_load_not_alma_marc(self):
        with self.assertRaises(alma_marc.AlmaMARCException):
            alma_marc.AlmaMARCRecord(normalmarc_xml)

    def test_that_input_is_same_as_output(self):
        record = alma_marc.AlmaMARCRecord(almamarc_xml)
        self.assertEqual(strip_white_space(record.to_string()), strip_white_space(almamarc_xml))

    def test_that_attributes_is_dict(self):
        self.assertTrue(isinstance(self.record.attributes, dict))

    def test_for_attributes_length(self):
        self.assertEqual(len(self.record.attributes), 16)


class Fields(unittest.TestCase):

    record = alma_marc.AlmaMARCRecord(almamarc_xml)

    def test_adding__and_removing_fields(self):
        tag = 'test'

        # First add a field and test if it was added
        self.record.add_field(tag=tag, subfields={'a': 'test_a'})
        self.assertEqual(self.record.get_fields(tag=tag)[0].get_subfield('a').value, 'test_a')

        # Then remove the field and see if it was removed
        self.record.remove_fields(tag=tag)
        self.assertEqual(len(self.record.get_fields(tag=tag)), 0)

        # Add multiple fields and then remove them and see if they are gone.

        self.record.add_field(tag=tag, subfields={'a': 'test_c'})
        self.record.add_field(tag=tag, subfields={'a': 'test_c'})
        self.record.remove_fields(tag=tag)
        self.assertEqual(len(self.record.get_fields(tag=tag)), 0)


class Subfields(unittest.TestCase):

    record = alma_marc.AlmaMARCRecord(almamarc_xml)


if __name__ == '__main__':
    unittest.main()
