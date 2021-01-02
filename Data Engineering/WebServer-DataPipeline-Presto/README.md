# Understanding User Behavior

# Summary

Our mobile game has two events we're interested in tracking: buying a sword and joining a guild. This report is a summary of how the data pipeline was set up so that our data anayltics team can use it to query and solve the business problems at hand.

# Repo Structure

- `docker-compose.yml` - Cluster used for spinning the multi-container pipeline: Kakfa,
- `Project_3.ipynb` - Jupyter Notebook that contains annotations on how the multi-container pipeline was set up for use with example business queries completed in Presto.
- `while-ab.sh` - The shell script that uses Apache Bench to generate business event requests for the web-app server.
- `write_stream.py` - Spark streaming file that pulls events from Kafka, filters for event type, reads and writes to 2 separate event streams, and writes them to storage in HDFS.
- `game_apy.py` - The API web-app Flask server that handles the event requests by processing the sword purchase or guild join events and logging those events to Kafka


