from io import StringIO
import pytest
from energuide import extractor


@pytest.fixture
def csv_string():
    return '''EVAL_ID,EVAL_TYPE,ENTRYBY,CLIENTPCODE,CLIENTNAME,TELEPHONE,\
MAIL_PCODE,TAXNUMBER,RAW_XML\n123,D,Fred Johnson,M5E 1W5,John \
Fredson,999 999 9999,M5E 1W5,999999999999,<tag>thing</tag>'''


def test_extract(csv_string: str):
    with StringIO() as file_in:
        file_in.write(csv_string)
        file_in.seek(0)

        output = extractor.extract(file_in)
        item = dict(next(output))

        assert item == {
            'EVAL_ID': '123',
            'EVAL_TYPE': 'D',

            'FORWARDSORTATIONAREA':'M5E'
        }
