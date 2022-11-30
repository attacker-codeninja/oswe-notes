# Deserialization

### Notes
- Purpose is to convert a data structure into a format that can be stored or transmitted over a network link for future consumption.
- Involves a "producer" and a "consumer" of the serialized object. 
- E.g. An application can define and instantiate an arbitrary object and modify its state in some way. It can then store the state of that object in the appropriate format (for example a binary file) using serialization. As long as the format of the saved file is understood by the "consumer" application, the object can be recreated in the process space of the consumer and further processed as desired.

