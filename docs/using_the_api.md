[La version française suit.](#---------------------------------------------------------------------)

# Using the API!

## Introduction

This guide provides a quick overview on how to use the Graphql API to query open EnerGuide data. You
can find out more about Graphql at [graphql.org](https://graphql.org/).

All queries in this guide can be run at the [EnerGuide API Graphiql interface](http://energuideapi.ca/).
You're encouraged to test them out as you read along :tada:

You can find a list with descriptions of all the fields currently available to query in our
[API schema documentation](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-en.md).

## Basic queries

There are two basic ways to query data:

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

**Important note:** For simplicity's sake, this guide uses queries that don't specify
return subfields. This works with the GraphiQL interface because it auto fills
subfields if none are specified, but when working with other interfaces or writing your
own, you will need to specify which subfields you want returned in your query. For example:

```
query {
  dwelling(houseId:1420418){
    yearBuilt
    evaluations {
      eghRating {
        measurement
        upgrade
      }
    }
  }
}
```

```
query {
  dwellings {
    results {
      yearBuilt
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

## Filters, Comparators, Limits & Pagination

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
query. Filters are always **AND**, never **OR**, which means you can query all the dwellings built in Ottawa in 1970,
but you can't query all dwellings built in Ottawa or Toronto in 1970 (you would have to split this query in two).

**Important note:**  All filters work by looking for at least one matching value and then returning a matching
dwelling with all of its data. This means that even if you're applying a filter specific to evaluations, you
will still receive dwellings that contain that evaluation, along with all the other evaluations belonging to that
dwelling. This behavior should be kept in mind when using the API.

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

The comparator flag allows you to specify how you want your filter applied. Specifically, we let you use:

* greater than (gt)
* equal to (eq)
* less than (lt)

All filter values need to be passed in as strings. For example, to filter by the year `1970`, you would pass it as:

`dwellings(filters:[{field:dwellingYearBuilt comparator:eq value:"1970"}])`

You can also limit the number of results returned by your query using the `limit` flag. For example, lets say you wanted to fetch the first 30 dwellings of the
last query:

```
query {
  dwellings(limit:30 filters:[{field:dwellingForwardSortationArea comparator:eq value:"V5V"}, {field:evaluationHouseType comparator:eq value:"Single detached"}]) {
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

**Important note:** The limit applies to the dwellings returned, not evaluations. Since a dwelling can have multiple evaluations, you will likely receive more
than 30. The default limit set by the pagination is 50 dwellings. The maximum you can set the limit is 300 results.

If you want to access results from the next or previous set of paginated data, you can use the `next` or `previous` values from your query. For example if you query
the following:

```
query {
  dwellings {
    next
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

You'll get a result back that looks something like this:

```
"data": {
  "dwellings": {
    "next": "eyIkb2lkIjoiNWFiZjIxZDhlZTUzZWE1MmFiZmJjMjU3In0",
    "results": [
      {
        "evaluations":
        ...
      }
   }
}
```

To query the next set of paginated data, take the value from the `next` field and plug it into the query. In this example,
it would look like this:

```
query {
  dwellings(next: "eyIkb2lkIjoiNWFiZjIxZDhlZTUzZWE1MmFiZmJjMjU3In0") {
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

The results you receive will be for the next set of data.

Congratulations! Now you know how to filter, limit & navigate through your results :tada:

## Using the data with an application

There are a wide variety of ways to build applications that can talk to Graphql APIs! [How to Graphql](https://www.howtographql.com/) is a fantastic resource to check out. They provide a number of tutorials for building front end applications using data from a Graphql API. You can even learn how to build your own Graphql API if you're super keen.

## Have issues?

If you experience any issues with this guide, or using the API in general, please flag them in our [Github issues tracker](https://github.com/cds-snc/nrcan_api/issues).

## ---------------------------------------------------------------------

# Utilisation de l‘API!

##Introduction

Ce guide offre un bref aperçu sur la manière d’utiliser le Graphql d’API pour faire des requêtes sur les données du ÉnerGuide. Pour avoir plus de renseignements, veuillez consulter le site Web : [graphql.org](https://graphql.org) (anglais seulement).

Toutes les requêtes dans ce guide peuvent être exécutées à l’[interface de Graphiql de l’API pour l’ÉnerGuide](http://energuideapi.ca/). Vous êtes encouragés à les tester au fil de votre lecture. 

Vous pouvez trouver une liste avec des descriptions de tous les champs actuellement disponibles pour interroger notre [documentation du schéma de l’API](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-fr.md).

##Requêtes de base

Il existe deux manières fondamentales d’interroger des données :

1. Données sur un logement spécifique, en fournissant un houseId dans la requête.
```
query {
  dwelling(houseId:1420418)
}
```

2. Données sur un ensemble de logements
```
query {
  dwellings
}
```

Vous remarquerez que cette requête retourne uniquement un ensemble de résultats, avec des champs de next & previous. Puisque la base de données contient une grande quantité de données, l’API a été conçu pour retourner un ensemble de résultats paginé, qui améliore le rendement. Il y a plusieurs manières de filtrer les résultats que vous recevez, mais nous y reviendrons plus tard!
Remarque importante : Par souci de simplicité, ce guide utilise des requêtes qui ne spécifient pas le retour des sous-champs. Ceci marche avec l’interface de GraphiQL parce qu’il remplit automatiquement les sous-champs si aucun n’est spécifié, mais lorsqu’il travaille avec les autres interfaces ou si vous écrivez le vôtre, vous aurez besoin de spécifier quels sous-champs vous voulez retourner dans votre requête. Par exemple :
```
query {
  dwelling(houseId:1420418){
    yearBuilt
    evaluations {
      eghRating {
        measurement
        upgrade
      }
    }
  }
}
query {
  dwellings {
    results {
      yearBuilt
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

## Chercher les données au niveau du logement

En ajoutant des champs additionnels à votre requête, vous pouvez accéder aux données sur un logement. Par exemple, si vous voulez accéder la section du tri d’acheminement (forward sortation area) et l’année de construction (year built) d’un logement particulier, vous interrogeriez ce qui suit :
```
query {
  dwelling(houseId:1420418) {
    yearBuilt
    forwardSortationArea
  }
}
```

Pour les multiples requêtes de logement, les données sont stockées dans un champ de résultats (results). Pour y accéder, vous devriez faire une requête comme ceci :
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

## Chercher les données au niveau d’évaluation 

L’évaluation des données pour les logements peut être accessible par le champ evaluations. Ceci retournera une liste des évaluations pour un logement (ou des logements), étant donné qu’un logement peut avoir plusieurs évaluations.
Pour accéder à l’évaluation de données, vous feriez une requête comme ceci :
Logement individuel :
```
query {
  dwelling(houseId:1420418) {
    evaluations
  }
}
```
Logements multiples :
```
query {
  dwellings {
    results {
      evaluations
    }
  }
}
```
Vous pouvez aussi accéder aux champs d’évaluation précis dans votre requête. Par exemple, si vous avez voulu accéder au type de maison (house type) et l’émission de gaz des maisons vertes (green house gas emissions):
Logement individuel:
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
Logements multiples :
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

Vous devriez être capable maintenant d'accéder à tous les champs que vous voulez de l’API 

## Filtres, comparateurs, limites et mise en page automatique

L’API comprend des filtres pour aider à déterminer de façon précise les ensembles des données lors de l’interrogation pour les logements multiples. Vous pouvez enchaîner plusieurs filtres ensemble afin de limiter la recherche des résultats aussi précisément que vous l’aimeriez. Tous les champs filtrables sont documentés dans votre [documentation du schéma de l’API](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-fr.md).

Par exemple, si vous voulez récupérer la note egh (eghRating) pour les logements dans un forward sortation area précis, vous pouvez faire une requête comme ceci :
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
Disons que vous voulez un ensemble de données encore plus précis : l’eghRating pour tous les logements unifamiliaux détachés (Single detached) dans un forwardSortationArea précis. Vous pouvez ajouter un filtre additionnel à la requête initiale. Les filtres sont toujours ET, jamais OU, ce qui signifie que vous pouvez interroger tous les logements construits à Ottawa en 1970, mais vous ne pouvez pas interroger tous les logements construits à Ottawa ou Toronto en 1970 (vous devriez séparer cette requête en deux).
Remarque importante : tous les filtres fonctionnent en cherchant au moins une valeur correspondante et ensuite en retournant un logement correspondant avec toutes ses données. Ceci signifie que même si vous appliquez un filtre précis aux évaluations, vous recevrez toujours des logements qui contiennent cette évaluation, ainsi que toutes les autres évaluations appartenant à ce logement. Il faudrait toujours se rappeler cela lorsque vous utilisez l’API.
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
Le drapeau comparateur vous permet de spécifier la manière que vous voulez que le filtre soit appliqué. Pour être plus précis, nous vous laissons utiliser :
* supérieur à (sa)
* égale à (eg)
* inférieur à (ia)

Toutes les valeurs de filtres doivent être passées comme des chaines. Par exemple, pour filtrer par l’année 1970, vous le passeriez comme ceci :
dwellings(filters:[{field:dwellingYearBuilt comparator:eq value:"1970"}])
Vous pouvez aussi limiter le nombre de résultats retournés par votre requête en utilisant le drapeau limit. Par exemple, si vous voulez chercher les 30 premiers logements de la dernière requête :
```
query {
  dwellings(limit:30 filters:[{field:dwellingForwardSortationArea comparator:eq value:"V5V"}, {field:evaluationHouseType comparator:eq value:"Single detached"}]) {
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
Remarque importante : la limite s’applique aux logements retournés, et non aux évaluations. Puisqu’un logement peut avoir plusieurs évaluations, vous recevrez probablement plus de 30. La limite par défaut établie par la mise en page est de 50 logements. Le maximum que vous pouvez établir la limite est de 300 résultats.

Si vous voulez accéder aux résultats du prochain ou précédent ensemble des données de mise en pages, vous pouvez utiliser les valeurs suivant (next) ou précédent (previous) de votre requête. Par exemple, si vous interrogez les suivants :
```
query {
  dwellings {
    next
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
Vos résultats ressembleront à ceci :
```
"data": {
  "dwellings": {
    "next": "eyIkb2lkIjoiNWFiZjIxZDhlZTUzZWE1MmFiZmJjMjU3In0",
    "results": [
      {
        "evaluations":
        ...
      }
   }
}
```
Pour interroger le prochain ensemble de données de mise en page, veuillez prendre la valeur du champ next et l’intégrer dans la requête. Dans cet exemple, cela ressemblera à ceci :
```
query {
  dwellings(next: "eyIkb2lkIjoiNWFiZjIxZDhlZTUzZWE1MmFiZmJjMjU3In0") {
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
Les résultats que vous recevez seront pour le prochain ensemble de données.

Félicitations! Maintenant vous connaissez la façon de filtrer, limiter et naviguer vos résultats

## Utilisation des données avec une application 

Il existe diverses manières de concevoir des applications qui peuvent communiquer aux API du Graphql! [How To Graphql](https://www.howtographql.com/) (anglais seulement) est une ressource fantastique de vérifier. Ils fournissent de nombreux tutoriels pour la conception d’applications frontales en utilisation des données d’un API du Graphql. Vous pouvez aussi apprendre à concevoir votre propre API du Graphql, si vous êtes vraiment passionné.

## Avez-vous des questions?

Si vous rencontrez des problèmes avec ce guide, ou en utilisant l'API en général, veuillez les signaler dans notre [Système de suivi des questions de Github](https://github.com/cds-snc/nrcan_api/issues).
