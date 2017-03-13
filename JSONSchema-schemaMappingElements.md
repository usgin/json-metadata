# Explanation of schema mapping encoding in the CINERGI JSON schema

Stephen M. Richard 2017-03-12

The CINERGI MinimalMetadataSchema is a reduced version of the full USGIN Metadata JSON schema. JSON that is consistent with the MinimalMetadata Schema will be consistent with the full schema, but not vice-versa.

Within the schema there are 'search_path' keys, and the objects at these keys provide guidance on mapping  from DataCite XML, ISO19115(19139) or ISO19115-2(19139-2) XML to the JSON.  No gmi (ISO19115-2) elements are used in any of the metadata properties here, so the JSON can  be accurately mapped  to ISO19115(19139) or ISO19115-2(19139-2) by using either ```gmd:MD_Metadata``` or ```gmi:MI_Metadata``` as the root element in the output document. Not all  of the content maps to DataCite XML because it is a relatively light weight schema.

### Prefixes

namespace prefixes that show up in this document:

```jmd:  http://resources.usgin.org/uri-gin/usgin/schema/json/3.2/metadata```  namespace identifies the vocabulary for the JSON  keys in the metadata integration scheme

```gmd: http://www.isotc211.org/2005/gmd```  Namespace for ISO19115(19139)

```gmi: http://www.isotc211.org/2005/gmi```  namespace for ISO19115-1(19139-1)

```gco: http://www.isotc211.org/2005/gco```  geospatial common namespace, defines basic data types for ISO schema

## *Explanation of search_paths*

Each search_path key contains an array object; each element in the array is a mapping object.


### schema key

Each mapping object element in the search_paths array has a 'schema' key. String values for this key indicate the target schema for the mapping. Currently the valid values are:

-'ISO 19139' -- use for ISO19115(19139) or ISO19115-2(19139-2)

-'DataCite v3' -- use for DataCite, specifically v3.1, but should work with three, and probably with v4 as well since no validation is done. 

### path key

the path key value is an Xpath in the target xml schema from which content should be taken to generate the value for the containing JSON key.  If the xpath resolves to a string, date or number, that value is used as the value for the containing JSON key. if the xpath resolves to an xml node, that node is used as the context node for xpaths in JSON object that is the value for the containing JSON key. A value of 'missing' for the 'path' key indicates that the content is not present in the source xml schema.

***Example***

```
"search_paths": [
    {"schema": "ISO 19139",
        "path": "//gmd:fileIdentifier/gco:CharacterString"
    },
    {"schema": "DataCite v3",
        "path": "missing"
    }
]
```

This array of mapping objects in this search_paths key indicate that:

1. if the input xml being mapped to JSON is ISO19139 (gmd:) or ISO19139-2 (gmi:) the containing JSON key should have a value that is the string found at the xpath ```//gmd:fileIdentifier/gco:CharacterString```  the // xpath notation indicates to selects nodes in the document that match the selection no matter where they are. Thus the correct value will be found in either gmd: or gmi: metadata. If the xpath does not resolve to a node, or there is no value at the node, the JSON key containing the search_paths element should not be generated in the output document.

2. if the input xml being mapped is DataCite xml, there is no corresponding metadata content and the containing JSON key should not be created in the mapped output.

***Example 2--child keys***

```
"jmd:metadataContacts": {
    "type": "array",
    "search_paths": [
        {"schema": "ISO 19139",
            "path": "//gmd:contact"
        },
        {"schema": "DataCite v3",
            "path": "missing"
        }
    ],
    "items": {
        "type": "object",
        "properties": {
            "jmd:agentRole": {
                "type": "object",
                "properties": {
                    "jmd:conceptPrefLabel": {
                        "type": "string",
                        "search_paths": [
                            {"schema": "ISO 19139",
                                "path": "./gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode/@codeListValue"}
                                ]
                    },...
    ```

this section of JSON schema defines a ```jmd:metadataContacts``` key. There is no corresponding content in DataCite metadata, so in that case, no ```jmd:metadataContacts``` key would be generated on mapping. For ISO metadata, if a ```//gmd:contact``` element is present (could be either ```gmd:MD_Metadata/gmd:contact``` or ```gmi:MI_Metadata/gmd:contact```) then a ```jmd:metadataContacts``` key is generated with a value that is an array of JSON objects. The first key in the first JSON object in the array in the contained JSON object is 'jmd:conceptPrefLabel' that has a string value. The xpath ```./gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode/@codeListValue``` locates the value in the source document; the './' notation indicates that this is a path relative to the current context node, in this case the current ```gmd:contact```. 

Note that ```jmd:metadataContacts``` content is an array of objects, and that in ISO metadata, the cardinality of ```gmd:contact``` is 1..*, so there might be multiple values for contact in the source document. If no value is found at the xpath in the source document, the ```jmd:conceptPrefLabel``` would not be created; if none of the keys in the first object element of the ```jmd:metadataContacts``` array has a value, then no object is created. If there are no ```gmd:contact``` elements in the source document that produce content in teh mapped output, then the ```jmd:metadataContacts``` key would be removed from the output stream.

Processing of an input ISO document for this example would produce output something like this if the ```gmd:CI_RoleCode/@codeListValue``` in the first ISO ```gmd:contact``` element is 'pointOfContact':

```
"jmd:metadataContacts":[
    {jmd:agentRole:
        {   "jmd:conceptPrefLabel":"pointOfContact",
            "jmd:...."
        },
        {other keys and values}
    },
    {another agentRole or other sibling}
]
```

