var fs = require('fs')
  , path = require('path');

var jsonFile = 'E:\\GitHub\\USGIN\\json-metadata\\MetadataJSONschema.json'
  , baseFolder = path.dirname(require.main.filename)
  , output = path.join(baseFolder, 'KeysDescriptions-output.csv');

fs.readFile(jsonFile, 'utf8', function (err, data) {
  if (err) console.log(err);
  var json = JSON.parse(data);

  function recursiveJson (o) {
    for (var key in o) {
      if (o.hasOwnProperty(key)) {
        if (key.search('jmd:') > -1) {
          var descText = 'no description';
          if (o[key]['description']){
             descText = o[key]['description']
          }
          var writeData = (key + ', \"' + descText + '\"\n');
          fs.appendFile(output, writeData, function (err) {
            if (err) console.log(err)
          })
        }
        if (o[key] && typeof(o[key]) == 'object') {
          recursiveJson(o[key])
        }
          if (o[key] && typeof(o[key]) == 'array') {
          recursiveJson(o[key])
        }
      }
    }
  }
  recursiveJson(json);
});