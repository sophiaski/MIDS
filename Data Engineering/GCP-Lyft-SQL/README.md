# Project 1: Query Project

  Uses Google Cloud Platform (GCP) and BiqQuery to answer business-driven
  questions using public datasets. This folder features code for web UI (BiqQuery) and
  the command-line tools in Jupyter Notebooks.
  
  This shows work completed in a cloud environment using SQL against a big data data platform.

#### Problem Statement

- You're a data scientist at Lyft Bay Wheels (https://www.lyft.com/bikes/bay-wheels), formerly known as Ford GoBike, the
  company running Bay Area Bikeshare.  are trying to increase ridership, and
  you want to offer deals through the mobile app to do so. 
  
- What deals do you offer though? Currently, your company has several options which can change over time. Frequent offers include: 
  * Single Ride 
  * Monthly Membership
  * Annual Membership
  * Bike Share for All
  * Access Pass
  * Corporate Membership
  * etc.

- This project answers the following questions: 
  * What are the 5 most popular trips that you would call "commuter trips"?  
  * What are your recommendations for offers (justify based on your findings)?


## Parts 1, 2, 3

- In Part 1, queries using the Google BigQuery GUI interface in the cloud.
- In Part 2, queries using the Linux command line from our virtual machine in the cloud.
- In Part 3, queries from a Jupyter Notebook in our virtual machine in the cloud, save the results into Pandas, and present a report enhanced by Pandas output tables and simple data visualizations using Seaborn / Matplotlib.

---

## Part 1 - Querying Data with BigQuery

### Some initial queries

- What's the size of this dataset? (i.e., how many trips)
  * Answer: There are 983,648 rows of data in `bikeshare_trips`, which corresponds to the total number of trips. 
  * SQL query:
```sql
SELECT
  COUNT(*) AS NumTrips
FROM
  `bigquery-public-data.san_francisco.bikeshare_trips`
```

- What is the earliest start date and time and latest end date and time for a trip?
  * Answer: The first bike trip started on August 29, 2013 at 09:08:00 UTC, and the last recorded trip ended on August 31, 2016 at 23:48:00 UTC. 
  * SQL query:
```sql
SELECT
  MIN(start_date) AS MinStartDate,
  MAX(end_date) AS MaxStartDate
FROM
  `bigquery-public-data.san_francisco.bikeshare_trips`
```

- How many bikes are there?
  * Answer: Counting unique bike IDs, there are 700 bikes in use between all of the bike stations.
  * SQL query:
```sql
SELECT
  COUNT(DISTINCT bike_number) AS NumBikes
FROM
  `bigquery-public-data.san_francisco.bikeshare_trips`
```

- Which are the two most popular hours for bike trips across all customer types?
  * Answer: Across all of the customer types, the highest number of trips were started within the 8th and 17th hour.
  * SQL query:
```sql
SELECT
  EXTRACT(HOUR FROM start_date) AS hour,
  COUNT(*) AS num_trips,
FROM
  `bigquery-public-data.san_francisco.bikeshare_trips`
GROUP BY
  hour
ORDER BY
  num_trips DESC
LIMIT
  2
```
- What cities have the most and least number of stations?
  * Answer: Grouping by distinct landmarks, the data shows that San Francisco has the maximum number of stations (37), while Palo Alto contains the least (5) number of stations. 
  * SQL query:
```sql
SELECT
  landmark,
  COUNT(*) AS num_stations
FROM
  `bigquery-public-data.san_francisco.bikeshare_stations`
GROUP BY
  landmark
ORDER BY
  num_stations DESC
```
- At what hour of the day did the longest trip start?
  * Answer: The longest trip recorded was 4797.3 hours, and it started within the 22nd hour.
  * SQL query:
```sql
SELECT
  ROUND(MAX(duration_sec/3600),2) AS max_trip_hours,
  EXTRACT(HOUR FROM start_date) AS hour,
FROM
  `bigquery-public-data.san_francisco.bikeshare_trips`
GROUP BY
  hour
ORDER BY
  hour
```
### Bonus queries

