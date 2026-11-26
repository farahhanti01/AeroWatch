from pyspark.sql import SparkSession
from pyspark.sql import functions as F

source_path = "/app/data/samples/opensky_aviation_dataset.csv"
bronze_path = "/app/data/delta/bronze/opensky_history"

spark = SparkSession.builder.appName("AeroWatch - Ingestion Bronze").getOrCreate()

try:
    # Lire le CSV en utilisant la première ligne comme noms de colonnes.
    observations = spark.read.option("header", True).csv(source_path)

    # Ajouter la provenance et l'heure du chargement.
    bronze = (
        observations
        .withColumn("source_file", F.lit("opensky_aviation_dataset.csv"))
        .withColumn("ingested_at", F.current_timestamp())
    )

    # Écrire la table Delta, puis la relire pour vérifier le chargement.
    bronze.write.format("delta").mode("overwrite").save(bronze_path)

    result = spark.read.format("delta").load(bronze_path)
    print(f"Observations enregistrées dans Bronze : {result.count()}")
    result.show(5, truncate=False)
finally:
    spark.stop()