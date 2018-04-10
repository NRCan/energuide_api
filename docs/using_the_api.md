# Using the API!

## Introduction

This guide provides a quick overview on how to use the Graphql API to query open EnerGuide data. You
can find out more about Graphql at [graphql.org](https://graphql.org/).

All queries in this guide can be run at the [EnerGuide API Graphiql interface](http://energuideapi.ca/).
You're encouraged to test them out as you read along :tada:

You can find a list with descriptions of all the fields currently available to query in our
[API schema documentation](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-en.md).

## Basic queries

There are two basic ways to fetch data:

1. Data about a specific dwelling, by providing a houseId in the query

```
query {
  dwelling(houseId:1420418)
}
```

2. Data about a set of dwellings

```
query {
  dwellings
}
```

You'll notice this query only returns a set of results, with `next` & `previous`
fields. Since the database contains a large amount of data, the API was built
to return a paginated set of results, which improves performance. There are
various ways to filter the results you receive, but more on that later!

## Fetch dwelling level data

By adding additional fields to your query, you can access data about a dwelling.
For example, if you wanted to access the `forward sortation area` and `year built`
of a specific dwelling, you would query the following:

```
query {
  dwelling(houseId:1420418) {
    yearBuilt
    forwardSortationArea
  }
}
```

For the multiple dwelling query, the data is stored in a `results` field. To
access it, you would query the following:

```
query {
  dwellings {
    results {
      yearBuilt
      forwardSortationArea
    }
  }
}
```

## Fetch evaluation level data

Evaluation data for dwellings can be accessed via the `evaluations` field. This
will return a list of evaluations for a dwelling (or dwellings), since a dwelling
can have multiple evaluations.

To access evaluation data, you would query the following:

Single dwelling:

```
query {
  dwelling(houseId:1420418) {
    evaluations
  }
}
```

Multiple dwellings:

```
query {
  dwellings {
    results {
      evaluations
    }
  }
}
```

You can also access specific evaluation fields in your query. For example if you
wanted to access `house type` and `green house gas emissions`:

Single dwelling:

```
query {
  dwelling(houseId:1420418) {
    evaluations {
      houseType
      greenhouseGasEmissions
    }
  }
}
```

Multiple dwellings:

```
query {
  dwellings {
    results {
      evaluations {
        houseType
        greenhouseGasEmissions
      }
    }
  }
}
```

You should now be able to access any field you want from the API :tada:

## Filters

The API includes filters to help narrow down data sets when querying for multiple
dwellings. You can chain multiple filters together to narrow down the results
as specifically as you would like. All filterable fields are documented in our
in our [API schema documentation](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-en.md).

For example, if you want to retrieve the `eghRating` for dwellings in a specific `forward sortation area`, you
can query the following:

```
query {
  dwellings(filters:[{field:dwellingForwardSortationArea comparator:eq value:"V5V"}]) {
    results {
      forwardSortationArea
      evaluations {
        eghRating
      }
    }
  }
}
```

Lets say you want an even more specific set of data: the `eghRating` for all the `Single detached`
dwellings in a specific `forwardSortationArea`. You can add an additional filter to the original
query:

```
query {
  dwellings(filters:[{field:dwellingForwardSortationArea comparator:eq value:"V5V"}, {field:evaluationHouseType comparator:eq value:"Single detached"}]) {
    results {
      forwardSortationArea
      evaluations {
        eghRating {
          measurement
          upgrade
        }
      }
    }
  }
}
```

And that's how filters work :tada:

## Using the data with an application

There are a wide variety of ways to build applications that can talk to Graphql APIs! [How to Graphql](https://www.howtographql.com/) is a fantastic resource to check out. They provide a number of
tutorials for building front end applications using data from a Graphql API. You can even learn how to
build your own Graphql API if you're super keen.

## Have issues?

If you experience any issues with this guide, or using the API in general, please flag them in our [Github issues tracker](https://github.com/cds-snc/nrcan_api/issues).
