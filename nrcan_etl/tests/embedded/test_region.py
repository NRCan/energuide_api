from energuide.embedded import region


class TestRegion:

    def test_from_name(self):
        data = [
            'Ontario',
            'british columbia',
            'NOVA SCOTIA',
            'ALBERTA',
            'SASKATCHEWAN',
            'MANITOBA',
            'QUEBEC',
            'NEW_BRUNSWICK',
            'PRINCE_EDWARD_ISLAND',
            'NEWFOUNDLAND_AND_LABRADOR',
            'YUKON',
            'NORTHWEST_TERRITORIES',
            'NUNAVUT',
        ]
        output = [region.Region.from_data(row) for row in data]

        assert output == [
            region.Region.ONTARIO,
            region.Region.BRITISH_COLUMBIA,
            region.Region.NOVA_SCOTIA,
            region.Region.ALBERTA,
            region.Region.SASKATCHEWAN,
            region.Region.MANITOBA,
            region.Region.QUEBEC,
            region.Region.NEW_BRUNSWICK,
            region.Region.PRINCE_EDWARD_ISLAND,
            region.Region.NEWFOUNDLAND_AND_LABRADOR,
            region.Region.YUKON,
            region.Region.NORTHWEST_TERRITORIES,
            region.Region.NUNAVUT,
        ]

    def test_from_unknown_name(self):
        assert region.Region.from_data('foo') == region.Region.UNKNOWN

    def test_from_accent(self):
        assert region.Region.from_data('QUÉBEC') == region.Region.QUEBEC

    def test_from_code(self):
        data = [
            'bC',
            'AB',
            'sk',
            'MB',
            'on',
            'Qc',
            'NB',
            'pE',
            'NS',
            'NL',
            'Yt',
            'NT',
            'nU',
        ]

        output = [region.Region.from_data(row) for row in data]
        assert output == [
            region.Region.BRITISH_COLUMBIA,
            region.Region.ALBERTA,
            region.Region.SASKATCHEWAN,
            region.Region.MANITOBA,
            region.Region.ONTARIO,
            region.Region.QUEBEC,
            region.Region.NEW_BRUNSWICK,
            region.Region.PRINCE_EDWARD_ISLAND,
            region.Region.NOVA_SCOTIA,
            region.Region.NEWFOUNDLAND_AND_LABRADOR,
            region.Region.YUKON,
            region.Region.NORTHWEST_TERRITORIES,
            region.Region.NUNAVUT,
        ]

    def test_from_unknown_code(self):
        assert region.Region.from_data('CA') == region.Region.UNKNOWN