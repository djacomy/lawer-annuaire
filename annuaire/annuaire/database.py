"""Module database."""
import logging

from config import settings

from tinydb import Query, TinyDB

logger = logging.getLogger(__name__)

DB = TinyDB(settings.DB_PATH)


def get_references(ref):
    """
    Get references from the database.

    :param ref:
    :return:
    """
    table = DB.table(ref)
    return table.all()


def poplulate_references(table_name, options):
    """
    Populate references by table name.

    :param table_name: table name
    :param options:  list xml Element
    :return: void
    """
    logger.info("[start] populate {0}".format(table_name))
    table = DB.table(table_name)
    ref = Query()
    for item in [{"name": item.text, "code": item.attrib["value"]} for item in options
                 if item.attrib["value"] != "nonRenseigne"]:
        table.upsert(item, ref.code == item.get("code"))
    logger.info("[end] populate {0}".format(table_name))


def populate_lawyers(items):
    """
    Populate lawyers by list.

    :param items:
    :return:
    """
    table = DB.table("layers")
    layer = Query()
    for item in items:
        item.pop("id", None)
        item.pop("detail_url", None)
        table.upsert(item, layer.name == item.get("name"))


def get_all_barreaux():
    """
    Get all barreaux.

    :return:
    """
    table = DB.table("barreau")
    return {b.get("code"): b.get("name") for b in table.all()}


def export_lawyers():
    """
    Export all lawyers in csv format.

    :return:
    """
    table = DB.table("layers")
    headers = ["barreau", "name", "cabinet", "addresse", "cp", "ville", "télécopie", "téléphone", "date_serment",
               "language", "mentions"]
    data = [
        headers
    ]
    for b in table.all():
        data.append([b.get(field) for field in headers])
    return data
