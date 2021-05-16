import netifaces

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # Recieves 4096 bytes each time step.

ERROR = "0"
SUCCESS = "1"

PROMPT_MESSAGE = "PomptMessage"
LIST_MESSAGE = "ListMessage"
FILE_MESSAGE = "FileMessage"


def default_route_ip():
    """
    Returns the first ip address on the interface
    associated with the default route.
    """
    # Name of the default interface.
    iface = netifaces.gateways()["default"][netifaces.AF_INET][1]
    return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["addr"]
