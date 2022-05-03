# Flink Out of Order Data

How can we handle out of order data in Apache Flink? Lets start by establishing a common background on the different notions of time. 

Flink has 4 notions of time

1. Event Time - timestamp recorded by the edge device producing the event
2. Storage Time - timestamp added to the event when it is ingested by Kinesis or Kafka
3. Ingestion Time - timestamp when Flink ingests the event  
4. Processing Time - timestamp when Flink processes the an event


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
