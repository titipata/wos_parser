import requests
import wos_parser
import hashlib

example_XML_loc = 'https://raw.githubusercontent.com/yadudoc/wos_builder/master/sample.xml'

# Grab sample XML file
r = requests.get(example_XML_loc)
xml_string = r.text
records = wos_parser.read_xml_string(xml_string)

def test_convert_pubinfo_ris():
    expected = "FN Clarivate Analytics Web of Science"

    ris_entries = wos_parser.rec_info_to_ris(records)
    ris_string = wos_parser.to_ris_text(ris_entries)

    assert ris_string[0:37] == expected, \
        """
        WoS identifer string not found!
        Expected: {}
        Got: {}
        """.format(ris_string[0:36], expected)

def test_expected_md5():
    """
    Test converted RIS text string by comparing against
    an expected hash value.

    The hash value was generated with the process below.

    ```python
    import hashlib
    example_XML_loc = 'https://raw.githubusercontent.com/yadudoc/wos_builder/master/sample.xml'

    # Grab sample XML file
    r = requests.get(example_XML_loc)
    xml_string = r.text
    records = wos_parser.read_xml_string(xml_string)

    ris_entries = wos_parser.rec_info_to_ris(records)
    ris_string = wos_parser.to_ris_text(ris_entries)

    tmp = hashlib.md5(ris_string.encode())
    hashstr = tmp.hexdigest()
    ```
    """
    # Expected md5 hash
    matching_md5 = 'd7d3bda08dea1f846d2ed6932977bc2a'

    ris_entries = wos_parser.rec_info_to_ris(records)
    ris_string = wos_parser.to_ris_text(ris_entries)

    tmp = hashlib.md5(ris_string.encode())
    hashstr = tmp.hexdigest()

    assert hashstr == matching_md5, "md5 hash of RIS string did not match!"
