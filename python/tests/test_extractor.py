from io import StringIO
import typing
import pytest
from energuide import extractor


@pytest.fixture
def csv_string():
    return '''EVAL_ID,EVAL_TYPE,HOUSEREGION,WEATHERLOC,ENTRYBY,CLIENTCITY,CLIENTPCODE,CLIENTNAME,TELEPHONE,MAIL_CITY,MAIL_REGION,MAIL_PCODE,TAXNUMBER,RAW_XML
123,D,Ontario,somewhere,Fred Johnson,Toronto,M5E 1W5,John Fredson,999 999 9999,Toronto,Ontario,M5E 1W5,999999999999,<tag>thing</tag>'''



def test_extract(csv_string: str): 
    with StringIO() as file_in:
        file_in.write(csv_string)
        file_in.seek(0)

        output = extractor.extract(file_in)
        item = dict(next(output))

        assert item == {
            'EVAL_ID': '123',
            'EVAL_TYPE': 'D',

            'HOUSEREGION': 'Ontario',
            'WEATHERLOC': 'somewhere',
            'CLIENTCITY': 'Toronto',
            'MAIL_CITY': 'Toronto',
            'MAIL_REGION': 'Ontario',
            'FORWARDSORTATIONAREA':'M5E'
        }
