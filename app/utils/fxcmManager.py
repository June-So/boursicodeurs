from SECRET import FXCMY_ACCESS_TOKEN,  FXCMY_SERVER
import fxcmpy


def connect_fxcm():
    """ connection API fxcmpy """
    connection = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server=FXCMY_SERVER)
    return connection
