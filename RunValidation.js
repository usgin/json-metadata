/**
 * Created by srichard on 9/22/2014.
 */
var fs = require('fs'),
    path = require('path'),
    validate = require('/home/ubuntu/workspace/validate.js');

var inputFile = '/home/ubuntu/workspace/json-metadata/CINERGI_MetadataObjectJSONSchema.json',
    schemaFile = '/home/ubuntu/workspace/json-schema/draft-04/schema',
    resultFile = '/home/ubuntu/workspace/json-metadata/validationResult.json',
    inputjson, schemajson;

function loadinput(inputFile) {
    var data = fs.readFileSync(inputFile, 'utf-8');
    var inputjson = JSON.parse(data);
    return inputjson;
}

function loadschema(schemaFile) {
    var data = fs.readFileSync(schemaFile, 'utf-8');
    var schemajson = JSON.parse(data);
    return schemajson;
}

console.log(validate.validate(loadinput(inputFile),loadschema(schemaFile)));

fs.writeFile(resultFile, validate.validate(loadinput(inputFile),loadschema(schemaFile)), function (err) {
                        if (err) console.log(err)});