- Top 5 popular station pairs in each region?
```sql
SELECT
t1.region_id AS REGION,
CONCAT(LEAST(start_station_id, end_station_id)," <> ",GREATEST(start_station_id, end_station_id)) AS TRIP_PAIR,
COUNT(*) AS PAIR_COUNT,
ROW_NUMBER() OVER(PARTITION BY t1.region_id ORDER BY COUNT(CONCAT(LEAST(start_station_id, end_station_id)," <> ",GREATEST(start_station_id, end_station_id))) DESC) AS PAIR_RANK_FOR_REGION,

FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips` AS t
JOIN (SELECT DISTINCT region_id, station_id FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t1 ON t1.station_id = t.start_station_id
JOIN (SELECT DISTINCT region_id, station_id FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t2 ON t2.station_id = t.end_station_id

WHERE t1.region_id = t2.region_id # Need to ignore pairs that start and end in different regions
GROUP BY REGION, TRIP_PAIR
ORDER BY PAIR_RANK_FOR_REGION, REGION
LIMIT 25 # Top 5 Pairs for 5 Regions = 25
```
- Top 3 most popular regions(stations belong within 1 region)?
```sql
SELECT
t1.region_id AS STARTING_REGION, # Defining the region by the starting station
SUM(CASE WHEN t1.region_id = t2.region_id THEN 1 ELSE 0 END) AS TRIP_END_SAME_REGION,
SUM(CASE WHEN t1.region_id != t2.region_id THEN 1 ELSE 0 END) AS TRIP_END_DIFF_REGION,
COUNT(*) AS NUM_TRIPS,

FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips` AS t
JOIN (SELECT DISTINCT region_id, station_id FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t1 ON t1.station_id = t.start_station_id
JOIN (SELECT DISTINCT region_id, station_id FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t2 ON t2.station_id = t.end_station_id

GROUP BY STARTING_REGION
ORDER BY NUM_TRIPS DESC
LIMIT 3
```
- Total trips for each short station name in each region?
```sql
SELECT
t1.region_id AS STARTING_REGION, # Defining the region and station by the starting station
t1.short_name AS STARTING_STATION,
SUM(CASE WHEN t1.region_id = t2.region_id THEN 1 ELSE 0 END) AS TRIP_END_SAME_REGION,
SUM(CASE WHEN t1.region_id != t2.region_id THEN 1 ELSE 0 END) AS TRIP_END_DIFF_REGION,
COUNT(*) AS NUM_TRIPS,

FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips` AS t
JOIN (SELECT DISTINCT region_id, station_id, short_name FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t1 ON t1.station_id = t.start_station_id
JOIN (SELECT DISTINCT region_id, station_id, short_name FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t2 ON t2.station_id = t.end_station_id

GROUP BY STARTING_STATION, STARTING_REGION
ORDER BY STARTING_REGION ASC, NUM_TRIPS DESC
```

- What are the top 10 used bikes in each of the top 3 region? These bikes could be in need of more frequent maintenance?
```sql
SELECT
t1.region_id AS REGION,
bike_number AS BIKE_NUMBER,
COUNT(*) AS NUM_TRIPS,
ROW_NUMBER() OVER(PARTITION BY t1.region_id ORDER BY COUNT(*) DESC) AS BIKE_RANK_FOR_REGION,

FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips` AS t
JOIN (SELECT DISTINCT region_id, station_id FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t1 ON t1.station_id = t.start_station_id
JOIN (SELECT DISTINCT region_id, station_id FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`) AS t2 ON t2.station_id = t.end_station_id

WHERE t1.region_id IN (3,5,12) # Popular regions
GROUP BY REGION, BIKE_NUMBER
ORDER BY BIKE_RANK_FOR_REGION, REGION
LIMIT 30 # Top 10 for 3 Regions = 30
```
---

## Part 2 - Querying data from the BigQuery CLI 

### Queries

-  What's the size of this dataset? (i.e., how many trips)
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT 
      COUNT(*) AS NumTrips
    FROM
       `bigquery-public-data.san_francisco.bikeshare_trips`'
```
  * Answer:
  
| NumTrips |
| -------- |
|   983648 |

- What is the earliest start time and latest end time for a trip?
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT
      MIN(start_date) AS MinStartDate,
      MAX(end_date) AS MaxStartDate
    FROM
      `bigquery-public-data.san_francisco.bikeshare_trips`'
```
  * Answer:
  
|    MinStartDate     |    MaxStartDate     |
| ------------------- | ------------------- |
| 2013-08-29 09:08:00 | 2016-08-31 23:48:00 |

- How many bikes are there?
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT
      COUNT(DISTINCT bike_number) AS NumBikes
    FROM
      `bigquery-public-data.san_francisco.bikeshare_trips`'
```
  * Answer:
| NumBikes |
| -------- |
|      700 |

- How many trips are in the morning vs in the afternoon?
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT
      COUNT(*) AS NumTrips,
      TimeOfDay,
    FROM
      (SELECT *,
        # This case statement simplifies the embedded calculation for `time_of_day_split` and segments into morning/afternoon/other categories.
        (CASE WHEN (time_of_day_split = "morning: +6-12") OR (time_of_day_split = "morning: 6-12+") THEN "morning"
        WHEN (time_of_day_split = "afternoon: +12-18") OR (time_of_day_split = "afternoon: 12-18+") THEN "afternoon"
        ELSE "other" END) AS TimeOfDay,
      FROM
        (SELECT *,
          # This calculates the number of trips where the majority of the trip took place between 6AM-12PM, starting before 6AM
          (CASE WHEN (EXTRACT(HOUR FROM start_date) >= 0) AND (EXTRACT(HOUR FROM start_date) < 6) AND (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) >= 6) AND (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) < 12) THEN "morning: +6-12"
          # This calculates the number of trips where the majority of the trip took place between 6AM-12PM, starting 6AM-12PM
          WHEN (EXTRACT(HOUR FROM start_date) >= 6) AND (EXTRACT(HOUR FROM start_date) < 12) AND (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) < 12) THEN "morning: 6-12+"
          # This calculates the number of trips where the majority of the trip took place between 12PM-6PM, starting before 12PM
          WHEN (EXTRACT(HOUR FROM start_date) >= 6) AND (EXTRACT(HOUR FROM start_date) < 12) AND (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) >= 12) AND (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND))< 18) THEN "afternoon: +12-18"
          # This calculates the number of trips where the majority of the trip took place between 12PM-6PM, starting 12PM-6PM
          WHEN (EXTRACT(HOUR FROM start_date) >= 12) AND (EXTRACT(HOUR FROM start_date) < 18) AND (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) < 18) THEN "afternoon: 12-18+"
          ELSE "other" END) AS time_of_day_split,
        FROM 
          `bigquery-public-data.san_francisco.bikeshare_trips`))
    WHERE 
      TimeOfDay != "other" # Removes extra data from print out
    GROUP BY 
      TimeOfDay'
