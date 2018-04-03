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

    def test_alternative_name(self):
        data = [
            'YUKON_TERRITORY',
            'NORTHWEST_TERRITORY',
        ]

        output = [region.Region.from_data(row) for row in data]

        assert output == [
            region.Region.YUKON,
            region.Region.NORTHWEST_TERRITORIES,
        ]

    def test_from_unknown_name(self):
        assert region.Region.from_data('foo') == region.Region.UNKNOWN


    def test_fuzzy_names(self):
        data = [
            'Qubec',
            'ONT',
            'Ontarioq',
            'Quibec',
            'Yukon Terr.',
            'Queebc',
            'Manitobal',
            'Aberta'
        ]
        output = [region.Region.from_data(row) for row in data]

        assert output == [
            region.Region.QUEBEC,
            region.Region.ONTARIO,
            region.Region.ONTARIO,
            region.Region.QUEBEC,
            region.Region.YUKON,
            region.Region.QUEBEC,
            region.Region.MANITOBA,
            region.Region.ALBERTA
        ]

    def test_french_name(self):
        data = [
            'Colombie-Britannique',
            'Terre-Neuve-et-Labrador',
            'Nouveau-Brunswick',
            'Nouvelle-Écosse',
            'Territoires du Nord-Ouest',
            'Île-du-Prince-Édouard',
        ]
        output = [region.Region.from_data(row) for row in data]

        assert output == [
            region.Region.BRITISH_COLUMBIA,
            region.Region.NEWFOUNDLAND_AND_LABRADOR,
            region.Region.NEW_BRUNSWICK,
            region.Region.NOVA_SCOTIA,
            region.Region.NORTHWEST_TERRITORIES,
            region.Region.PRINCE_EDWARD_ISLAND,
        ]

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

    def test_alternative_code(self):
        data = [
            'PEI',
            'NWT',
        ]
        output = [region.Region.from_data(row) for row in data]
        assert output == [
            region.Region.PRINCE_EDWARD_ISLAND,
            region.Region.NORTHWEST_TERRITORIES,
        ]

    def test_from_unknown_code(self):
        assert region.Region.from_data('CA') == region.Region.UNKNOWN