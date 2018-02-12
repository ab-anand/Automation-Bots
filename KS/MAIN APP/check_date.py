import pytz
import date_extractor

text = "need to get two signatures."
dates = date_extractor.extract_dates(text)

print (dates)

