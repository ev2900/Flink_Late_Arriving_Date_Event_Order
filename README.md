# Flink Late Arriving / Out of Order Events

How can we handle late arriving data in Flink and what are the implications on message order?

## Background

We need to understand a few key concepts before we can have a meaningful disscussion on late arriving data and message/event order.

### Notions of Time

Flink has four notions of time

| Notion of Time  | Description                                                                      |
| ----------------|----------------------------------------------------------------------------------|
| Event Time      | timestamp created by the edge device producing the event                         |
| Storage Time    | timestamp added to the event when it is ingested by Kinesis or Kafka             |
| Ingestion Time  | timestamp when the event enters Flink                                            | 
| Processing Time | timestamp when Flink processes the event respective to a given Flink operation   |

When choicing a notion of time a few key considerations 
* Event time and storage times are immutable to Flink. If you reprocess the same event multiple times the event time and storage time value(s) never change. 
* Ingest and processing times are mutable to Flink. If you reprocess the same event multiple times you will get different ingest and processing time value(s) each time you reprocess.
* Since event time and storage time are immutable they are also deterministic. Recomputing calculations that are dependent on event time or storage time will produce the same results each time you reprocess.
* Since ingest and processing time are mutable they are NOT deterministic. Recomputing calculations that are dependent on ingest or processing time may or may not produce the same results each time you recompute.

Being immutable and deterministic are generally favorable. Consequently developers often chose to use event time as Flink's notion of time.

### Watermarks

How does Flink determine if an event is on time or late? 

Flink determines if an event is late by comparing the timestamp in the event (assuming we are using event time as our notion of time) to the most current watermark it keeps track of.
* If the timestamp in the event < the water mark = event is labeled as late.
* If the timestamp in the event > the watermark = event is consider on time.

Since Flink is comparing messages to this watermark to determine if they are late or not; what is a watermark?

A watermark is a time stamp. More specificlly it is a time stamp that Flink tracks internally to know up to what point in time it has processed events for. Watermark is a way of telling Flink how far it is, in the event time. When Flink receives a watermark, it understands (assumes) that it is not going to see any message older than that watermark time stamp. If it does see an event older then the watermark it labels the event as late.

## Implementation

Since Flink uses the watermark timestamp as a point of comparision to determine if a message should be labeled as late, what does an implementation of a common watermark strategy on event time look like? 

The implementation examples will assume that you are using the SQL APIs for Flink. They will assume we are working with a subset of the NYC Taxi cab data. 

When using the [SQL API](https://nightlies.apache.org/flink/flink-docs-release-1.13/docs/dev/table/sql/overview/) for Flink we set the definition for the watermark when we define the table. 

In the example below we use the ```pickup_datetime``` feild from the event as the watermark. We offset the watermark by 5 seconds via. ```pickup_datetime - INTERVAL '5' SECOND``` this sets the watermark value as 5 second earlier then the value of the ```trip_distance``` field. This allows events to arrive upto 5 seconds *late* without being labeled late by Flink. However as disscussed in the background this does introduce the possibility of out of order data within the 5 second offset.

Example Flink SQL code
 
```
CREATE TABLE yellow_cab (
   `VendorID` INT,
   `pickup_datetime` TIMESTAMP(3),
   `dropoff_datetime` TIMESTAMP(3),
   `passenger_count` INT,
   `trip_distance` FLOAT,
    WATERMARK FOR pickup_datetime AS pickup_datetime - INTERVAL '5' SECOND
) 
 WITH (
   'connector' = 'kinesis',
   'stream' = 'yellow-cab-trip',
   'aws.region' = 'us-east-1',
   'scan.stream.initpos' = 'LATEST',
   'format' = 'json'
)
```

If we were to set the watermark for this table with out the 5 second offset. Then data won't be able to arrive within the 5 second grace period and not be labeled as late.
