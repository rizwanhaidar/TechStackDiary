Apache Kafka 101: Introduction.
    What is an Event: Things that have happened, combined with the information about what has happened. It is a combination of Notifications.
            e.g: Someone Clicked on a link, A Microservice completed its tasks, Business Process Change.
        Notification: Element of When-ness of a things. (Can be used to trigger some other activity/activities)
            +
        State: its is small, usually less than a MB and of a structured format (Json, Avro etc) State is serialized in some usually standard    
                format.
        Data Model of an Event:
            Key Value Pair
            Kafka Internally is loosely type but the outside for example the programming language that we are using might not be loosely typed.
            Key value pair concept is not what we think of it, it is not a unique identifier of an event but of some object or entity in the kafka. More details to follow...

        
