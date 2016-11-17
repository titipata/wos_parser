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
        addr_no = name.attrib.get('addr_no', '')
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
                  'addr_no': addr_no,
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

def extract_addresses(elem):
    """Give element tree of WoS, return list of addresses"""
    address_dict_all = list()
    wos_id = extract_wos_id(elem)
    addresses = elem.findall('./static_data/fullrecord_metadata/addresses/address_name')
    for address in addresses:
        address_dict = dict()
        address_spec = address.find('address_spec')
        addr_no = address_spec.attrib.get('addr_no', '')
        for tag in ['city', 'state', 'country', 'zip', 'full_address']:
            if address_spec.find(tag) is not None:
                address_dict[tag] = address_spec.find(tag).text
            else:
                address_dict[tag] = ''
        if address_spec.find('organizations') is not None:
            organizations = '; '.join([oraginization.text for oraginization in address_spec.find('organizations')])
        else:
            organizations = ''
        if address_spec.find('suborganizations') is not None:
            suborganizations = '; '.join([s.text for s in address_spec.find('suborganizations')])
        else:
            suborganizations = ''
        address_dict.update({'wos_id': wos_id,
                             'addr_no': addr_no,
                             'organizations': organizations,
                             'suborganizations': suborganizations})
        address_dict_all.append(address_dict)
    return address_dict_all

def extract_publisher(elem):
    """Extract publisher details"""
    wos_id = extract_wos_id(elem)
    publisher_list = list()
    publishers = elem.findall('./static_data/summary/publishers/publisher')
    for publisher in publishers:
        publisher_dict = dict()
        name = publisher.find('names/name')
        for tag in ['display_name', 'full_name']:
            if name.find(tag) is not None:
                publisher_dict[tag] = name.find(tag).text
            else:
                publisher_dict[tag] = ''
        addr = publisher.find('address_spec')
        for tag in ['full_address', 'city']:
            if addr.find(tag) is not None:
                publisher_dict[tag] = addr.find(tag).text
            else:
                publisher_dict[tag] = ''
        publisher_dict.update({'wos_id': wos_id})
        publisher_list.append(publisher_dict)
    return publisher_list

def extract_pub_info(elem):
    """Extract publication information from WoS"""

    pub_info_dict = dict()
    pub_info_dict.update({'wos_id': extract_wos_id(elem)})

    pub_info = elem.find('.static_data/summary/pub_info').attrib
    for key in ['sortdate', 'has_abstract', 'pubtype', 'pubyear', 'pubmonth', 'issue']:
        if key in pub_info.keys():
            pub_info_dict.update({key: pub_info[key]})
        else:
            pub_info_dict.update({key: ''})

    for title in elem.findall('./static_data/summary/titles/title'):
        if title.attrib['type'] in ['source', 'item']:
            # more attribute includes source_abbrev, abbrev_iso, abbrev_11, abbrev_29
            title_dict = {title.attrib['type']: title.text}
            pub_info_dict.update(title_dict)

    language = elem.find('./static_data/fullrecord_metadata/languages/language')
    if language.tag is not None:
        pub_info_dict.update({'language': language.text})
    else:
        pub_info_dict.update({'language': ''})

    heading_tag = elem.find('./static_data/fullrecord_metadata/category_info/headings/heading')
    if heading_tag is not None:
        heading = heading_tag.text
    else:
        heading = ''
    pub_info_dict.update({'heading': heading})

    subheading_tag = elem.find('./static_data/fullrecord_metadata/category_info/subheadings/subheading')
    if subheading_tag is not None:
        subheading = subheading_tag.text
    else:
        subheading = ''
    pub_info_dict.update({'subheading': subheading})

    doctype_tag = elem.find('./static_data/summary/doctypes/doctype')
    if doctype_tag is not None:
        doctype = doctype_tag.text
    else:
        doctype = ''
    pub_info_dict.update({doctype_tag.tag: doctype})

    abstract_tag = elem.findall('./static_data/fullrecord_metadata/abstracts/abstract/abstract_text/p')
    if len(abstract_tag) > 0:
        abstract = ' '.join([p.text for p in abstract_tag])
    else:
        abstract = ''
    pub_info_dict.update({'abstract': abstract})

    keywords, keywords_plus = extract_keywords(elem)
    pub_info_dict.update({'keywords': keywords,
                          'keywords_plus': keywords_plus})

    return pub_info_dict

def extract_funding(elem):
    """Extract funding text and funding agency separated by semicolon from WoS
    if see no funding, it will return just Web of Science id and empty string
    """
    wos_id = extract_wos_id(elem)
    grants = elem.findall('./static_data/fullrecord_metadata/fund_ack/grants/grant')
    fund_text_tag = elem.find('./static_data/fullrecord_metadata/fund_ack/fund_text')
    if fund_text_tag is not None:
        fund_text = ' '.join([p_.text for p_ in fund_text_tag.findall('p')])
    else:
        fund_text = ''

    grant_list = list()
    for grant in grants:
        if grant.find('grant_agency') is not None:
            grant_list.append(grant.find('grant_agency').text)

    return {'wos_id': wos_id,
            'funding_text': fund_text,
            'funding_agency': '; '.join(grant_list)}

def extract_conferences(elem):
    """Extract list of conferences from given WoS element tree
    if no conferences exist, return None"""
    conferences_list = list()
    wos_id = extract_wos_id(elem)
    conferences = elem.findall('./static_data/summary/conferences/conference')

    for conference in conferences:
        conference_dict = dict()
        conf_title_tag = conference.find('conf_titles/conf_title')
        if conf_title_tag is not None:
            conf_title = conf_title_tag.text
        else:
            conf_title = ''

        conf_date_tag = conference.find('conf_dates/conf_date')
        if conf_date_tag is not None:
            conf_date = conf_date_tag.text
        else:
            conf_date = ''
        for key in ['conf_start', 'conf_end']:
            if key in conf_date_tag.attrib.keys():
                conference_dict.update({key: conf_date_tag.attrib[key]})
            else:
                conference_dict.update({key: ''})

        conf_city_tag = conference.find('conf_locations/conf_location/conf_city')
        conf_city = conf_city_tag.text if conf_city_tag is not None else ''

        conf_state_tag = conference.find('conf_locations/conf_location/conf_state')
        conf_state = conf_state_tag.text if conf_state_tag is not None else ''

        conf_sponsor_tag = conference.findall('sponsors/sponsor')
        if len(conf_sponsor_tag) > 0:
            conf_sponsor = '; '.join([s.text for s in conf_sponsor_tag])
        else:
            conf_sponsor = ''

        conf_host_tag = conference.find('./conf_locations/conf_location/conf_host')
        conf_host = conf_host_tag.text if conf_host_tag is not None else ''

        conference_dict.update({'wos_id': wos_id,
                                'conf_title': conf_title,
                                'conf_date': conf_date,
                                'conf_city': conf_city,
                                'conf_state': conf_state,
                                'conf_sponsor': conf_sponsor,
                                'conf_host': conf_host})

        conferences_list.append(conference_dict)
    if not conferences_list:
        conferences_list = None
    return conferences_list
