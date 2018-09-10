import requests
import wos_parser

example_XML_loc = 'https://raw.githubusercontent.com/yadudoc/wos_builder/master/sample.xml'

# Grab sample XML file
r = requests.get(example_XML_loc)
xml_string = r.text

def test_read_xml_string():
    expected_num_records = 50
    records = wos_parser.read_xml_string(xml_string)
    assert len(records) == expected_num_records, \
        "Mismatch in number of records, got {}, expected {}".format(len(records), expected_num_records)

def test_read_xml_string_limit():
    expected_num_records = 25
    records = wos_parser.read_xml_string(xml_string, n_records=expected_num_records)
    assert len(records) == expected_num_records, \
        "Mismatch in number of records, got {}, expected {}".format(len(records), expected_num_records)
