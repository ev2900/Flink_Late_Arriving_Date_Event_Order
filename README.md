# Flink Out of Order Data

How can we handle out of order data in Apache Flink? Let us start by establishing a common background on the different notions of time. 

Flink has four notions of time

1. Event Time - timestamp created by the edge device producing the event
2. Storage Time - timestamp added to the event when it is ingested by Kinesis or Kafka
3. Ingestion Time - timestamp when the event enters Flink  
4. Processing Time - timestamp when Flink processes the event respective to a given Flink operation

Event time and storage times are immutable to Flink. If you reprocess the same event multiple times the event time and storage time value(s) never change. 

Ingest and processing times are mutable to Flink. If you reprocess the same event multiple times you will get different ingest and processing time value(s) each time you reprocess.

Since event time and storage time are immutable they are also deterministic. Recomputing calculations that are dependent on event time or storage time will produce the same results each time you reprocess.

Since ingest and processing time are mutable they are NOT deterministic. Recomputing calculations that are dependent on ingest or processing time may or may not produce the same results each time you recompute.

Being immutable and deterministic are generaly generally favorable in stream data processing. Consequently developers often chose to use event time as Flink's notion of time.

Using event time as Flink's notion of time has a disadvantage. It creates the possibility of Flink ingesting events that are out of order with respect to event time.




--

When we query data in Flink we can ev

Often we use event time as our notion of time. Using event time has the advantages of being deterministic and immutable. However using event time also has the disadvantage of introducing the possibility of out of order event streams.

To handle out of order events

To handle out of order event streams we first need to consider if the results of the query we are running in Flink can be determined by only looking at the single event or if it requires the context of the events before it and/or after it. 

Example - If we are running a query that is filtering on a given value in a message. 

It does not matter when an event arrives with respect to its event time.

If we are calculating 

Watermarks


Windows
1. Tumbling Window
2. Sliding Window
3. Session Window
4. Global Window
