# Flink Out of Order Data

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

### Water Marks

How does Flink determine if an event is on time or late? 

Answer. Flink compares the timestamp in the event (assuming we are using event time as our notion of time) to the most current watermark it keeps track of.
* If the timestamp in the event < the water mark = event is labeled as late.
* If the timestamp in the event > the watermark = event is consider on time.

Since Flink is comparing messages to this watermark to determine if they are late or not; what is a watermark?

Answer. A watermark is a time stamp. More specificlly  
