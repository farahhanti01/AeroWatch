# Plan de travail par sprints

**Projet AeroWatch**  
**Équipe** · Farah HANTI, Mohammed ESSOULAIMANI et Ahmed MASBAH  
**Calendrier** · Six sprints sur les trois semaines restantes du projet.

Cochez une tâche lorsque son résultat a été vérifié. Pour faciliter la revue en équipe, ajoutez le lien de la pull request ou de l’issue à côté des tâches concernées.

## Sprint 1 — Cadrage et ingestion batch

**Semaine 2 · Objectif** — Charger un premier fichier historique OpenSky dans Delta Bronze.

- [ ] Valider le périmètre de la démonstration et choisir un fichier historique OpenSky.
- [ ] Configurer Spark et Delta Lake dans `compose.yaml`, puis vérifier leur démarrage local.
- [ ] Placer un échantillon dans `data/samples/` ou documenter comment l’obtenir.
- [ ] Implémenter la lecture du fichier dans `ingestion/batch/load_opensky_history.py`.
- [ ] Écrire les observations brutes dans Bronze avec leur source et leur heure d’ingestion.
- [ ] Documenter la commande de chargement et relever le nombre de lignes lues et écrites.

**Critère de validation** — Une lecture Spark retrouve les observations de l’échantillon dans Bronze avec leur provenance.

## Sprint 2 — Ingestion quasi temps réel

**Semaine 2 · Objectif** — Suivre une observation récente depuis OpenSky jusqu’à Bronze.

- [ ] Tester l’accès à l’API OpenSky et vérifier la disponibilité des observations sur la zone choisie.
- [ ] Configurer Kafka et créer le topic des observations brutes.
- [ ] Implémenter la collecte périodique dans `ingestion/streaming/collect_opensky.py` et publier les réponses dans Kafka.
- [ ] Gérer les erreurs de collecte et stocker la configuration d’accès hors Git.
- [ ] Configurer Spark Structured Streaming pour lire le topic et écrire dans Bronze avec un checkpoint.
- [ ] Conserver un échantillon de réponses autorisé pour préparer le scénario de rejeu.

**Critère de validation** — Une observation de l’API est retrouvée dans le topic Kafka puis dans Bronze.

## Sprint 3 — Qualité des données et alertes dynamiques

**Semaine 3 · Objectif** — Publier des observations fiables dans Silver et démontrer une règle modifiable à chaud.

- [ ] Définir le schéma commun des observations batch et streaming, puis normaliser les dates en UTC.
- [ ] Contrôler les champs obligatoires et les coordonnées avec Great Expectations.
- [ ] Dédupliquer sur l’identifiant de l’appareil et l’horodatage de position, puis écrire les observations valides dans Silver.
- [ ] Envoyer les observations invalides en quarantaine avec leur motif de rejet.
- [ ] Créer une règle d’alerte dans PostgreSQL et configurer Debezium pour publier ses modifications dans Kafka.
- [ ] Faire consommer à Flink les observations et les changements de règles, puis publier les alertes.

**Critère de validation** — Une ligne invalide est retrouvée en quarantaine. Un changement de seuil dans PostgreSQL modifie le résultat produit par Flink sur une observation ultérieure, sans redémarrage.

## Sprint 4 — Réconciliation et premiers KPI

**Semaine 3 · Objectif** — Afficher un premier indicateur reproductible dans le tableau de bord.

- [ ] Vérifier qu’une observation présente dans les deux sources n’est comptée qu’une fois.
- [ ] Construire les agrégats Gold par zone et période à partir des observations réconciliées.
- [ ] Exposer les premiers indicateurs en Spark SQL, dont le nombre d’appareils distincts et la vitesse moyenne.
- [ ] Connecter Power BI à la couche de restitution ou utiliser Superset pour la démonstration locale si nécessaire.
- [ ] Afficher un premier KPI et le vérifier par une requête Spark SQL sur le même périmètre.
- [ ] Rejouer un lot et comparer les indicateurs avant et après le rejeu.

**Critère de validation** — Le KPI affiché concorde avec Spark SQL et garde la même valeur après le rejeu du lot testé.

## Sprint 5 — Machine Learning et exploitation

**Semaine 4 · Objectif** — Publier des scores d’atypicité et superviser les traitements.

- [ ] Construire les segments de trajectoire et calculer les caractéristiques de vitesse, d’altitude et de variation de cap.
- [ ] Entraîner K-means avec Spark MLlib et évaluer le modèle sur une période ultérieure à l’entraînement.
- [ ] Enregistrer les paramètres et les métriques, dont le score de silhouette, dans MLflow.
- [ ] Publier les scores d’atypicité dans Gold et afficher un segment à examiner dans le tableau de bord.
- [ ] Configurer un DAG Airflow pour les traitements batch, la qualité, Gold et l’entraînement.
- [ ] Afficher dans Grafana la fraîcheur des données, le débit, les rejets et les erreurs de collecte.

**Critère de validation** — Une exécution Airflow aboutit. MLflow affiche les métriques d’un entraînement, le tableau de bord présente un segment noté et Grafana affiche les métriques du pipeline.

## Sprint 6 — Recette et soutenance

**Semaine 4 · Objectif** — Valider la démonstration complète et préparer les livrables.

- [ ] Exécuter la chaîne sous Docker Compose et suivre une observation depuis sa source jusqu’au tableau de bord.
- [ ] Tester la démonstration de secours avec des réponses OpenSky enregistrées et identifier le mode rejeu sur le tableau de bord.
- [ ] Vérifier la règle d’alerte dynamique, les rejets, le non-double-comptage et les résultats ML.
- [ ] Finaliser le catalogue, le lignage, les règles d’accès et de rétention, ainsi que la section RGPD.
- [ ] Mettre à jour le README avec les commandes de démarrage et de démonstration testées.
- [ ] Finaliser le rapport, les diapositives et les fiches de contribution individuelle.
- [ ] Répéter la démonstration en trinôme.

**Critère de validation** — L’équipe peut reproduire le parcours complet en direct et en rejeu, puis présenter les résultats et les limites de la plateforme.
