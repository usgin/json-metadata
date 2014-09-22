/**
 * Created by srichard on 9/22/2014.
 */
var fs = require('fs'),
    path = require('path'),
    validate = require('E:\\GitHub\\json-schema\\lib\\validate.js');

var inputFile = 'E:\\GitHub\\USGIN\\json-metadata\\CINERGI_MetadataObjectJSONSchema.json',
    schemaFile = 'E:\\GitHub\\json-schema\\draft-04\\schema',
    resultFile = 'E:\\GitHub\\USGIN\\json-metadata\\validationResult.json',
    inputjson, schemajson;

fs.readFile(inputFile, 'utf8', function (err, data) {
    if (err) console.log(err);
    inputjson = JSON.parse(data)
});

fs.readFile(schemaFile, 'utf8', function (err, data) {
    if (err) console.log(err);
    schemajson = JSON.parse(data)
});

fs.appendFile(resultFile, validate.validate(inputjson,schemajson), function (err) {
                        if (err) console.log(err)
                    });