[La version française suit.](#---------------------------------------------------------------------)

# Ingress to ETL - AKA generating input CSVs

See the following diagram for an architechural overview of the system

<img src="architectural_diagram.png" width="500" >

To generate the input to the system this describes, a script will have to be written to generate the CSV dumps of the database

The system is built to support incremental loads, and has convience built-in for generating the incremental dumps from the database.
The `Extract endpoint` portion of the system provides three endpoints, one of which is for fetching the timestamp showing how fresh the
data is. This will return the most recent `MODIFICATIONDATE` provided to the system, which is updated along with each post to the endpoint.

The ingress to the system should query this endpoint, and dump all rows with modification date after what is returned by
the `/timestamp` endpoint, and pass along the latest `MODIFICATIONDATE` in the returned dataset.

Something along the lines of the following

```
url="https://nrcan-endpoint.azurewebsites.net"
modification_date=$(curl "$url/timestamp") 
new_date = $(dump_from_datebase.sh $modification_date)
energuide extract --infile generated.csv --outfile extract.zip
extract_endpoint extract.zip $new_date --url $url
```

Where `dump_from_database.sh` is some script that dumps all rows who's `MODIFICATIONDATE` field is after the date passed in, and outputs the max `MODIFICATIONDATE` in the returned data.

## ---------------------------------------------------------------------

# Entrée à l’ETC – aussi appelé produisant des données d'entrée des fichiers CSV

Voir le diagramme suivant pour un survol architectural du système

<img src="architectural_diagram.png" width="500" >

Pour produire des données d’entrée au système, un script devra être écrit pour produire des dépôts de base de données du fichier CSV. 

Le système est conçu pour appuyer l’augmentation des charges, et est facile d’accès pour produire des dépôts supplémentaires de la base de données. La partie Extract endpoint du système donne trois points d’extrémité, dont un est pour chercher l’horodateur montrant à quel point les données sont récentes. Cela va retourner la plus récente date de modification (MODIFICATIONDATE) fournie dans le système, qui est mis à jour avec chaque article au point d’extrémité.
L’entrée au système devrait interroger ce point d’extrémité, et laisser tomber toutes les rangées avec une date de modification après ce qui est retourné par le /timestamp du point d’extrémité, et transmettre la dernière date de modification (MODIFICATIONDATE) dans le jeu de données retourné.
Vous aurez quelque chose qui ressemble à ceci :
```
url="https://nrcan-endpoint.azurewebsites.net"
modification_date=$(curl "$url/timestamp") 
new_date = $(dump_from_datebase.sh $modification_date)
energuide extract --infile generated.csv --outfile extract.zip
extract_endpoint extract.zip $new_date --url $url
```
Le lieu où dump_from_database.sh se trouve, certains scripts qui déchargent toutes les rangées champ de la date de modification (MODIFICATIONDATE) qui est après la date passée, et extrait le maximum de MODIFICATIONDATE dans les données retournées.

