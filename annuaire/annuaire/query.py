"""Query module."""
import logging
import os

from annuaire.annuaire.exception import AnnuaireException
from annuaire.annuaire.parser import parse_detail, parse_result

from config import settings

from lxml import html

import requests

base_url = settings.BASE_URL

log = logging.getLogger(__name__)


def get_form_page():
    """
    Get form page and cookies.

    :return:
    """
    cookie_name = "JSESSIONID"
    url = "{0}/eAnnuaire/formulaire?appelRetour=true".format(base_url)
    response = requests.request("GET", url)
    if response.status_code != 200:
        raise Exception(response.content)
    return {
        "raw": html.fromstring(response.content),
        "cookies": {cookie_name: requests.utils.dict_from_cookiejar(response.cookies)[cookie_name]}
    }


def search(barreau_code, cookies, output=None):
    """
    Extract lawyers from result page and detail page.

    :param barreau_code:
    :param cookies:
    :param output:
    :return:
    """
    params = {
        "form": "formulaireRecherche",
        "barreau": barreau_code,
        "nomAvocat": "",
        "prenomAvocat": "",
        "ville": "",
        "codePostal": ""
    }
    data = "&".join(["{0}={1}".format(k, v) for k, v in params.items()])
    i = 1
    res = _get_result(data, cookies)
    if output:
        # store result to debug
        with open(os.path.join(output, "page{0}.html".format(i)), "wb") as fp:
            fp.write(html.tostring(res))

    items = _analyse_result(res, cookies)

    tmp = [item.attrib["href"] for item in res.xpath("//a[@href='/eAnnuaire/resultats?suivant=true']")]
    while tmp:
        res = _follow(cookies)

        if output:
            # store result to debug
            with open(os.path.join(output, "page{0}.html".format(i)), "wb") as fp:
                fp.write(html.tostring(res))

        items += _analyse_result(res, cookies)
        tmp = [item.attrib["href"] for item in res.xpath("//a[@href='/eAnnuaire/resultats?suivant=true']")]
        i += 1
    return items


def _analyse_result(res, cookies, output=None):
    """
    Parse result page then get extra fields after getting and parsing detail page for each found lawyers.

    :param res:
    :param cookies:
    :param output:
    :return:
    """
    new_items = parse_result(res)
    for item in new_items:
        try:
            tmp = _get_detail(item["id"], cookies)
            if output:
                # store result to debug
                with open(os.path.join(output, "{0}.html".format(item["id"])), "wb") as fp:
                    fp.write(html.tostring(tmp))
            res = parse_detail(tmp)
            item.update(res)
        except AnnuaireException as e:
            log.warning("ERR: {0}".format(e.message))
    return new_items


def _get_result(data, cookies):
    """
    Get the result page.

    :param data:
    :param cookies:
    :return:
    """
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Origin": "https://annuaire.avocat.fr",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image"
                  "/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://annuaire.avocat.fr/eAnnuaire/formulaire?appelRetour=true",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    url = "{0}/eAnnuaire/resultats".format(base_url)
    response = requests.post(url,
                             data=data,
                             headers=headers,
                             cookies=cookies)
    if response.status_code != 200:
        raise AnnuaireException(response.reason)
    if not response.content:
        raise AnnuaireException(f"empty response: {url}")
    return html.fromstring(response.content)


def _second_request(url, cookies):
    """
    Do a second request from the result page.

    :param url:
    :param cookies:
    :return:
    """
    headers = {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/"
                  "webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://annuaire.avocat.fr/eAnnuaire/resultats",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url,
                            headers=headers,
                            cookies=cookies)
    if response.status_code != 200:
        raise AnnuaireException(response.reason)
    if not response.content:
        raise AnnuaireException(f"empty response: {url}")
    return html.fromstring(response.content)


def _follow(cookies):
    """
    Get the next page.

    :param cookies:
    :return:
    """
    url = f"{base_url}/eAnnuaire/resultats?suivant=true"
    return _second_request(url, cookies)


def _get_detail(item_id, cookies):
    """
    Get the detail page.

    :param item_id:
    :param cookies:
    :return:
    """
    url = f"{base_url}/eAnnuaire/fiche?identifiantAvocat={item_id}"
    return _second_request(url, cookies)