```
  * Answer:
| NumTrips | TimeOfDay |
| -------- | --------- |
|   388538 | afternoon |
|   392520 | morning   |

There are 392,520 morning trips, with the majority of the duration of their trip between 6AM and 12PM, and there are 388,538 afternoon trips, with the majority of the duration of their trip between 12PM and 6PM. 

### Project Questions
Identify the main questions you'll need to answer to make recommendations (list below, add as many questions as you need).

- Question 1: How many one-way trips are there?

- Question 2: For each subscriber type, during what starting hours do you see peak usage of one-way trips? 

- Question 3: For subscribers, is there a similar peak of one-way trips over the weekend?

- Question 4: What is the average duration of one-way trips that take place around 7-10AM and 4-7PM during the week? 

- Question 5: What are the 5 most popular trips that you would call "commuter trips"?

- Question 6: How many customers are ending their trips during popular commuter starting stations?

### Answers
Answer at least 4 of the questions you identified above You can use either BigQuery or the bq command line tool.  Paste your questions, queries and answers below.

- Question 1: How many one-way trips are there?
  * Answer: By calculating how many trips started and ended at different stations, 951,601 one-way trips were counted in this dataset. 
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT
      CASE WHEN start_station_id = end_station_id THEN "round trip" ELSE "one-way" END AS TripType,
      COUNT(*) AS NumTrips,
    FROM
      `bigquery-public-data.san_francisco.bikeshare_trips`
    GROUP BY
      TripType'
```
| TripType   | NumTrips |
| ---------- | -------- |
| round trip | 32047    |
| one-way    | 951601   |

