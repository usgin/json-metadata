var resolveRefs, schemaCopy, schemaUtils, schemas, _,
  __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

_ = require('underscore');

schemas = {
  link: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-link/',
    type: 'object',
    properties: {
      URL: {
        type: 'string',
        format: 'uri',
        required: true
      },
      Name: {
        type: 'string',
        required: false
      },
      Description: {
        type: 'string',
        required: false
      },
      Distributor: {
        type: 'string',
        required: false
      }
    }
  },
  serviceLink: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-service-link/',
    type: 'object',
    properties: {
      ServiceType: {
        type: 'string',
        required: true,
        "enum": ['OGC:WMS', 'OGC:WFS', 'OGC:WCS', 'OPeNDAP', 'ESRI']
      },
      LayerId: {
        type: 'string',
        required: false
      }
    },
    'extends': 'http://resources.usgin.org/uri-gin/usgin/schema/json-link/'
  },
  address: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-address/',
    type: 'object',
    properties: {
      Street: {
        type: 'string',
        required: true
      },
      City: {
        type: 'string',
        required: true
      },
      State: {
        type: 'string',
        required: true
      },
      Zip: {
        type: 'string',
        required: true
      }
    }
  },
  contactInformation: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-contact-information/',
    type: 'object',
    properties: {
      Phone: {
        type: 'string',
        format: 'phone',
        required: false
      },
      email: {
        type: 'string',
        format: 'email',
        required: true
      },
      Address: {
        required: false,
        $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-address/'
      }
    }
  },
  contact: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-metadata-contact/',
    type: 'object',
    properties: {
      Name: {
        type: 'string',
        required: false
      },
      OrganizationName: {
        type: 'string',
        required: false
      },
      ContactInformation: {
        required: true,
        $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-contact-information/'
      }
    }
  },
  geographicExtent: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-geographic-extent/',
    type: 'object',
    properties: {
      NorthBound: {
        type: 'number',
        minimum: -90,
        maximum: 90,
        required: true
      },
      SouthBound: {
        type: 'number',
        minimum: -90,
        maximum: 90,
        required: true
      },
      EastBound: {
        type: 'number',
        minimum: -180,
        maximum: 180,
        required: true
      },
      WestBound: {
        type: 'number',
        minimum: -180,
        maximum: 180,
        required: true
      }
    }
  },
  harvestInfo: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-harvest-information/',
    type: 'object',
    properties: {
      OriginalFileIdentifier: {
        type: 'string',
        required: false
      },
      OriginalFormat: {
        type: 'string',
        required: false
      },
      HarvestRecordId: {
        type: 'string',
        required: true
      },
      HarvestURL: {
        type: 'string',
        required: true
      },
      HarvestDate: {
        type: 'string',
        format: 'date-time',
        required: true
      }
    }
  },
  metadata: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-metadata/',
    type: 'object',
    properties: {
      Title: {
        type: 'string',
        required: true
      },
      Description: {
        type: 'string',
        required: true,
        minLength: 50
      },
      PublicationDate: {
        type: 'string',
        format: 'date-time',
        required: true
      },
      ResourceId: {
        type: 'string',
        required: false
      },
      Authors: {
        type: 'array',
        required: true,
        minItems: 1,
        items: {
          $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-metadata-contact/'
        }
      },
      Keywords: {
        type: 'array',
        required: true,
        minItems: 1,
        items: {
          type: 'string'
        }
      },
      GeographicExtent: {
        required: true,
        $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-geographic-extent/'
      },
      Distributors: {
        type: 'array',
        required: true,
        minItems: 1,
        items: {
          $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-metadata-contact/'
        }
      },
      Links: {
        type: 'array',
        required: true,
        minItems: 0,
        items: {
          $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-link/'
        }
      },
      MetadataContact: {
        required: true,
        $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-metadata-contact/'
      },
      HarvestInformation: {
        required: false,
        $ref: 'http://resources.usgin.org/uri-gin/usgin/schema/json-harvest-information/'
      },
      Collections: {
        type: 'array',
        required: true,
        minItems: 0,
        items: {
          type: 'string'
        }
      },
      Published: {
        type: 'boolean',
        required: true
      }
    }
  },
  collection: {
    id: 'http://resources.usgin.org/uri-gin/usgin/schema/json-metadata-collection/',
    type: 'object',
    properties: {
      Title: {
        type: 'string',
        required: true
      },
      Description: {
        type: 'string',
        required: false
      },
      ParentCollections: {
        type: 'array',
        required: false,
        items: {
          type: 'string'
        }
      }
    }
  }
};

