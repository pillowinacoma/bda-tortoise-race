# BDA-tortoises-races

### Comment utiliser le programme

- après la connection à la VM ci dessus, pous pouvez lancer les differentes programmes :
  - Récuperation des données :

    ```bash
        python3 recuperation.py $course $target_dir $single_file_size
    ```
    cette commande lancera la recuperation des données de la course $course (tiny, small, medium et large) depuis le server, ces données seront stoqués dans un repertoir $target_dir dans des fichiers de la taille $single_file_size, les fichiers sont nommés selon le premier et le dernier top contenus dedans, les données seront stockés sous la structure suivante : 
    ```bash
    $target_dir
    |   tiny
    |   |   0
    |   |   |   785398-786398.csv
    |   |   |   786398-787398.csv
    |   |   |   ...
    |   |   1
    |   |   ...
    |   small
    |   ...
    ...
    
    ```
- Analise de données: 
    ```bash
    chmod 700 analyse.sh && ./analyse.sh
    ```
    cette commande lancera le script d'analyse des données, par defaut, ce script recupère les données du repertoir `data3` (hdfs), et génére un modèle dans le repertoir `results`, ce modèle sera parcouru par le script de prédiction
- Prédiction:
    ```bash
    chmod 700 prediction.sh && ./prediction.sh $course, $id, $top, $pos1, $pos2, $pos3, $temp, $quali, $deltatop
    ```
    en sortie vous aurez la position de la tortue à la position `$pos1 + $deltatop`





## Récupération des données

Pour la récuperation de données nous utilisons un programme Python avec la librairie **requests** pour requêter le serveur.

### Script de récupération

La script Python [recuperation.py](./recuperation.py) va requêter le serveur toutes les 2 secondes pour éviter de manquer des _tops_ et va ignorer les doublons. Si la nouvelle donnée sur la course possède le même _top_ que la dernière enregistrée, alors elle est ignoré.

La fonction **getData** de notre script de récupération de données prend 3 paramètres :

- La taille de la course sur laquelle on veut récuperer les données. `{tiny, small, medium, large}`
- Le répertoire dans lequelle on veut enregistrer les données. `Par défaut : "./data"`
- Le nombre de ligne que l'on veut enregistrer par fichier. `Par défaut : 1000`

> Remarque : Les fichiers csv ne sont écrit que lorsque le bon nombre donnée à été récupéré. _Exemple : Si le nombre de ligne par fichier est configuré sur 1000, les fichiers csv seront créés une fois qu'on aura récupéré 1000 tops._

Au lancement du programme, nous allons créer dans le répertoire _./data/{taille_course}/_, un répertoire pour chaque tortue. Chaque dossier portera comme nom l'identifiant de la tortue qu'il représente. Dans chaque dossier associé à une tortue nous allons créer et remplir des fichiers csv au cours de l'éxecution du programme. Chaque csv contiendra par défaut 1000 top d'une tortue.

Les fichiers seront composé dans attributs suivant : `top | id | position | vitesse | qualite | temperature `, où la vitesse est la différence entre la position de la tortue au top précedent et le top actuel.

Un exemple pour la tortue 0 de la course tiny:

```csv
top,id,position,vitesse,qualite,temperature
794399,0,66729516,84,0.3100529516794682,4.431087398824114
794400,0,66729600,84,0.3100529516794682,4.431087398824114
794401,0,66729684,84,0.3100529516794682,4.431087398824114
794402,0,66729768,84,0.3100529516794682,4.431087398824114
794403,0,66729852,84,0.3100529516794682,4.431087398824114
794404,0,66729936,84,0.3100529516794682,4.431087398824114
...
```

On peut supposer que cette tortue est régulière car sa vitesse ne change pas.

Un exemple pour la tortue 17 de la course small:

```csv
top,id,position,vitesse,qualite,temperature
...
804871,17,129987328,63,0.48688447869248985,-4.201155048069171
804872,17,129987378,50,0.48688447869248985,-4.201155048069171
804873,17,129987415,37,0.48688447869248985,-4.201155048069171
804874,17,129987439,24,0.48688447869248985,-4.201155048069171
804875,17,129987450,11,0.48688447869248985,-4.201155048069171
804876,17,129987450,0,0.48688447869248985,-4.201155048069171
804877,17,129987463,13,0.48688447869248985,-4.201155048069171
804878,17,129987489,26,0.48688447869248985,-4.201155048069171
804879,17,129987528,39,0.48688447869248985,-4.201155048069171
804880,17,129987580,52,0.48688447869248985,-4.201155048069171
804881,17,129987645,65,0.48688447869248985,-4.201155048069171
...
```

On peut supposer que celle-ci est fatigué car sa vitesse diminue jusqu'à atteindre 0 puis re-accélère.

### Copie sur HDFS

Pour affectuer nos traitements d'analyses nous allons avoir besoins d'un systeme de traitement distribuée pour gérer et analyser nos grandes quantité de données.
Nous allons utiliser HDFS pour sauvegarder nos données de façon distribué. Par la suite nous pourrons appliquer un traitement distribué pour rendre notre analyse bien plus efficace et rapide.

![Schema traitement distribué HDFS](Hadoop_schema.jpeg)

Pour cela nous allons copier nos données sur un cluster HDFS toutes les 12h. Nous utilisons **cron** pour executer la commande _hdfs_ automatiquement tout les _x_ temps :

- commande cron hdsf:

```bash
# crontab -l
00 */8 * * * hdfs dfs -put /home/p1807434/TP/data4/* data3/ >> /home/p1807434/TP/hdfs_put_cron.log
```

## Analyse des données

Le script [analyse.py](analyse.py) parcours les données récupérées pour chaque tortue, on agrège par température et qualité, puis on trasforme les données à ce format

```json

    "cyclique": [
        {
            "params": [
                "cyclique",
                [
                    252,
                    81,
                    163
                ],
                18
            ],
            "env": [
                {
                    "temp": 17.004066201175558,
                    "quali": 0.9999277673652672
                },
                {
                    "temp": 11.56090978502972,
                    "quali": 0.9999277673652672
                },
                {
                    "temp": 15.075484303915852,
                    "quali": 0.9999277673652672
                }
            ]
        }
    ]
```

Une tortue lunatique aura de ce fait, plusieurs comportements à la suite.
Pour lancer l'analyse pour toutes les courses, il suffit de lancer le script Shell analyse.sh, qui lancera l'analyse pour tout les courses, en generant le modèle ci dessus.

## Prédiction

Pour les tortues avec un seul comportement, on déduit directement à partir des données du fichier modèle la position dans _deltatop_ top. Pour une tortue avec plusieurs comportements (lunatiques), on calcule la distance minimale entre la temperature et la qualité de celle ci, et les temperatures et qualités obsérvées pendant les comportements enregistré dans le fichier modèle. Le comportement lié à cette distance minimale sera celui utilisé pour la prédiction.