- Question 2: For each subscriber type, during what times do you see peak usage of one-way trips by starting hour?
  * Answer: For customers, the peak usage is in the early to late afternoon (starting between 12-5PM), and for subscribers, there is a morning (starting between 7-10AM) and late afternoon (starting between 4-7PM) peak in trips.
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT
      EXTRACT(HOUR FROM start_date) AS TripStartingHour,
      SUM(CASE WHEN subscriber_type = "Customer" THEN 1 ELSE 0 END) AS NumCustomerTrips, # Count customer trips
      SUM(CASE WHEN subscriber_type = "Subscriber" THEN 1 ELSE 0 END) AS NumSubscriberTrips, # Count subscriber trips
    FROM
      `bigquery-public-data.san_francisco.bikeshare_trips`
    WHERE
      start_station_id != end_station_id # One-way trip
    GROUP BY
      TripStartingHour
    ORDER BY
      TripStartingHour'
```
| TripStartingHour | NumCustomerTrips | NumSubscriberTrips |
| ---------------- | ---------------- | ------------------ |
| 0                | 659              | 2016               |
| 1                | 480              | 953                |
| 2                | 328              | 445                |
| 3                | 154              | 390                |
| 4                | 123              | 1223               |
| 5                | 212              | 4751               |
| 6                | 693              | 19369              |
| 7                | 2194             | 64592              |
| 8                | 4728             | 126586             |
| 9                | 5535             | 88934              |
| 10               | 6664             | 34008              |
| 11               | 9010             | 28681              |
| 12               | 10191            | 33362              |
| 13               | 10534            | 30125              |
| 14               | 10388            | 24365              |
| 15               | 10625            | 34099              |
| 16               | 10725            | 75319              |
| 17               | 9998             | 114168             |
| 18               | 7673             | 75129              |
| 19               | 4858             | 35083              |
| 20               | 3207             | 18698              |
| 21               | 2444             | 12230              |
| 22               | 2004             | 7816               |
| 23               | 1229             | 4603               |

- Question 3: For subscribers, is there a similar peak of one-way trips over the weekend?
  * Answer: Subscribers have the same trip peak hours during the weekday as in Question 2. However, on a weekend day (Saturday or Sunday), the peak hours shift to the late mornning - early afternoon timeframe (starting between 11AM-1PM).
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT
      EXTRACT(HOUR FROM start_date) AS TripStartingHour,
      SUM(CASE WHEN EXTRACT(DAYOFWEEK from start_date) IN (1,7) THEN 1 ELSE 0 END) AS NumWeekendTrips,
      SUM(CASE WHEN EXTRACT(DAYOFWEEK from start_date) IN (2,3,4,5,6) THEN 1 ELSE 0 END) AS NumWeekdayTrips,
    FROM
      `bigquery-public-data.san_francisco.bikeshare_trips`
    WHERE
       (start_station_id != end_station_id) AND (subscriber_type = "Subscriber") # One-way trips and Subscribers only
    GROUP BY
      TripStartingHour
    ORDER BY 
      TripStartingHour'
``` 
| TripStartingHour | NumWeekendTrips | NumWeekdayTrips |
| ---------------- | --------------- | --------------- |
| 0                | 797             | 1219            |
| 1                | 463             | 490             |
| 2                | 246             | 199             |
| 3                | 61              | 329             |
| 4                | 52              | 1171            |
| 5                | 193             | 4558            |
| 6                | 436             | 18933           |
| 7                | 981             | 63611           |
| 8                | 2209            | 124377          |
| 9                | 3373            | 85561           |
| 10               | 4194            | 29814           |
| 11               | 4693            | 23988           |
| 12               | 4657            | 28705           |
| 13               | 4519            | 25606           |
| 14               | 4175            | 20190           |
| 15               | 4257            | 29842           |
| 16               | 4254            | 71065           |
| 17               | 3795            | 110373          |
| 18               | 3297            | 71832           |
| 19               | 2453            | 32630           |
| 20               | 1923            | 16775           |
| 21               | 1487            | 10743           |
| 22               | 1195            | 6621            |
| 23               | 902             | 3701            |

