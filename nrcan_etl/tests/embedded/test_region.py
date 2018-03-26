from energuide.embedded import region


class TestRegion:

    def test_from_name(self):
        data = [
            'Ontario',
            'british columbia',
            'NOVA SCOTIA',
        ]
        output = [region.Region.from_data(row) for row in data]

        assert output == [
            region.Region.ONTARIO,
            region.Region.BRITISH_COLUMBIA,
            region.Region.NOVA_SCOTIA,
        ]

    def test_from_unknown_name(self):
        assert region.Region.from_data('foo') == region.Region.UNKNOWN

    def test_from_code(self):
        data = [
            'ON',
            'bc',
            'Ns',
        ]
        output = [region.Region.from_data(row) for row in data]
        assert output == [
            region.Region.ONTARIO,
            region.Region.BRITISH_COLUMBIA,
            region.Region.NOVA_SCOTIA,
        ]

    def test_from_unknown_code(self):
        assert region.Region.from_data('CA') == region.Region.UNKNOWN