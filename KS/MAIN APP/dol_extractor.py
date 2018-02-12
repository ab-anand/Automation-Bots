import pytz
import date_extractor

def extract_dol(lines):
	'''take list as input
	break it into lines and 
	extract date from each lines 
	if present
	'''

	dates_arr = []
	for line in lines:
		dates = date_extractor.extract_dates(line)
		for date in dates:
					dates_arr.append(date.date())

	return dates_arr

# TEST CASE
# text = "need to get two signatures.DoL: 9 feb 1986 with accident yesterday dOL: 19 feb, 2019"
# for i in extract_dol(text):
# 		print i



