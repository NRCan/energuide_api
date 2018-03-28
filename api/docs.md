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
The root query type

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

Details for a specific dwelling

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

Details for all dwellings, optionally filtered by one or more values

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

A residential building evaluted under the Energuide program

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

Unique identification number for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>yearBuilt</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

Year of construction

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>city</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Name of city where dwelling is located

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>region</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Region of country for dwelling (province/territory)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>forwardSortationArea</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The first three characters of a Canadian postal code, which correspond to a geographical area defined by Canada Post

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>evaluations</strong></td>
<td valign="top">[<a href="#evaluation">Evaluation</a>]</td>
<td>

A list of evaluations of specific features of the dwelling

</td>
</tr>
</tbody>
</table>

### Evaluation

Detailed information about specific features of a given dwelling

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

Evaluation type codes are used to define the type of evaluation performed and to distinguish the house type (i.e. newly built or existing)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>entryDate</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Date the evaluation was made

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>fileId</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>houseType</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>creationDate</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Date the record was first created

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>modificationDate</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Date the record was last modified

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>energyUpgrades</strong></td>
<td valign="top">[<a href="#upgrade">Upgrade</a>]</td>
<td>

A list of upgrades that would improve energy efficiency

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heatedFloorArea</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>ersRating</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td>

The EnerGuide Rating calculated for this evaluation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>eghRating</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>greenhouseGasEmissions</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>energyIntensity</strong></td>
<td valign="top"><a href="#rating">Rating</a></td>
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>walls</strong></td>
<td valign="top"><a href="#wall">Wall</a></td>
<td></td>
</tr>
</tbody>
</table>

### Insulation

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
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>rValue</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td></td>
</tr>
</tbody>
</table>

### PaginatedResultSet

One page of results

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

If true, a further page of results can be returned

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>hasPrevious</strong></td>
<td valign="top"><a href="#boolean">Boolean</a></td>
<td>

If true, a previous page of results can be returned

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>next</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Identifier used to return the next page of results

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>previous</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Identifier cursor used to return the previous page of results

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>results</strong></td>
<td valign="top">[<a href="#dwelling">Dwelling</a>]</td>
<td>

A list of dwellings

</td>
</tr>
</tbody>
</table>

### Rating

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
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>upgrade</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td></td>
</tr>
</tbody>
</table>

### Upgrade

An improvement that could increase the energy efficiency of the dwelling

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

Part of the dwelling to be upgraded

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>cost</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

Estimated cost of upgrade

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>priority</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

Order of importance of upgrade recommendation (lower number means a higher priority)

</td>
</tr>
</tbody>
</table>

### Wall

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
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>upgrade</strong></td>
<td valign="top"><a href="#wallmeasurement">WallMeasurement</a></td>
<td></td>
</tr>
</tbody>
</table>

### WallMeasurement

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
<td></td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heatLost</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td></td>
</tr>
</tbody>
</table>

## Enums

### Comparator

An operator to describe how results will be filtered

<table>
<thead>
<th align="left">Value</th>
<th align="left">Description</th>
</thead>
<tbody>
<tr>
<td valign="top"><strong>gt</strong></td>
<td>

Greater than: returns true for results greater than the comparison value

</td>
</tr>
<tr>
<td valign="top"><strong>lt</strong></td>
<td>

Less than: returns true for results less than the comparison value

</td>
</tr>
<tr>
<td valign="top"><strong>eq</strong></td>
<td>

Equal to: returns true for results equal to the comparison value

</td>
</tr>
</tbody>
</table>

### DateField

An ISO date value, formatted 'YYYY-MM-DD'

<table>
<thead>
<th align="left">Value</th>
<th align="left">Description</th>
</thead>
<tbody>
<tr>
<td valign="top"><strong>evaluationEntryDate</strong></td>
<td>

Filter results by the dwellings containing at least one evaluation with a specific entry date

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationCreationDate</strong></td>
<td>

Filter results by the dwellings containing at least one evaluation with a specific record creation date

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationModificationDate</strong></td>
<td>

Filter results by the dwellings containing at least one evaluation with a specific record modification date

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

Filter results by the house ID of a dwelling

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingYearBuilt</strong></td>
<td>

Filter results by dwellings built in a specific year

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingCity</strong></td>
<td>

Filter results by the dwellings in a specific city

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingRegion</strong></td>
<td>

Filter results by the dwellings in a specific region

</td>
</tr>
<tr>
<td valign="top"><strong>dwellingForwardSortationArea</strong></td>
<td>

Filter results by the dwellings in a specific forward sortation area

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationEvaluationType</strong></td>
<td>

Filter results by the dwellings containing at least one evaluation with a specific evaluation type code

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationFileId</strong></td>
<td>

Filter results by the dwellings containing at least one evaluation with a specific evaluation ID

</td>
</tr>
<tr>
<td valign="top"><strong>evaluationErsRating</strong></td>
<td>

Filter results by the dwellings containing at least one evaluation with a specific ERS rating

</td>
</tr>
</tbody>
</table>

## Scalars

### Boolean

The 'Boolean' scalar type represents 'true' or 'false'.

### Date

A date string, such as 2007-12-03, compliant with the 'full-date' format outlined in section 5.6 of the RFC 3339 profile of the ISO 8601 standard for representation of dates and times using the Gregorian calendar.

### Float

The 'Float' scalar type represents signed double-precision fractional values as specified by [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).

### Int

The 'Int' scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

### String

The 'String' scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.

