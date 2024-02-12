import re


def adjust_connection_url(connection_url: str) -> str:
    """Adjust connection url to be compatible.

    Args:
        connection_url (str): connection url

    Returns:
        str: adjusted connection url

    """
    prog = re.compile("(.*)(://.*)")
    result = prog.match(connection_url)
    protocol = "mysql+pymysql"

    if result:
        return f"{protocol}{result.group(2)}"

    return f"{protocol}://{connection_url}"
