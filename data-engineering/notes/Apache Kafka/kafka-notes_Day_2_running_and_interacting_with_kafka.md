Where to start:
    Create a Confluent Cloud Account (Most easiest way to use Apache Kafka)
    https://www.confluent.io/confluent-cloud/tryfree/?session_ref=https%3A%2F%2Fwww.google.com%2F&_gl=1*1x530yq*_gcl_au*MTc0OTI4NzAyNS4xNzM3MjEyMDE1*_ga*NDMzNDYyMjY0LjE3MzcyMTIwMTY.*_ga_D2D3EGKSGD*MTczNzIxMjAxNi4xLjEuMTczNzIxMjk2My4yOS4wLjA.

Kafka:
    is a collection of immutable append only logs, 
Topics:
    Primary Component of Storage in Kafka is called Topic. -> representing a particular data entity.
    Topics in kafka are broken down into smaller Components called partitions.
    When we write a message to a kafka topic, that message is actually stored to the one of the topic's partition.
    Partition to which the message will be routed is based on the key of that topic.
        It is not necessary that the partition number will be same as the key of the topic.
Methoss to Produce or Comsume to/from a Topic:
    Console, Producer/Consumer API from the application that one is building, Kafka Connect. Confluent Cloud Command Line Interface.
    


