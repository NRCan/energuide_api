# Schema Types

<details>
  <summary><strong>Table of Contents</strong></summary>

  * [Query](#query)
  * [Objects](#objects)
    * [Ceiling](#ceiling)
    * [Door](#door)
    * [Dwelling](#dwelling)
    * [Evaluation](#evaluation)
    * [Floor](#floor)
    * [Foundation](#foundation)
    * [FoundationFloor](#foundationfloor)
    * [FoundationWall](#foundationwall)
    * [Header](#header)
    * [HeatedFloorArea](#heatedfloorarea)
    * [Heating](#heating)
    * [PaginatedResultSet](#paginatedresultset)
    * [Upgrade](#upgrade)
    * [Ventilation](#ventilation)
    * [Wall](#wall)
    * [WaterHeater](#waterheater)
    * [Window](#window)
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

### Ceiling

Ceilings are the upper interior surface of a room

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
<td colspan="2" valign="top"><strong>label</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Used to identify the ceiling in the house

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>typeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Describes the construction of the ceiling (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>typeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Describes the construction of the ceiling (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling insulation nominal R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling insulation effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling insulation effective R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling area in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling area in square feet (ft2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>lengthMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling length in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>lengthFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Ceiling length in feet (ft)

</td>
</tr>
</tbody>
</table>

### Door

Doors are on outside walls, separating the interior heated space from the outside

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
<td colspan="2" valign="top"><strong>typeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Describes the construction of the door (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>typeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Describes the construction of the door (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Door RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Door R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>uFactor</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Door U-factor in metric: watts per square metre per degree Celcius (W/m2C)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>uFactorImperial</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Door U-factor in imperial: British Thermal Units per square feet per degree Fahrenheit (BTU/ft2F)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Door area in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Door area in square feet (ft2)

</td>
</tr>
</tbody>
</table>

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
<td colspan="2" valign="top"><strong>ceilings</strong></td>
<td valign="top">[<a href="#ceiling">Ceiling</a>]</td>
<td>

A list of ceiling data entries for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>walls</strong></td>
<td valign="top">[<a href="#wall">Wall</a>]</td>
<td>

A list of wall data entries for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>floors</strong></td>
<td valign="top">[<a href="#floor">Floor</a>]</td>
<td>

A list of floor data entries for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>doors</strong></td>
<td valign="top">[<a href="#door">Door</a>]</td>
<td>

A list of door data entries for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>windows</strong></td>
<td valign="top">[<a href="#window">Window</a>]</td>
<td>

A list of window data entries for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heatedFloorArea</strong></td>
<td valign="top"><a href="#heatedfloorarea">HeatedFloorArea</a></td>
<td>

A heated floor area entry for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>ventilations</strong></td>
<td valign="top">[<a href="#ventilation">Ventilation</a>]</td>
<td>

A list of ventilation data entries for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>waterHeatings</strong></td>
<td valign="top">[<a href="#waterheater">WaterHeater</a>]</td>
<td>

A list of water heater data entries for a dwelling

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heating</strong></td>
<td valign="top"><a href="#heating">Heating</a></td>
<td>

A principal heating system for a dwelling

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
<td colspan="2" valign="top"><strong>foundations</strong></td>
<td valign="top">[<a href="#foundation">Foundation</a>]</td>
<td>

The details of the foundation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>ersRating</strong></td>
<td valign="top"><a href="#int">Int</a></td>
<td>

The EnerGuide Rating calculated for this evaluation

</td>
</tr>
</tbody>
</table>

### Floor

Floors represents the usable area of the house

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
<td colspan="2" valign="top"><strong>label</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Description of floor location

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor insulation nominal R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor insulation effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor insulation effective R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor area of the house in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor area of the house in square feet (ft2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>lengthMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor length of the house in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>lengthFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Floor area of the house in square feet (ft2)

</td>
</tr>
</tbody>
</table>

### Foundation

The lowest load-bearing part of a dwelling

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
<td colspan="2" valign="top"><strong>foundationTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The type of foundation (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>foundationTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The type of foundation (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>label</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

A descriptive label for the foundation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>configurationType</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The type of configuration for the foundation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>materialEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The material used in the construction of this foundation (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>materialFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The material used in the construction of this foundation (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>floors</strong></td>
<td valign="top">[<a href="#foundationfloor">FoundationFloor</a>]</td>
<td>

The details of the floors associated with this foundation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>walls</strong></td>
<td valign="top">[<a href="#foundationwall">FoundationWall</a>]</td>
<td>

The details of the walls associated with this foundation

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>header</strong></td>
<td valign="top"><a href="#header">Header</a></td>
<td>

The details of the foundationn header

</td>
</tr>
</tbody>
</table>

### FoundationFloor

A floor below ground that represents the usable area of the house

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
<td colspan="2" valign="top"><strong>floorTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of foundation floor (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>floorTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of foundation floor (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The insulation nominal RSI (R-value Systeme International) of the foundation floor

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The insulation nominal R-value of the foundation floor

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The insulation effective RSI (R-value Systeme International) of the foundation floor

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The insulation effective R-value of the foundation floor

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The area of the foundation floor in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The area of the foundation floor in square feet (ft2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>perimeterMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The perimeter of the foundation floor in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>perimeterFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The perimeter of the foundation floor in feet (ft)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The width of the foundation floor in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The width of the foundation floor in feet (ft)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>lengthMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The length of the foundation floor in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>lengthFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The length of the foundation floor in feet (ft)

</td>
</tr>
</tbody>
</table>

### FoundationWall

Foundation Walls are below-ground walls separating the interior heated space from the outside (interior partition walls are not considered walls)

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
<td colspan="2" valign="top"><strong>wallTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Wall construction being used (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>wallTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Wall construction being used (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation nominal R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation nominal R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall area of the house in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall area of the house in square feet (ft2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>percentage</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

The percentage of the total wall area this section accounts for

</td>
</tr>
</tbody>
</table>

### Header

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
<td colspan="2" valign="top"><strong>insulationNominalRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header insulation nominal R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header insulation effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header insulation effective R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header area in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header area in square feet (ft2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>perimeterMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header perimeter of the house in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>perimeterFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header perimeter of the house in feet (ft)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header height in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Header height in feet (ft)

</td>
</tr>
</tbody>
</table>

### HeatedFloorArea

Heated floor areas represents the usable areas of a house that is conditioned to a specified temperature during the whole heating season

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
<td colspan="2" valign="top"><strong>areaAboveGradeMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Above-grade heated area of the house in square metres (m2), i.e. the ground floor

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaAboveGradeFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Above-grade heated area of the house in square feet (ft2), i.e. the ground floor

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaBelowGradeMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Below-grade heated area of the house in square metres (m2), i.e. the basement

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaBelowGradeFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Below-grade heated area of the house in square feet (ft2), i.e. the basement

</td>
</tr>
</tbody>
</table>

### Heating

A principal heating system is either the only source of heat for the house, or is used for at least 70% of the heating load

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
<td colspan="2" valign="top"><strong>label</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Description of heating system

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heatingTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of heating system (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heatingTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of heating system (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>energySourceEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The source of fuel for the heating system (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>energySourceFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

The source of fuel for the heating system (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>equipmentTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Equipment type of heating system (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>equipmentTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Equipment type of heating system (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>outputSizeKW</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Output capacity of the heating system in kilowatt hours (kWh)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>outputSizeBtu</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Output capacity of the heating system in British Thermal Units per hour (BTU/h)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>efficiency</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Measures how effectively your heating system is burning fuel or turning fuel into heat

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>steadyState</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Steady-state efficiency is the combustion efficiency of the equipment at peak performance. The Annual Fuel Utilization Efficiency (AFUE) is a measure of efficiency based on average usage, accounting for the fact that most heating systems rarely run long enough to reach peak performance.

</td>
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

### Ventilation

Ventilation systems draw exterior air into the house, exhaust interior air to the exterior, or both

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
<td colspan="2" valign="top"><strong>typeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Ventilation type installed (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>typeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Ventilation type installed (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>airFlowRateLps</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Air flow rate in litres per second (L/s)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>airFlowRateCfm</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Air flow rate in cubic feet per minute (f3/m)

</td>
</tr>
</tbody>
</table>

### Wall

Walls separate the interior heated space from the outside (interior partition walls are not considered walls)

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
<td colspan="2" valign="top"><strong>label</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Description of wall location

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>structureTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Wall construction being used (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>structureTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Wall construction being used (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>componentTypeSizeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Size of the component type (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>componentTypeSizeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Size of the component type (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationNominalR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation nominal R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationEffectiveR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall insulation nominal R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall area of the house in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall area of the house in square feet (ft2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>perimeterMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall perimeter of the house in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>perimeterFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall perimeter of the house in feet (ft)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall height of the house in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Wall height of the house in feet (ft)

</td>
</tr>
</tbody>
</table>

### WaterHeater

Water heaters heat the domestic water in a house

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
<td colspan="2" valign="top"><strong>typeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of tank being used to heat the domestic water in the house (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>typeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of tank being used to heat the domestic water in the house (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>tankVolumeLitres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Capacity of the tank in litres (L)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>tankVolumeGallon</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Capacity of the tank in gallons (Gal)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>efficiencyEf</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Measures how effectively your water heater is burning fuel or turning fuel into heat

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>efficiencyPercentage</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

A percentage representing the ratio of how effectively your water heater is turning fuel into heat

</td>
</tr>
</tbody>
</table>

### Window

Windows separate the interior heated space from the outside

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
<td colspan="2" valign="top"><strong>label</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Used to identify the window component in the house

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationRsi</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>insulationR</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window R-value

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>glazingTypesEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Number of panes of transparent material in a window (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>glazingTypesFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Number of panes of transparent material in a window (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>coatingsTintsEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of coating and tint on a window pane (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>coatingsTintsFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of coating and tint on a window pane (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>fillTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of gas injected between the glass layers (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>fillTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Type of gas injected between the glass layers (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>spacerTypeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Spacer systems used between the glass layers (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>spacerTypeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Spacer systems used between the glass layers (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>typeEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Describes the construction of the window (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>typeFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Describes the construction of the window (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>frameMaterialEnglish</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Material type of the window frame (en)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>frameMaterialFrench</strong></td>
<td valign="top"><a href="#string">String</a></td>
<td>

Material type of the window frame (fr)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window area in square metres (m2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>areaFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window area in square feet (ft2)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>widthMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window width in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>widthFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window width in feet (ft)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightMetres</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window height in metres (m)

</td>
</tr>
<tr>
<td colspan="2" valign="top"><strong>heightFeet</strong></td>
<td valign="top"><a href="#float">Float</a></td>
<td>

Window height in feet (ft)

</td>
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
<tr>
<td valign="top"><strong>ventilationTypeEnglish</strong></td>
<td>

Filter results by the dwellings containing at least one ventilation system with a specific type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>ventilationTypeFrench</strong></td>
<td>

Filter results by the dwellings containing at least one ventilation system with a specific type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>ventilationAirFlowRateLps</strong></td>
<td>

Filter results by the dwellings containing at least one ventilation system with a specific air flow rate in litres per second (L/s)

</td>
</tr>
<tr>
<td valign="top"><strong>ventilationAirFlowRateCfm</strong></td>
<td>

Filter results by the dwellings containing at least one ventilation system with a specific air flow rate in cubic feet per minute (f3/m)

</td>
</tr>
<tr>
<td valign="top"><strong>ventilationEfficiency</strong></td>
<td>

Filter results by the dwellings containing at least one ventilation system with a specific efficiency rating

</td>
</tr>
<tr>
<td valign="top"><strong>floorLabel</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific location

</td>
</tr>
<tr>
<td valign="top"><strong>floorInsulationNominalRsi</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>floorInsulationNominalR</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific nominal R-value

</td>
</tr>
<tr>
<td valign="top"><strong>floorInsulationEffectiveRsi</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific effective R-value

</td>
</tr>
<tr>
<td valign="top"><strong>floorInsulationEffectiveR</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific effective R-value

</td>
</tr>
<tr>
<td valign="top"><strong>floorAreaMetres</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>floorAreaFeet</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>floorLengthMetres</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific length in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>floorLengthFeet</strong></td>
<td>

Filter results by the dwellings containing at least one floor with a specific length in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>waterHeatingTypeEnglish</strong></td>
<td>

Filter results by the dwellings containing at least one water heating system of a specific type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>waterHeatingTypeFrench</strong></td>
<td>

Filter results by the dwellings containing at least one water heating system of a specific type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>waterHeatingTankVolumeLitres</strong></td>
<td>

Filter results by the dwellings containing at least one water heating system with a specific capacity in litres (L)

</td>
</tr>
<tr>
<td valign="top"><strong>waterHeatingTankVolumeGallon</strong></td>
<td>

Filter results by the dwellings containing at least one water heating system with a specific capacity in gallons (Gal)

</td>
</tr>
<tr>
<td valign="top"><strong>waterHeatingEfficiencyPercentage</strong></td>
<td>

Filter results by the dwellings containing at least one water heating system with a specific efficiency percentage

</td>
</tr>
<tr>
<td valign="top"><strong>waterHeatingEfficiencyEf</strong></td>
<td>

Filter results by the dwellings containing at least one water heating system with a specific efficiency rating

</td>
</tr>
<tr>
<td valign="top"><strong>heatingLabel</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific description

</td>
</tr>
<tr>
<td valign="top"><strong>heatingHeatingTypeEnglish</strong></td>
<td>

Filter results by the dwellings containing a heating system of a specific type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingHeatingTypeFrench</strong></td>
<td>

Filter results by the dwellings containing a heating system of a specific type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingEnergySourceEnglish</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific fuel source (en)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingEnergySourceFrench</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific fuel source (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingEquipmentTypeEnglish</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific type of equipment (en)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingEquipmentTypeFrench</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific type of equipment (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingOutputSizeKW</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific output capacity in kilowatt hours (kWh)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingOutputSizeBtu</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific output capacity in British Thermal Units per hour (BTU/h)

</td>
</tr>
<tr>
<td valign="top"><strong>heatingEfficiency</strong></td>
<td>

Filter results by the dwellings containing a heating system with a specific efficiency rating

</td>
</tr>
<tr>
<td valign="top"><strong>heatingSteadyState</strong></td>
<td>

Filter results by the dwellings containing a heating system efficiency measurement that is either 'Steady State' or 'AFUE'

</td>
</tr>
<tr>
<td valign="top"><strong>heatedFloorAreaAreaAboveGradeMetres</strong></td>
<td>

Filter results by the dwellings containing an above-grade heated floor area with a specific area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>heatedFloorAreaAreaAboveGradeFeet</strong></td>
<td>

Filter results by the dwellings containing an above-grade heated floor area with a specific area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>heatedFloorAreaAreaBelowGradeMetres</strong></td>
<td>

Filter results by the dwellings containing a below-grade heated floor area with a specific area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>heatedFloorAreaAreaBelowGradeFeet</strong></td>
<td>

Filter results by the dwellings containing a below-grade heated floor area with a specific area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>wallLabel</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific location

</td>
</tr>
<tr>
<td valign="top"><strong>wallStructureTypeEnglish</strong></td>
<td>

Filter results by the dwellings containing at least one wall of a specific type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>wallStructureTypeFrench</strong></td>
<td>

Filter results by the dwellings containing at least one wall of a specific type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>wallComponentTypeSizeEnglish</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a component of a specific size (en)

</td>
</tr>
<tr>
<td valign="top"><strong>wallComponentTypeSizeFrench</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a component of a specific size (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>wallInsulationNominalRsi</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>wallInsulationNominalR</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific nominal R-value

</td>
</tr>
<tr>
<td valign="top"><strong>wallInsulationEffectiveRsi</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>wallInsulationEffectiveR</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific effective R-value

</td>
</tr>
<tr>
<td valign="top"><strong>wallAreaMetres</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>wallAreaFeet</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>wallPerimeterMetres</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific perimeter in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>wallPerimeterFeet</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific perimeter in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>wallHeightMetres</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific height in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>wallHeightFeet</strong></td>
<td>

Filter results by the dwellings containing at least one wall with a specific height in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingLabel</strong></td>
<td>

Filter results by the dwellings where at least one ceiling has a matching label

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingTypeEnglish</strong></td>
<td>

Filter results by the dwellings where at least one ceiling has a matching type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingTypeFrench</strong></td>
<td>

Filter results by the dwellings where at least one ceiling has a matching type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingInsulationNominalRsi</strong></td>
<td>

Filter results by the dwellings where at least one ceiling has a specific nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingInsulationNominalR</strong></td>
<td>

Filter results by the dwellings containing at least one ceiling with a specific nominal R-value

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingInsulationEffectiveRsi</strong></td>
<td>

Filter results by the dwellings containing at least one ceiling with a specific effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingInsulationEffectiveR</strong></td>
<td>

Filter results by the dwellings containing at least one ceiling with a specific effective R-value

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingAreaMetres</strong></td>
<td>

Filter results by the dwellings containing at least one ceiling with a specific area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingAreaFeet</strong></td>
<td>

Filter results by the dwellings containing at least one ceiling with a specific area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingLengthMetres</strong></td>
<td>

Filter results by the dwellings containing at least one ceiling with a specific length in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>ceilingLengthFeet</strong></td>
<td>

Filter results by the dwellings containing at least one ceiling with a specific length in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>doorTypeEnglish</strong></td>
<td>

Filter results by the dwellings containing at least one door with a specific type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>doorTypeFrench</strong></td>
<td>

Filter results by the dwellings containing at least one door with a specific type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>doorInsulationRsi</strong></td>
<td>

Filter results by the dwellings where at least one door has a specific RSI (R-value Systeme International) value

</td>
</tr>
<tr>
<td valign="top"><strong>doorInsulationR</strong></td>
<td>

Filter results by the dwellings containing at least one door with a specific effective R-value

</td>
</tr>
<tr>
<td valign="top"><strong>doorUFactor</strong></td>
<td>

Filter results for dwellings which have at least one door with a matching U-factor in metric: watts per square metre per degree Celcius (W/m2C)

</td>
</tr>
<tr>
<td valign="top"><strong>doorUFactorImperial</strong></td>
<td>

Filter results for dwellings which have at least one door with a matching U-factor in imperial: British Thermal Units per square feet per degree Fahrenheit (BTU/ft2F)

</td>
</tr>
<tr>
<td valign="top"><strong>doorAreaMetres</strong></td>
<td>

Filter results by dwellings where the area of the doors have certain value in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>doorAreaFeet</strong></td>
<td>

Filter results by dwellings where the area of the doors have certain value in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>windowLabel</strong></td>
<td>

Filter results by dwellings that have a window with a specific label

</td>
</tr>
<tr>
<td valign="top"><strong>windowInsulationRsi</strong></td>
<td>

Filter results by dwellings with a specific window RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>windowInsulationR</strong></td>
<td>

Filter results by dwellings with a specific window R-value

</td>
</tr>
<tr>
<td valign="top"><strong>windowGlazingTypesEnglish</strong></td>
<td>

Filter results by dwellings with a matching number of panes of transparent material in a window (en)

</td>
</tr>
<tr>
<td valign="top"><strong>windowGlazingTypesFrench</strong></td>
<td>

Filter results by dwellings with a matching number of panes of transparent material in a window (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>windowCoatingsTintsEnglish</strong></td>
<td>

Filter results for dwellings with a specific type of coating and tint on a window pane (en)

</td>
</tr>
<tr>
<td valign="top"><strong>windowCoatingsTintsFrench</strong></td>
<td>

Filter results for dwellings with a specific type of coating and tint on a window pane (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>windowFillTypeEnglish</strong></td>
<td>

Filter results for dwellings with windows containing a specific type of gas injected between the glass layers (en)

</td>
</tr>
<tr>
<td valign="top"><strong>windowFillTypeFrench</strong></td>
<td>

Filter results for dwellings with windows containing a specific type of gas injected between the glass layers (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>windowSpacerTypeEnglish</strong></td>
<td>

Filter results for dwellings with a specific spacer system used between the glass layers (en)

</td>
</tr>
<tr>
<td valign="top"><strong>windowSpacerTypeFrench</strong></td>
<td>

Filter results for dwellings with a specific spacer system used between the glass layers (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>windowTypeEnglish</strong></td>
<td>

Filter results for dwellings with a particular type of window construction (en)

</td>
</tr>
<tr>
<td valign="top"><strong>windowTypeFrench</strong></td>
<td>

Filter results for dwellings with a particular type of window construction (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>windowFrameMaterialEnglish</strong></td>
<td>

Filter results for dwellings with window frames matching a specific material (en)

</td>
</tr>
<tr>
<td valign="top"><strong>windowFrameMaterialFrench</strong></td>
<td>

Filter results for dwellings with window frames matching a specific material (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>windowAreaMetres</strong></td>
<td>

Filter results for dwellings with a window matching a specific area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>windowAreaFeet</strong></td>
<td>

Filter results for dwellings with a window matching a specific area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>windowWidthMetres</strong></td>
<td>

Filter results for dwellings with a window matching a specific width in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>windowWidthFeet</strong></td>
<td>

Filter results for dwellings with a window matching a specific width in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>windowHeightMetres</strong></td>
<td>

Filter results for dwellings with a window matching a specific height in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>windowHeightFeet</strong></td>
<td>

Filter results for dwellings with a window matching a specific height in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFoundationTypeEnglish</strong></td>
<td>

Filter results for dwellings with matching foundation type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFoundationTypeFrench</strong></td>
<td>

Filter results for dwellings with matching foundation type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationLabel</strong></td>
<td>

Filter results for dwellings with a specific foundation label

</td>
</tr>
<tr>
<td valign="top"><strong>foundationConfigurationType</strong></td>
<td>

Filter results for dwellings with a specific foundation configuration

</td>
</tr>
<tr>
<td valign="top"><strong>foundationMaterialEnglish</strong></td>
<td>

Filter results for dwellings whose foundation was constructed with a specific material (en)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationMaterialFrench</strong></td>
<td>

Filter results for dwellings whose foundation was constructed with a specific material (en)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderInsulationNominalRsi</strong></td>
<td>

Filter results for dwellings with a specific foundation header insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderInsulationNominalR</strong></td>
<td>

Filter results for dwellings with a specific foundation header insulation nominal R-value

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderInsulationEffectiveRsi</strong></td>
<td>

Filter results for dwellings with a specific foundation header insulation effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderInsulationEffectiveR</strong></td>
<td>

Filter results for dwellings with a specific foundationn header insulation effective R-value

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderAreaMetres</strong></td>
<td>

Filter results for dwellings with a specific foundation header area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderAreaFeet</strong></td>
<td>

Filter results for dwellings with a specific foundation header area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderPerimeterMetres</strong></td>
<td>

Filter results for dwellings with a specific foundation header perimeter in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderPerimeterFeet</strong></td>
<td>

Filter results for dwellings with a specific foundation header perimeter in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderHeightMetres</strong></td>
<td>

Filter results for dwellings with a specific foundation header height in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationHeaderHeightFeet</strong></td>
<td>

Filter results for dwellings with a specific header height in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorFloorTypeEnglish</strong></td>
<td>

Filter for dwellings with a specific type of foundation floor type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorFloorTypeFrench</strong></td>
<td>

Filter for dwellings with a specific type of foundation floor type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorInsulationNominalRsi</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorInsulationNominalR</strong></td>
<td>

Filter for dwellings with a specific insulation nominal R-value on the foundation floor

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorInsulationEffectiveRsi</strong></td>
<td>

Filter for dwellings with a specific insulation effective RSI (R-value Systeme International) for the foundation floor

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorInsulationEffectiveR</strong></td>
<td>

Filter for dwellings with a specific insulation effective R-value for the foundation floor

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorAreaMetres</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorAreaFeet</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific area in square feet (ft2)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorPerimeterMetres</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific perimeter in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorPerimeterFeet</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific perimeter in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorWidthMetres</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific width in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorWidthFeet</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific width in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorLengthMetres</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific length in metres (m)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationFloorLengthFeet</strong></td>
<td>

Filter for dwellings where the foundation floor has a specific length in feet (ft)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallWallTypeEnglish</strong></td>
<td>

Filter results for dwellings whose foundation wall has a specific type (en)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallWallTypeFrench</strong></td>
<td>

Filter results for dwellings whose foundation wall has a specific type (fr)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallInsulationNominalRsi</strong></td>
<td>

Filter results for dwellings with a specific foundation wall insulation nominal RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallInsulationNominalR</strong></td>
<td>

Filter results for dwellings with a specific foundation wall insulation nominal R-value

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallInsulationEffectiveRsi</strong></td>
<td>

Filter results for dwellings with a specific foundation wall insulation effective RSI (R-value Systeme International)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallInsulationEffectiveR</strong></td>
<td>

Filter results for dwellings with a specific foundation wall insulation effective R-value

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallPercentage</strong></td>
<td>

Filter results for dwellings with a section of its foundation wall with a specific percentage of the overall amount

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallAreaMetres</strong></td>
<td>

Filter results for dwellings with a specific foundation wall area in square metres (m2)

</td>
</tr>
<tr>
<td valign="top"><strong>foundationWallAreaFeet</strong></td>
<td>

Filter results for dwellings with a specific foundation wall area in square feet (ft2)

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

