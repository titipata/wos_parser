import os
from wos_parser import parser as ps

# For compatibility with Py2.7
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


def rec_info_to_ris(records):
    """Parse wos_parser pub_info

    Parameters
    ==========
    * records: list, of WoS records parsed from XML

    Example
    ==========
    ```python
    import wos_parser

    records = wos_parser.read_xml_string(xml_string)

    parsed_recs = []
    for rec in records:
        parsed_recs.append(wos_parser.extract_pub_info(rec))

    ris_recs = wos_parser.rec_info_to_ris(parsed_recs)
    ```

    See Also
    ==========
    * wos_parser.read_xml
    * wos_parser.read_xml_string

    Returns
    ==========
    * list, of dicts representing RIS values
    """
    ris_entries = []
    for rec in records:
        pubinfo = ps.extract_pub_info(rec)

        authors = []
        author_fullnames = []
        for author in ps.extract_authors(rec):
            author_fullnames.append(author['full_name'])
            authors.append("{}, {}".format(author['last_name'],
                           author['first_name']))
        # End for

        ris_info = {}
        ris_info['AU'] = authors
        ris_info['AF'] = author_fullnames
        ris_info['TI'] = pubinfo['item']
        ris_info['AB'] = pubinfo['abstract']
        ris_info['SO'] = pubinfo['source']
        ris_info['LA'] = pubinfo['language']
        ris_info['DT'] = "{} {}".format(pubinfo['pubtype'], pubinfo['doctype'])
        ris_info['DE'] = pubinfo['keywords']
        ris_info['ID'] = pubinfo['keywords_plus']
        ris_info['PY'] = pubinfo['pubyear']
        ris_info['PD'] = pubinfo['sortdate']
        ris_info['UT'] = pubinfo['wos_id']

        if 'doi' in pubinfo:
            ris_info['DI'] = pubinfo['doi']
        elif 'xref_doi' in pubinfo:
            ris_info['DI'] = pubinfo['xref_doi']
        # End if

        ris_entries.append(ris_info)
    # End for

    return ris_entries
# End rec_info_to_ris()


def to_ris_text(entries):
    """
    Convert publication information from WoS XML to RIS format.

    Example
    ==========
    ```python
    ris_recs = wos_parser.rec_info_to_ris(parsed_recs)
    wos_parser.to_ris_text(ris_recs)
    ```

    See Also
    ==========
    * rec_info_to_ris

    Parameters
    ==========
    * entries: list, of WoS pubinfo dict entries in RIS format

    Returns
    ==========
    * str, representing publication info in RIS format
    """
    out = StringIO()

    # Markers to indicate WoS sourced RIS file
    out.write("FN Clarivate Analytics Web of Science\n")
    out.write("VR 1.0\n")

    for ent in entries:
        for k, v in ent.items():
            if isinstance(v, list):
                v = [i for i in v if i != ', ' and i is not None]
                v = "\n   ".join(v)
            out.write("{} {}\n".format(k, v))
        # End for
        out.write("ER\n\n")  # End of record marker
    # End for

    return out.getvalue()
# End to_ris_text()


def write_file(text, filename, ext='.txt', overwrite=False):
    """Write string to text file."""
    fn = '{}{}'.format(filename, ext)
    if not os.path.isfile(fn) or overwrite:
        with open(fn, 'w', encoding='utf-8') as outfile:
            outfile.write(text)
            outfile.flush()
    # End if
# End write_txt_file()