schemaCopy = function(schema) {
  var copy, key, name, sch, value;
  copy = {};
  for (key in schema) {
    sch = schema[key];
    if (key === 'items') {
      copy.items = _.clone(sch);
    } else if (key === 'properties') {
      copy.properties = {};
      for (name in sch) {
        value = sch[name];
        copy.properties[name] = schemaCopy(value);
      }
    } else {
      copy[key] = _.clone(sch);
    }
  }
  return copy;
};

resolveRefs = function(schema) {
  var name, prop, resolved, _ref;
  schema = schemaCopy(schema);
  if (schema.$ref != null) {
    resolved = _.extend({}, schema, schemaUtils.byId(schema.$ref));
    delete resolved.$ref;
  } else {
    resolved = _.extend({}, schema);
  }
  if (resolved['extends'] != null) {
    _.extend(resolved.properties, schemaUtils.byId(resolved['extends']).properties);
  }
  delete resolved['extends'];
  if ((resolved.items != null) && (resolved.items.$ref != null)) {
    resolved.items = resolveRefs(schemaUtils.byId(resolved.items.$ref));
  }
  _ref = resolved.properties;
  for (name in _ref) {
    prop = _ref[name];
    resolved.properties[name] = resolveRefs(prop);
  }
  return resolved;
};

module.exports = schemaUtils = {
  byId: function(id) {
    var name, schema;
    for (name in schemas) {
      schema = schemas[name];
      if ((schema.id != null) && schema.id === id) {
        return schema;
      }
    }
    return null;
  },
  byName: function(name) {
    if (schemas[name] != null) {
      return schemas[name];
    }
    return null;
  },
  all: function() {
    var key, value;
    return (function() {
      var _results;
      _results = [];
      for (key in schemas) {
        value = schemas[key];
        _results.push({
          name: key,
          schema: value
        });
      }
      return _results;
    })();
  },
  validate: function(obj, schema) {
    var item, itemSchema, name, prop, _ref;
    schema = resolveRefs(schema);
    switch (schema.type) {
      case 'string':
        if (!_.isString(obj)) {
          return false;
        }
        if (obj === '' && schema.required) {
          return false;
        }
        if ((schema.minLength != null) && obj.length < schema.minLength) {
          return false;
        }
        if ((schema.maxLength != null) && obj.length > schema.maxLength) {
          return false;
        }
        if ((schema["enum"] != null) && __indexOf.call(schema["enum"], obj) < 0) {
          return false;
        }
        break;
      case 'number':
        if (!_.isNumber(obj)) {
          return false;
        }
        if ((schema.minimum != null) && obj < schema.minimum) {
          return false;
        }
        if ((schema.maximum != null) && obj > schema.maximum) {
          return false;
        }
        break;
      case 'boolean':
        if (!_.isBoolean(obj)) {
          return false;
        }
        break;
      case 'array':
        if (!_.isArray(obj)) {
          return false;
        }
        if (schema.minItems && obj.length < schema.minItems) {
          return false;
        }
        if (schema.maxItems && obj.length > schema.maxItems) {
          return false;
        }
        itemSchema = resolveRefs(schema.items);
        if (__indexOf.call((function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = obj.length; _i < _len; _i++) {
            item = obj[_i];
            _results.push(schemaUtils.validate(item, itemSchema));
          }
          return _results;
        })(), false) >= 0) {
          return false;
        }
        break;
      case 'object':
        if (!_.isObject(obj)) {
          return false;
        }
        _ref = schema.properties;
        for (name in _ref) {
          prop = _ref[name];
          if (prop.required && (obj[name] == null)) {
            return false;
          }
          if ((obj[name] != null) && schemaUtils.validate(obj[name], prop) === false) {
            return false;
          }
        }
    }
    return true;
  },
  resolve: resolveRefs,
  emptyInstance: function(schema) {
    var name, prop, result, _ref;
    schema = resolveRefs(schema);
    switch (schema.type) {
      case 'string':
        return '';
      case 'number':
        return 0;
      case 'boolean':
        return true;
      case 'array':
        return [];
      case 'object':
        result = {};
        _ref = schema.properties;
        for (name in _ref) {
          prop = _ref[name];
          result[name] = schemaUtils.emptyInstance(prop);
        }
        return result;
    }
  }
};
