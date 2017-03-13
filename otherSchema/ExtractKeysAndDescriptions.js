var fs = require('fs'),
    path = require('path');

var jsonFile = 'E:\\GitHub\\USGIN\\json-metadata\\CINERGI_MetadataObjectJSONSchema.json',
    baseFolder = path.dirname(require.main.filename),
    output = path.join(baseFolder, 'KeysDescriptions-output.txt');

fs.readFile(jsonFile, 'utf8', function (err, data) {
    if (err) console.log(err);
    var json = JSON.parse(data);


    function recursiveJson(o, theContainer) {
        for (var key in o) {
            if (o.hasOwnProperty(key)) {
                if (key.search('cmd:') > -1) {
                    var descText = 'no description';
                    if (o[key]['description']) {
                        descText = o[key]['description']
                    }
                    var writeData = (key + '\t \"' + descText + '\"\t ' + theContainer + '\n');
//                    console.log(writeData);
                    fs.appendFile(output, writeData, function (err) {
                        if (err) console.log(err)
                    });
                    recursiveJson(o[key], key)
                }
            }
            if (o[key] && (key == 'properties')) {
                recursiveJson(o[key], theContainer)
            }
            if (o[key] && (key == 'items')) {
                recursiveJson(o[key], theContainer)
            }
            if (o[key] && (key == 'definitions')) {
                recursiveJson(o[key], '')
            }
            if (o[key] && (key == 'anyOf')) {
                for (var akey in o[key]){
                recursiveJson(o[key][akey], theContainer)
            }}
        }

    }

    recursiveJson(json, '');
});