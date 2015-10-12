# ...because metadata is the engine of data discovery and reuse...

Ryan Clark started a JSON encoding of a generic metadata model that incorporates concepts from ISO19115, ISO19119, FRBR, and FGDC CSDGM in 2012. The entry-point for his initial work is a [JSON-schema](http://json-schema.org) document located [here on Github](http://raw.github.com/usgin/json-metadata/master/schemas/metadataRecord.json).

A [new JSON schema for science resource metadata](https://github.com/usgin/json-metadata/blob/master/USGINMetadataJSONschemav2.1.json) based on draft-4 of the JSON schema RFC has  been generated, including content for a comprehensive suite of metadata properties from ISO19115 (2006, -1 and -2), ISO19119, ISO19110, ISO11179, ISO19157, and FGDC CSDGM.  A [UML model for some key metadata elements]( 
http://usgin.github.io/usginspecs/metadataModel/index.htm) provides an overview of the content (2015-10-10 note the UML is somewhat out of sync with the current JSON...).  Where element names in the JSON schema correspond to elements in one of the source models, the names have been kept similar to facilate mappings.

2015-10-10 Updated schema to v2.1; validate using http://jsonschemalint.com/draft4/#, and use USGIN metadata JSON schema (USGINMetadataJSONschemav2.1.json)  to validate the JSON example (ExampleUSGIN-JSONmetadata2.1.json). 

The schema is constructed with modules, currently all in one file with the various module 'objects' in the definitions section of the schema. One design objective is to keep the required JSON paths to access any particular object as short as possible. This goal dictates minimizing the depth of element nesting and making the JSON keys include more of the element context (resulting in longer key names...).  To the extent possible, the implementation attempts to provide only one way to encode any particular fact, to avoid some of the problems the source scheme that provides multiple possible paths to implement the same documentation in various cases (e.g. format and digitalTransferOptions in ISO19115).

JSON keys are namespace scoped, and a JSON-LD context is included, but the linking to the various metadata vocabularies has not been done. The long- term goal is to implement linked data elements that would make integration across various metadata implementations simpler.



Stephen M Richard, Ryan Clark, 2012