### concatenating content

Some search_paths concatenate content from multiple paths in a document:

```
"path": ". || ' > ' || ./@resourceTypeGeneral"
```

In this case, the output string is the content of the current context node, concatenated with a constant-- the string ' > ', concatenated with the value of the @resourceTypeGeneral attribute on the current context node. In this case, the '||' characters are string concatenate operators, because they are  contained within the path string and  are not quoted with single quotes.

In some cases content from multiple elements in source xml is concatenated into the value for a single JSON key. This  is indicated thus:

```
"search_paths": [
    {"schema": "ISO 19139",
        "concat": [
            {"path": "//gmd:metadataStandardName/gco:CharacterString"},
            {"path": "//gmd:metadataStandardVersion/gco:CharacterString"},
            {"delimiter": "||"}
        ]
    }
]
```

This indicates that content at the paths listed should be concatenated to form the string value for the containing JSON key, using the string '||' as a delimiter. The order of the path keys should be honored in the order of the output string elements; if no value is found for a path key, a space should be added to the output string, the delimiter should be inserted. this is to allow the inverse mapping to be determinate. If no delimiter is specified, the space character ' ' should be used.


### 'or' key -- alternate content

In some cases, values for a JSON key may originate in multiple locations in the source XML. These situations are represented thus:

```
"jmd:resourceIdentifiers": {
    "type": "array",
    "search_paths": [
        {"schema": "ISO 19139",
            "or": [
                {"path": "//gmd:identificationInfo//gmd:citation/gmd:CI_Citation/gmd:identifier"},
                {"path": "//gmd:dataSetURI"}
            ]
        },
        {"schema": "DataCite v3",
            "or": [
                {"path": "/resource/alternateIdentifier"},
                {"path": "/resource/identifier"}
            ]
        }
    ]...
                    
```
  
The interpretation of this search_paths content is to produce a ```jmd:resourceIdentifiers``` array of values that come from either of two paths in both the ISO and DataCite cases. If values are found at both paths, two elements in the output array would be generated. If values are found at neither path, the ```jmd:resourceIdentifiers``` key would be removed from the output stream.

### $ref to component schema

Some schema patterns are repeated in multiple locations in input or output documents. These are defined in the 'definitions' key of the JSON schema. In this version of the schema, there are two component object-- AgentObject and LinkObject. These objects are defined with paths relative to specific elements in the source XML. The AgentObject content is defined relative to ISO ```gmd:CI_ResponsibleParty``` and the DataCite ```creator``` or ```contributor``` elements. The LinkObject content is defined relative to the ISO ```gmd:CI_OnlineResource``` element. There is no equivalent construct in DataCite XML. 

```
"jmd:citationResponsibleParties": {
    "type": "array",
    "items": {
        "type": "object",
        "search_paths": [
            {"schema": "ISO 19139",
                "path": "//gmd:identificationInfo//gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty"
            },
            {"schema": "DataCite v3",
                "or": [
                    {"path": "/resource/creators"},
                    {"path": "/resource/contributors"}
                ]
            }
        ],
        "properties": {                
            "jmd:agent": {
                "type": "object",
                "search_paths": [
                    {"schema": "ISO 19139",
                        "path": "./gmd:CI_ResponsibleParty"
                            },
                    {"schema": "DataCite v3",
                        "or": [
                            {"path": "./creator"},
                            {"path": "./contributor"}
                        ]
                    }
                ],
                "properties": {
                    "$ref": "#/definitions/jmd:AgentObject"
            }

```

This example shows the use of the 'or' key in the mapping object, as well as reference to a component defined in the definitions key of the schema. A ```jmd:citationResponsibleParties``` key with a value that is an array of ```jmd:agent``` objects will be created if a  ```gmd:identificationInfo//gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty``` element is found in an ISO document, or if either a ```/resource/creators``` or a ```/resource/contributors``` element is found in a DataCite document. jmd:agent objects in the jmd:citationResponsibleParties array will be populated by creating the jmd:agent objects for each instance of these elements found in the source document. The  content of the jmd:agent object is defined in by the mapping in ```definitions/jmd:AgentObject``` for each ```gmd:CI_ResponsibleParty```, ```/creator```, or ```/contributor``` in the source document that is a childe of the node at the specified xpath found by the search_paths for the ```jmd:citationResponsibleParties``` element. Note that in ISO, there can be multiple ```gmd:citedResponsibleParty``` elements, each with exactly one ```gmd:CI_ResponsibleParty```, but in dataCite there may only be one creators and one contributors element, but each of these can have multiple creator or creator child elements.


### 'if' key--Conditional values, 'constant' key, 'valueOf' key 

In some cases, a logical test is required to determine the a value to insert. This example also shows insertion of constant value or the value of a particular node based on a condition:

```
{
"schema": "DataCite v3",
    "if": [
        {   "path": "./creator",
            "constant": "creator"
        },
        {   "path": "./contributor",
            "valueOf": "./contributor/@contributorType",
            "default": "contributor"
        }
    ]
}
```

The interpretation of this mapping schema, which is for a DataCite mapping, is that if the path 
```./creator``` is present relative to the current  context node, then the value of the containing JSON key is a string constant 'creator'.  If the path ```./contributor``` is present relative to the current context node, then the value of of the containing JSON key is the value found at the xpath ```./contributor/@contributorType```, i.e. the contributorType attribute on the contributor node.

the 'default' value constant is inserted if no value is found at the provided xpath.