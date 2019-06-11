import re


def parse_result(src):
    """
    Parse the result page and convert to json format
    :param html_result:
    :return:
    """
    res = []
    tmp = {}
    for i, item in enumerate(src.xpath("//table[@class='shadow-details-2']/tr/td")):
        if not item.text or not item.text.strip():
            if len(item.xpath('.//a')) == 1:
                tmp['name'] = item.xpath('.//a')[0].text.strip()
                m = re.search('identifiantAvocat=(\d+)', item.xpath('.//a')[0].attrib['href'])
                tmp['id'] = m.group(1)
            if len(item.xpath('.//a') )== 3 and tmp:
                res.append(tmp)
                tmp = {}
            continue

        m = re.search("([A-Z\s]+)\s,\s*(\d*\s.*)\s-\s(\d+)\s([\w\s]+)", item.text.strip())
        if m:
            tmp['cabinet'] = m.group(1).strip()
            tmp['addresse'] = m.group(2).strip()
            tmp['cp'] = m.group(3).strip()
            tmp['ville'] = m.group(4).strip()
        else:
            ro = re.compile(r"([\w\s]+)\s:\s(\w+|\+?\d+)", re.UNICODE)
            for m in ro.finditer(item.text.strip()):
                tmp[m.group(1).strip().lower()] = m.group(2).strip()
    return res


def parse_detail(src):
    """
    Parse the detail page and convert to json format with extra fields
    :param src:
    :return:
    """
    res = []
    for i, item in enumerate(src.xpath("//table[@class='shadow-details-2']/tr/td")):
        if not item.text or not item.text.strip():
            continue
        res.append(re.sub(r'\n\t*', ' ', item.text.strip()))
    tmp = '@@@@'.join(res)
    tmp = tmp.replace(':@@@@', ': ')
    m = re.search('Date de prestation de serment :\s+(\d+\s*\/\s+\d+\s*\/\s+\d+)\s*@@@@', tmp)
    m1 = re.search('Mention\(s\) de spécialisation :\s*(.*)\s*@@@@', tmp)
    m2 = re.search('Langue\(s\) :\s*(\w+)\s*', tmp)
    return {
        'date_serment': m.group(1).replace(' ','') if m else None,
        'mentions': m1.group(1) if m1 else None,
        'language': m2.group(1) if m2 else None,
    }