- Question 4: What is the average duration of one-way trips that take place around 7-10AM and 4-7PM during the week?
  * Answer: For subscribers, where the halfway point lies during the morning or afternoon commute time, the average trip length is 9.05 minutes with a standard deviation of 10.67 minutes. For customers, the average trip length is 31.34 minutes with a standard deviation of 108.04 minutes.
  * SQL query:
```sql
bq query --use_legacy_sql=false '
    SELECT 
      ROUND(AVG(duration_sec/60),2) AS AvgTripLength_Min,
      ROUND(STDDEV(duration_sec/60),2) AS StdTripLength_Min,
      subscriber_type as SubscriberType
    FROM 
      (SELECT *,
        CASE WHEN (((EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) < 10) AND 
        (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) >= 7)) OR 
        ((EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) < 19) AND 
        (EXTRACT(HOUR FROM TIMESTAMP_ADD(start_date, INTERVAL CAST(duration_sec/2 AS INT64) SECOND)) >= 16))) 
        THEN "Commuter Hours" ELSE "Non-Commuter Hours" END AS Commute,
      FROM
        `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE
  (start_station_id != end_station_id)) # One-way trips
WHERE
  (Commute = "Commuter Hours") AND EXTRACT(DAYOFWEEK from start_date) IN (2,3,4,5,6) # Only during commute hours and on a weekday
GROUP BY
  SubscriberType'
```

| AvgTripLength_Min | StdTripLength_Min | SubscriberType |
| ----------------- | ----------------- | -------------- |
| 9.05              | 10.67             | Subscriber     |
| 31.34             | 108.04            | Customer       |

---

## Part 3 - Employ notebooks to synthesize query project results

### Get Going

Create a Jupyter Notebook against a Python 3 kernel named Project_1.ipynb in the assignment branch of your repo.

#### Run queries in the notebook 

At the end of this document is an example Jupyter Notebook you can take a look at and run.  

You can run queries using the "bang" command to shell out, such as this:

```
! bq query --use_legacy_sql=FALSE '<your-query-here>'
```

- NOTE: 
- Queries that return over 16K rows will not run this way, 
- Run groupbys etc in the bq web interface and save that as a table in BQ. 
- Max rows is defaulted to 100, use the command line parameter `--max_rows=1000000` to make it larger
- Query those tables the same way as in `example.ipynb`

Or you can use the magic commands, such as this:

```sql
%%bigquery my_panda_data_frame

select start_station_name, end_station_name
from `bigquery-public-data.san_francisco.bikeshare_trips`
where start_station_name <> end_station_name
limit 10
```

```python
my_panda_data_frame
```

#### Report in the form of the Jupter Notebook named Project_1.ipynb

- Using markdown cells, MUST definitively state and answer the two project questions:

  * What are the 5 most popular trips that you would call "commuter trips"? 
  
  * What are your recommendations for offers (justify based on your findings)?

- For any temporary tables (or views) that you created, include the SQL in markdown cells

- Use code cells for SQL you ran to load into Pandas, either using the !bq or the magic commands

- Use code cells to create Pandas formatted output tables (at least 3) to present or support your findings

- Use code cells to create simple data visualizations using Seaborn / Matplotlib (at least 2) to present or support your findings

### Resource: see example .ipynb file 

[Example Notebook](example.ipynb)

