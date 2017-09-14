"""
This serves as function wrapper. This formats the incoming request data and
passes it to the actual function.

DO NOT MODIFY.
"""
import main


def lambda_wrap(event, context):
    if type(event) == dict:
        return main.main(**event)
    elif type(event) == list:
        return main.main(*event)
