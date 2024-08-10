# Flink Late Arriving / Out of Order Events

<img width="85" alt="map-user" src="https://img.shields.io/badge/views-615-green"> <img width="125" alt="map-user" src="https://img.shields.io/badge/unique visits-214-green">

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

A watermark is a time stamp. More specificlly it is a time stamp that Flink tracks internally to know up to what point in time it has processed events for. Watermark is a way of telling Flink how far it is in processing in terms of event time. When Flink receives a watermark, it understands (assumes) that it is not going to see any message older than that watermark time stamp. If it does see an event older then the watermark it labels the event as late.

### Late Events (ie. labeled late by Flink)

When Flink labels an event as late, how does it impact the downstream operations in my Flink application?

This depends on what your Flink application is doing. Some operations in Flink are sensitive to late data. Example late data will not be included when calculating a result (average, sum, count ...) in certain scenarios.

Other operations in Flink are not sensitive to late data and will produce the same output regardless of if data is labeled as late or not.

*This section is under construction*

## Implementation

### Table API & SQL

Since Flink uses the watermark timestamp as a point of comparision to determine if a message should be labeled as late, what does an implementation of a common watermark strategy on event time look like?

The implementation examples will assume that you are using the SQL APIs for Flink.

When using the [SQL API](https://nightlies.apache.org/flink/flink-docs-release-1.13/docs/dev/table/sql/overview/) for Flink we set the definition for the watermark when we define the table.

#### Create a Table with Event Time as the Notion of Time and 5 second Offset Watermark

In the example below we use the ```event_timestamp``` feild from the event as the watermark. We offset the watermark by 5 seconds via. ```event_timestamp - INTERVAL '5' SECOND``` this sets the watermark value as 5 second earlier then the value of the ```event_timestamp``` field. This allows events to arrive upto 5 seconds *late* without being labeled late by Flink. However as disscussed in the background this does introduce the possibility of out of order event within the 5 second offset.

Example Flink SQL code (designed to be run via. KDA Studio Zeppelin notebook on AWS)

```
%flink.ssql

DROP TABLE IF EXISTS late_data;

CREATE TABLE late_data (
   `event_timestamp` TIMESTAMP(3),
   `value1` INT,
   WATERMARK FOR `event_timestamp` AS `event_timestamp` - INTERVAL '5' SECOND
)
 WITH (
   'connector' = 'kinesis',
   'stream' = 'late-data',
   'aws.region' = 'us-east-1',
   'scan.stream.initpos' = 'LATEST',
   'format' = 'json'
);
```


If we were to set the watermark for this table without the ```- INTERVAL '5' SECOND```, we would remove the possibility of having out of order events but at the cost of events not being able to arrive late without being labeled as late.

To visualize this example and these concepts in action with sample events view the [Helpful Animations.pptx](https://github.com/ev2900/Flink_Late_Arriving_Date_Event_Order/blob/main/Helpful%20Animations/Helpful%20Animations.pptx) presentation. View the presentation in presentation mode and follow the animations step by step.
