var config, mongoUrl, recordsSchema, harvestsSchema, collectionsSchema, mongoDb, mongoose;


// *****************************
// * Records collection schema *
// *****************************
recordsSchema = new mongoose.Schema({
    _id: {
        type: String,
        required: true,
        unique: true
    },
    Title: {
        type: String,
        required: true
    },
    Description: {
        type: String,
        required: true
    },
    PublicationDate: {
        type: Date,
        required: true
    },
    ResourceId: {
        type: String,
        required: false
    },
    Authors: [{
        // this is an Agent object; the agent role is hard coded
        // see the relatedAgent object in USGINMetadataJSONschema.json
        Name: {
            type: String,
            required: false
        },
        OrganizationName: {
            type: String,
            required: false
        },
        ContactInformation: {
            Phone: {
                type: String,
                required: false
            },
            email: {
                type: String,
                required: true
            },
            Address: {
                Street: {
                    type: String,
                    required: true
                },
                City: {
                    type: String,
                    required: true
                },
                State: {
                    type: String,
                    required: true
                },
                Zip: {
                    type: String,
                    required: true
                }
            }
        }
  }],
    Keywords: [],
    GeographicExtent: {
        NorthBound: {
            type: Number,
            required: true,
            min: -90,
            max: 90
        },
        SouthBound: {
            type: Number,
            required: true,
            min: -90,
            max: 90
        },
        EastBound: {
            type: Number,
            required: true,
            min: -180,
            max: 180
        },
        WestBound: {
            type: Number,
            required: true,
            min: -180,
            max: 180
        }
    },
    Distributors: [{ // this is an Agent object; the agent role is hard coded
        // see the relatedAgent object in USGINMetadataJSONschema.json
        Name: {
            type: String,
            required: false
        },
        OrganizationName: {
            type: String,
            required: false
        },
        ContactInformation: {
            Phone: {
                type: String,
                required: false
            },
            email: {
                type: String,
                required: true
            },
            Address: { //SMR note-- I think we can put postal address all in one field
                // what are the use cases for having fielded City, State, Zip?
                Street: {
                    type: String,
                    required: true
                },
                City: {
                    type: String,
                    required: true
                },
                State: {
                    type: String,
                    required: true
                },
                Zip: {
                    type: String,
                    required: true
                }
            }
        }
  }],
    Links: [{
        //  see the LinkObject object in USGINMetadataJSONschema.json
        URL: {
            type: String,
            required: true
        },
        Name: {
            type: String,
            required: false
        },
        Description: {
            type: String,
            required: false
        },
        Distributor: {
            type: String,
            required: false
        },
        ServiceType: {
            type: String,
            required: false
        }
  }],
    MetadataContact: {
        // this is an Agent object; the agent role is hard coded
        // see the relatedAgent object in USGINMetadataJSONschema.json
        Name: {
            type: String,
            required: false
        },
        OrganizationName: {
            type: String,
            required: false
        },
        ContactInformation: {
            Phone: {
                type: String,
                required: false
            },
            email: {
                type: String,
                required: true
            },
            Address: {
                Street: {
                    type: String,
                    required: true
                },
                City: {
                    type: String,
                    required: true
                },
                State: {
                    type: String,
                    required: true
                },
                Zip: {
                    type: String,
                    required: true
                }
            }
        }
    },
    HarvestInformation: {
        //SMR-- 2014-09-09added this object into USGINMetadataJSONschema.json
        OriginalFileIdentifier: {
            type: String,
            required: false
        },
        OriginalFormat: {
            type: String,
            required: false
        },
        HarvestRecordId: {
            type: String,
            required: true
        },
        HarvestURL: {
            type: String,
            required: true
        },
        HarvestDate: {
            type: String,
            required: true
        }
    },
    Collections: {
        type: Array,
        required: true
    },
    Published: {
        type: Boolean,
        required: true
    }
});
