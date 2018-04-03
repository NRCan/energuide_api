# Adding AIR50P and UGRAIR50PA to ETL
AIR50P: This field provides the result of the blower door Air Changes per Hour (ACH) @ 50 Pa.

## Adding to Extract

### `nrcan_etl/src/energuide/extractor.py`
Add "AIR50P" and "UGRAIR50PA" to the NULLABLE_FIELDS list

```
NULLABLE_FIELDS = [
    ...
    'AIR50P',
    'UGRAIR50PA',
    ...
]
```

### `nrcan_etl/tests/test_extractor.py`
Add example data elements to the dictionary returned in the `base_data` function
```
    {
        ...
        'AIR50P': '8.7962',
        'UGRAIR50PA': '8.215',
        ...
    }
```

### `nrcan_etl/tests/test_cli.py`
Add example data elements to the dictionary returned in the `data1` function
```
    {
        ...
        'AIR50P': '8.7962',
        'UGRAIR50PA': '8.215',
        ...
    }
```

Commit and push your changes, and make a Pull Request

## Adding to Transform

### `nrcan_etl/src/energuide/dwelling.py`
1. Add a new property to `_ParsedDwellingDataRow` for the air leakage

This class is a container for all the fields at both the dwelling and evaluation levels.
The input data is parsed into this container at the beginning of the process so the rest of the pipeline has a dependable known structure to use.
```
class _ParsedDwellingDataRow(typing.NamedTuple):
    ...
    air_leakage: measurement.Measurement
    ...

```

2. Add new elements to the `_SCHEMA` directionary in the `Dwelling` class.
This is a description of each data element for validation and very simple processing purposes.
`type`: the datatype that the element will be
`nullable`: specificies that while the key must be present, it's value is allowed to be `None`
`coerce`: A function to pass the value through before the type check, for simple transformations such as data type casting

```
    _SCHEMA = {
        ...
        'AIR50P': {'type': 'float', 'nullable': True, 'coerce': float},
        'UGRAIR50PA':  {'type': 'float', 'nullable': True, 'coerce': float},
        ...
    }
```

3. Add new elements to constructor call of `ParsedDwellingDataRow` in the class method `Dwelling.from_row`

```
        return ParsedDwellingDataRow(
            ...
            air_leakage=measurement.Measurement(
                measurement=parsed['AIR50P'],
                upgrade=parsed['UGRAIR50PA'],
            )
            ...
        )
```

4. Add new property to `_Evaluation`

```
class _Evaluation(typing.NamedTuple):
    ...
    air_leakage: measurement.Measurement
    ...
```

5. Add new element to constructor call of `Evaluation` in the class method `Evaluation.from_data`

```
        return Evaluation(
            ...
            air_leakage=data.air_leakage,
            ...
        )
```

### `nrcan_etl/tests/test_dwelling.py`
1. Add example data elements to the dictionary returned by the `sample_input_d` function

```
    return {
        ...
        'AIR50P': '8.7962',
        'UGRAIR50PA': '8.215',
        ...
    }
```

2. Add elements to the contructor call of `ParsedDwellingDataRow` in the test method `TestParsedDwellingDataRow.from_row`

```

        assert output == dwelling.ParsedDwellingDataRow(
            ...
            air_leakage=measurement.Measurement(
                measurement=8.7962,
                upgrade=8.215,
            )
            ...
```

Commit and push your changes, and make a Pull Request

## Adding to Load

### `nrcan_etl/src/energuide/dwelling.py`

Add new element to the dict returned by `Evaluation.to_dict`

```
        return {
            ...
            'airLeakage': self.air_leakage.to_dict(),
            ...
        }
```

### `nrcan_etl/tests/test_dwelling.py`

Add new element to the dict in `TestDwellingEvaluation.test_to_dict`
```
        assert output == {
            ...
            'airLeakage': {
                'measurement': 8.7962,
                'upgrade': 8.215,
            },
            ...
        }
```


Commit and push your changes, and make a Pull Request