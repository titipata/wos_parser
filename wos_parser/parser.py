from lxml import etree

def get_record(filehandle):
    """Iteratively go through file and get text of each WoS record"""
    record = ''
    flag = False
    for line in filehandle:
        if not flag and not line.startswith('<REC'):
            continue
        flag = True
        record = record + line
        if line.strip().endswith('</REC>'):
            return record
    return None

def read_xml(path_to_xml, verbose=True):
    """
    Read XML file and return full list of records in element tree

    Parameters
    ==========
    path_to_xml: str, full path to WoS XML file
    verbose: boolean, True if we want to print number of records parsed
    """
    records = list()
    count = 0
    with open(path_to_xml, 'r') as file:
        while True:
            record = get_record(file)
            count += 1
            try:
                rec = etree.fromstring(record)
                records.append(rec)
            except:
                pass
            if verbose:
                if count % 5000 == 0: print('read total %i records' % count)
            if not record:
                break
    return records

def extract_wos_id(elem):
    """Return WoS id from given element tree"""
    if elem.find('UID') is not None:
        wos_id = elem.find('UID').text
    else:
        wos_id = ''
    return wos_id

def extract_authors(elem):
    """Extract list of authors from given element tree"""
    wos_id = extract_wos_id(elem)
    authors = list()
    names = elem.findall('./static_data/summary/names/')
    for name in names:
        dais_id = name.attrib.get('dais_id', '')
        seq_no = name.attrib.get('seq_no', '')
        role = name.attrib.get('role', '')
        if name.find('full_name') is not None:
            full_name = name.find('full_name').text
        else:
            full_name = ''
        if name.find('first_name') is not None:
            first_name = name.find('first_name').text
        else:
            first_name = ''
        if name.find('last_name') is not None:
            last_name = name.find('last_name').text
        else:
            last_name = ''
        author = {'dais_id': dais_id,
                  'seq_no': seq_no,
                  'role': role,
                  'full_name': full_name,
                  'first_name': first_name,
                  'last_name': last_name}
        author.update({'wos_id': wos_id})
        authors.append(author)
    return authors

def extract_keywords(elem):
    """Extract keywords and keywords plus each separated by semicolon"""
    keywords = elem.findall('./static_data/fullrecord_metadata/keywords/keyword')
    keywords_plus = elem.findall('./static_data/item/keywords_plus/keyword')
    if keywords:
        keywords_text = '; '.join([keyword.text for keyword in keywords])
    else:
        keywords_text = ''
    if keywords_plus:
        keywords_plus_text = '; '.join([keyword.text for keyword in keywords_plus])
    else:
        keywords_plus_text = ''
    return keywords_text, keywords_plus_text
