"""Module test to test function of the module annuaire.annuaire."""
import os
import unittest
from unittest import mock

from annuaire.annuaire.query import get_form_page, search

from config import settings


def mocked_requests_scrapping_form(*args, **kwargs):
    """
    Mock the get and post request.

    :param args:
    :param kwargs:
    :return:
    """
    class MockResponse:
        def __init__(self, json_data, status_code, url):
            self.content = json_data
            self.status_code = status_code
            self.url = url
            self.cookies = {"JSESSIONID": "jkghhjgjhgfjgfgjg"}
            self.encoding = "utf-8"

        def json(self):
            return self.json_data

    dn = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dn, "fixtures", "form.html"), "rb") as fp:
        return MockResponse(fp.read(), 200, args[0])


# This method will be used by the mock to replace requests.get

def mocked_requests_scrapping_get(*args, **kwargs):
    """
    Mock the get and post request.

    :param args:
    :param kwargs:
    :return:
    """
    class MockResponse:
        def __init__(self, json_data, status_code, url):
            self.content = json_data
            self.status_code = status_code
            self.url = url
            self.cookies = {"JSESSIONID": "jkghhjgjhgfjgfgjg"}
            self.encoding = "utf-8"

        def json(self):
            return self.json_data

    dn = os.path.dirname(os.path.realpath(__file__))
    for url, provider in {f"{settings.BASE_URL}/eAnnuaire/formulaire?appelRetour=true": "form",
                          f"{settings.BASE_URL}/eAnnuaire/resultat": "suivant",
                          f"{settings.BASE_URL}/eAnnuaire/fiche": "detail"}.items():
        if args[0].startswith(url):
            with open(os.path.join(dn, "fixtures", f"{provider}.html"), "rb") as fp:
                return MockResponse(fp.read(), 200, args[0])


def mocked_requests_scrapping_post(*args, **kwargs):
    """
    Mock the get and post request.

    :param args:
    :param kwargs:
    :return:
    """
    class MockResponse:
        def __init__(self, json_data, status_code, url):
            self.content = json_data
            self.status_code = status_code
            self.url = url
            self.cookies = {"JSESSIONID": "jkghhjgjhgfjgfgjg"}
            self.encoding = "utf-8"

        def json(self):
            return self.json_data

    dn = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dn, "fixtures", "result.html"), "rb") as fp:
        return MockResponse(fp.read(), 200, args[0])


def cookies(self):
    """
    Mock the cookie.

    :param self:
    :return:
    """
    return {
        "JSESSIONID": "test-value"
    }


class TestSearch(unittest.TestCase):
    """Class to test search function in the module collector.collector.crawler."""

    @mock.patch("requests.request", side_effect=mocked_requests_scrapping_form)
    @mock.patch("requests.utils.dict_from_cookiejar", side_effect=cookies)
    def test_get_form_page(self, mock_get, mock_cookie):
        """
        Test unknown source.

        :param mock_get:
        :return:
        """
        result = get_form_page()
        self.assertIn("raw", result)
        self.assertEqual(result["cookies"], {"JSESSIONID": "test-value"})

    @mock.patch("requests.get", side_effect=mocked_requests_scrapping_get)
    @mock.patch("requests.post", side_effect=mocked_requests_scrapping_post)
    @mock.patch("requests.utils.dict_from_cookiejar", side_effect=cookies)
    def test_search(self, mock_get, mock_post, mock_cookie):
        """
        Test search.

        :param mock_get:
        :param mock_post:
        :param mock_cookie:
        :return:
        """
        result = search("002", {"JSESSIONID": "test-value"})
        self.assertEqual(len(result), 14)

        expected_result = {"name": "LABADIE  SARAH",
                           "id": "10",
                           "barreau": "AGEN",
                           "cabinet": "MAITRE SARAH LABADIE",
                           "addresse": "88 boulevard de la liberte , residence pradines",
                           "cp": "47000",
                           "ville": "AGEN",
                           "téléphone": "0553984533",
                           "date_serment": "30/11/1971",
                           "mentions": None,
                           "language": "Français"}

        for k, v in result[0].items():
            self.assertIn(k, expected_result, msg=f"check key {k} is in result")
            self.assertEqual(v, expected_result[k], msg=f"check  {k}={v}")
