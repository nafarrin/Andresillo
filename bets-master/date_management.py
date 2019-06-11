import string
import re
import datetime
import pendulum

aliases = {
    "jun":["6"],
    "ago":["8"],
    "sep": ["9"]
}




def cleanBothEnds (string_2_clean):
  working_string = string_2_clean
  if not working_string.isprintable():
    working_string = working_string.lstrip()
    working_string = working_string.rstrip()
  return working_string

def excel_date(date1):
    temp = datetime.datetime(1899, 12, 30)  # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)