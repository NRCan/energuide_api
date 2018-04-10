# Schema Types

<details>
  <summary><strong>Table of Contents</strong></summary>

  * [Query](#query)
  * [Objects](#objects)
    * [Dwelling](#dwelling)
    * [Evaluation](#evaluation)
    * [Insulation](#insulation)
    * [PaginatedResultSet](#paginatedresultset)
    * [Rating](#rating)
    * [Upgrade](#upgrade)
    * [Wall](#wall)
    * [WallMeasurement](#wallmeasurement)
  * [Enums](#enums)
    * [Comparator](#comparator)
    * [DateField](#datefield)
    * [Field](#field)
  * [Scalars](#scalars)
    * [Boolean](#boolean)
    * [Date](#date)
    * [Float](#float)
    * [Int](#int)
    * [String](#string)

</details>

## Query 
Le type de requête racine

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>dwelling</strong></td>
<td valign="top"><a href="#dwelling">Dwelling</a></td>
<td>

Détails pour un logement donné

</td>
</tr>
<tr>
<td colspan="2" align="right" valign="top">houseId</td>
<td valign="top"><a href="#int">Int</a>!</td>
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>dwellings</strong></td>
<td valign="top"><a href="#paginatedresultset">PaginatedResultSet</a></td>
<td>

Détails pour tous les logements, pouvant être triés par une ou plusieurs valeurs

</td>
</tr>
<tr>
<td colspan="2" align="right" valign="top">filters</td>
<td valign="top">[<a href="#filter">Filter</a>!]</td>
<td></td>
</tr>
<tr>
<td colspan="2" align="right" valign="top">dateRange</td>
<td valign="top"><a href="#daterange">DateRange</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" align="right" valign="top">limit</td>
<td valign="top"><a href="#int">Int</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" align="right" valign="top">next</td>
<td valign="top"><a href="#string">String</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" align="right" valign="top">previous</td>
<td valign="top"><a href="#string">String</a></td>
<td></td>
</tr>
</tbody>
</table>

## Objects

### Dwelling

Un immeuble résidentiel évalué dans le cadre du programme ÉnerGuide

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>houseId</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

Numéro d'identification unique d'un logement

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>yearBuilt</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

Année de construction

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>city</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Nom de la ville où se trouve le logement

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>region</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Région du pays où se trouve le logement (province ou territoire)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>forwardSortationArea</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Les trois premiers caractères d'un code postal canadien correspondant à une zone géographique définie par Postes Canada

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>evaluations</strong></td>
<td valign="top">[<a href="#evaluation">Evaluation</a>]</td>
<td>

Une liste d'évaluation des caractéristiques spécifiques du logement

</td>
</tr>
</tbody>
</table>

### Evaluation

Informations détaillées sur les caractéristiques spécifiques d'un logement donné

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>evaluationType</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Les codes de types d'évaluation sont utilisés pour définir le type d'évaluation effectuée et pour distinguer le type d'habitation (c'est-à-dire nouvelle construction ou existante

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>entryDate</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Date de l'évaluation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>fileId</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Champ composé avec l'organisme de service, conseiller et évaluation avec la version

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>houseType</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type de maison

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>creationDate</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Date de création du dossier

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>modificationDate</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Dernière modification du dossier

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>energyUpgrades</strong></td>
<td valign="top">[<a href="#upgrade">Upgrade</a>]</td>
<td>

Une liste d'améliorations qui augmentent l'efficacité énergétique

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heatedFloorArea</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Surface de plancher chauffé en m2

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>ersRating</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td>

La cote EnerGuide calculée pour cette évaluation, en GJ

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>eghRating</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td>

[plus valide] La cote ÉnerGuide calculée aux fins de l’évaluation 

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>greenhouseGasEmissions</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td>

Cote liée aux émissions de gaz à effet de serre en tonnes/an

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>energyIntensity</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td>

Calculé comme Surface de plancher chauffé/Cote ERS, unités de GJ/m2

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>walls</strong></td>
<td valign="top"><a href="#wall">Wall</a></td>
<td>

Entrée de données pour les murs d’un logement 

</td>
</tr>
</tbody>
</table>

### Insulation

Matériau utilisé pour isoler quelque chose 

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>percentage</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

La proportion de l’élément total que représente l’isolation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>rValue</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

La valeur R de l’isolation de l’élément 

</td>
</tr>
</tbody>
</table>

### PaginatedResultSet

Une page de résultats

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>hasNext</strong></td>
<td valign="top"><a href="#boolean">Boolean</a></td>
<td>

Si 'true', une autre page de résultats peut être générée

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>hasPrevious</strong></td>
<td valign="top"><a href="#boolean">Boolean</a></td>
<td>

Si true', une page précédente de résultats peut être générée

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>next</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Identifiant utilisé pour générer la prochaine page de résultats

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>previous</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Curseur d'identification utilisé pour générer la page précédente de résultats

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>results</strong></td>
<td valign="top">[<a href="#dwelling">Dwelling</a>]</td>
<td>

Une liste de logements

</td>
</tr>
</tbody>
</table>

### Rating

Une valeur R pour un champ donné 

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>measurement</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Valeur de la cote calculée aux fins de cette évaluation 

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>upgrade</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Valeur de la cote de l’amélioration proposée calculée aux fins de cette évaluation 

</td>
</tr>
</tbody>
</table>

### Upgrade

Une amélioration qui pourrait augmenter l'efficacité énergétique du logement

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>upgradeType</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Partie du logement à améliorer

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>cost</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

Coût estimatif de l'amélioration

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>priority</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

Ordre d'importance de l'amélioration recommandée (plus le chiffre est petit, plus la priorité est élevée)

</td>
</tr>
</tbody>
</table>

### Wall

Les murs séparent l'espace intérieur chauffé de l'extérieur (les cloisons intérieures ne sont pas considérées comme des murs)

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>measurement</strong></td>
<td valign="top"><a href="#wallmeasurement">WallMeasurement</a></td>
<td>

Mesures des murs calculées aux fins de cette évaluation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>upgrade</strong></td>
<td valign="top"><a href="#wallmeasurement">WallMeasurement</a></td>
<td>

Mesures des murs liées à l’amélioration proposée calculées aux fins de cette évaluation

</td>
</tr>
</tbody>
</table>

### WallMeasurement

Mesures des murs calculées aux fins de cette évaluation

<table>
<thead>
<tr>
<th align="left">Field</th>
<th align="right">Argument</th>
<th align="left">Type</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" valign="top"><strong>insulation</strong></td>
<td valign="top">[<a href="#insulation">Insulation</a>]</td>
<td>

Description de l'isolation des murs

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heatLost</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Pertes de chaleur par les murs en MJ

</td>
</tr>
</tbody>
</table>

## Enums

### Comparator

Un opérateur indiquant comment les résultats seront triés

<table>
<thead>
<th align="left">Value</th>
<th align="left">Description</th>
</thead>
<tbody>
<tr>
<td valign="top"><strong>gt</strong></td>
<td>

Supérieur à : génère 'true' pour les résultats supérieurs à la valeur de comparaison

</td>
</tr>
<tr>
<td valign="top"><strong>lt</strong></td>
<td>

Inférieur à : génère 'true' pour les résultats inférieurs à la valeur de comparaison

</td>
</tr>
<tr>
<td valign="top"><strong>eq</strong></td>
<td>

Égal à : génère 'true' pour les résultats égaux à la valeur de comparaison

</td>
</tr>
</tbody>
</table>

### DateField

Une valeur de date ISO, formatée "AAAA-MM-JJ"

<table>
<thead>
<th align="left">Value</th>
<th align="left">Description</th>
</thead>
<tbody>
<tr>
<td valign="top"><strong>evaluationEntryDate</strong></td>
<td>

Trier les résultats par les logements contenant au moins une évaluation avec une date d'entrée spécifique

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationCreationDate</strong></td>
<td>

Trier les résultats par les logements contenant au moins une évaluation avec une date de création d'enregistrement spécifique

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationModificationDate</strong></td>
<td>

Trier les résultats par les logements contenant au moins une évaluation avec une date de modification d'enregistrement spécifique

</td>
</tr>
</tbody>
</table>

### Field

<table>
<thead>
<th align="left">Value</th>
<th align="left">Description</th>
</thead>
<tbody>
<tr>
<td valign="top"><strong>dwellingHouseId</strong></td>
<td>

Trier les résultats par l'ID de maison d'un logement

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingYearBuilt</strong></td>
<td>

Trier les résultats par année de construction

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingCity</strong></td>
<td>

Trier les résultats par ville

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingRegion</strong></td>
<td>

Trier les résultats par région

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingForwardSortationArea</strong></td>
<td>

Trier les résultats par région de tri d'acheminement

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationEvaluationType</strong></td>
<td>

Trier les résultats par les logements contenant au moins une évaluation avec un code de type d'évaluation spécifique

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationFileId</strong></td>
<td>

Trier les résultats par les logements contenant au moins une évaluation avec un ID d'évaluation spécifique

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationHouseType</strong></td>
<td>

Trier les résultats par type de logement

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationErsRating</strong></td>
<td>

Trier les résultats des logements contenant au moins une évaluation avec un classement ERS spécifique

</td>
</tr>
</tbody>
</table>

## Scalars

### Boolean

Le type scalaire 'Booléen' représente vrai ('true') ou faux ('false').

### Date

Une date, telle que 2007-12-03, conforme au format' full-date 'décrit dans la section 5.6 du profil RFC 3339 de la norme ISO 8601 pour la nomenclature des dates et des heures du calendrier grégorien.

### Float

Le type scalaire 'Float' représente les valeurs fractionnelles signées à double précision spécifiées par [IEEE 754](https://fr.wikipedia.org/wiki/IEEE_754).

### Int

Le type scalaire 'Int' représente des valeurs numériques entières signées non fractionnaires. Int peut représenter des valeurs comprises entre -(2^31) et 2^31 - 1.

### String

Le type scalaire 'String' représente des données textuelles, représentées par des séquences de caractères UTF-8. Le type String est le plus souvent utilisé par GraphQL pour représenter un texte lisible par un humain.

