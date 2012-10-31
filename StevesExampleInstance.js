//A metadata record has two sections, one with information for management of the metadata itself, and one that describes some individual resource. Each metadata record describes exactly 1 resource. The metadata record can be considered a representation of the resource, but it has an identity that is distinct from the identity of the described resource.  There may be more than one metadata record in the system describing a single resource; these should have distinct metadata lineages. Inclusion of this template is didactic.
_metadataRecord = {  
	MetadataInfo: _metadataRecordInfoTemplate, //exactly 1
	DescribedResource: _resourceDescriptionTemplate //exactly 1. This is what the metadata record is about
};

//these are data items for managing the metadata record as a resource.
_metadataRecordInfoTemplate = {  
	MDRecordURI: "http://some.domain.org/metadata/437u4u6", //exactly 1
	MDUpdateDate: "please use a format like this: 2011-10-11T14:30",  //exactly 1. This is time stamp for most recent change to metadata content in this record. Update history should be in Maintenance section; this is a convienence property
	// <<<<<<<<<<<<<<skipped>>>>>>>>>>>>>>>>>
	MDSpecification: _referenceTemplate,  //exactly 1
	// <<<<<<<<<<<<<<skipped>>>>>>>>>>>>>>>>>
	MDMaintenance: _maintenanceTemplate, /* 1..N  contact information is mandatory */
	MDLanguage: "ISO three letter language code", //exactly 0..1 default is eng if no value is specified.
	/* 	MetadataOriginator: [ _partyTemplate ],  //1..N   move to Lineage */
	MDLineage:  _lineageTemplate //0..N
};

// basic metadata that might apply to any resource
_resourceDescriptionTemplate = {
    Title: "The title of the resource being described",  //exactly 1
    Description: "A description of what the resource being described is about", //extactly 1
    Originator: [ _partyTemplate ],  //0..N
    OriginDate: [ _eventDateTemplate ], //0..N  Each date should scope a different origin event
	ResourceURI: "URI",
	AlternateTitle: [ {
		AltTitleText: "title", 
		AltTitleLanguage: "ISO three letter language code"
	} ],  /* 0..N */
	SpatialExtent: [ _extentTemplate ], //allow multiple bounding box extents for non contiguous resource, e.g. map of US coasts.
 	TemporalScope: [ {
		begin:_eventDateTemplate, 
		end:_eventDateTemplate 
		} ], /* 0..N  scope using named time ordinal eras (e.g. geologic time) should be specified using temporal keywords (vocabulary is a time scale) */
	ResourceType: [ _controlledConceptTemplate ], //0..N
	 //ResourceType is a specially recognized keywordTheme that categorizes the resource; at least one type category should be specified, as the type will guide processing of other parts of the metadata record. Resource categorization can be done on many axes. Some example schemes include 'Functional Requirements for Bibliographic Records' (FRBR) entity, which include 'work','expression','manifestation', and 'item' (see http://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records#FRBR_Entities), frbr form here as well (e.g. e.g., novel, play, poem, essay, biography, symphony, concerto, sonata, map, drawing, painting, photograph, etc.), ISO scopeCodes that type resources. The different category schmes can be disambiguated by their VocabularyURI values, but concepts in each should have URIs that are sufficient.
    Tags: ["words"]	/* 0..N  free form keywords
	Keywords: [ {		/* formal keywords */
		KeywordTheme: _controlledConceptTemplate, //typical themes might include 'place', 'temporal', 'thematic', 'ISO topic category' etc...
		Keyword: [ _controlledConceptTemplate ]
		} ],
	ResourceLanguage: "ISO three letter language code",
    Distribution: [ {
		Distributor: _partyTemplate, 
		OnlineAccess: [ _linkTemplate ],  //format information is included in link elements for online resources
		OfflineAccess: {
			AccessInformation: "free text description of how to get resource; only necessary for offline access, otherwise link.description provides details. The links here will be to frbr:expression of the resource. Include turnaround time and business hours information here",
			DistributionMedium: {
				MediumType: _controlledConceptTemplate,
				MediumFormat: _controlledConceptTemplate
			} 
		} ,
		Fees: "text explanation of any payment required to access resource"
	 } ],
	RelatedResource: [ _referenceTemplate ],  //0..N.  browseGraphic is a related resource, many other possibilities here...
	Lineage: _lineageTemplate,
	Quality: _resourceQualityTemplate,
	UsageConstraint: _resourceUsageConstraintTemplate,
	ResourceMaintenance: _maintenanceTemplate, //only one here, because particular maintainence events that update the resource should be recorded in the lineage. This element provides information on how often maintenance is expected to occur and who is doing the maintenance. The resource maintenance contact will be the point of contact for reporting issues with the resource content.
	ResourceTypeDetails: { 
		Publication: _publicationDetailsTemplate, 
		Dataset: _datasetDetailsTemplate, 
		Service: _serviceDetailsTemplate, 
		CoverageDataset: _coverageDetailsTemplate,
		EarthImageCoverage: _earthImageTemplate,
		Software: _softwareTemplate
		}  //extension point-- other detail types might be added, e.g. _specimenTemplate, _bookTemplate, _physicalItemTemplate...
};

_maintenanceTemplate = {
	Contact: [ _partyTemplate ], /* 1..N minimum is contact info for metadata issue reporting */
	Note: "free text information about maintenance plans, workflow, process...", 
	Interval: "time interval between planned maintenance events e.g. '6 months'",
	Frequency: _controlledConceptTemplate,  //0..1
	Date: [ _eventDateTemplate ]	//0..N if nothing changes, can time-stamp to indicate maintenance check points. If record is updated, a process step in metadataLineage should be added.
};

_lineageTemplate = {
	LineageStatement: "free text description of provenance of resource and processing steps in its production",
	History: [ _processStepTemplate ] //0..N
};

_processStepTemplate = {
	Label: "text to characterize,identify this step for user interface listing",
	Party: [ _partyTemplate ], //0..N parties responsible for processing step
	ProcessType: [ _controlledConcept ], //0..N
	ProcessDescription: "description of what was done",
	sequenceNo: 3,  //number each step to all putting them in order. Order of listing is not significant
	InputResource: [ _referenceTemplate ], //0..N
	OutputResource: [ _referenceTemplate ], //0..N
	Event:  [ _eventDateTemplate ], //allow array, may have beginning, end, intermediate times...
	Rationale: "discussion of why the process step was done",  /*0..1 */
	ComputerProcessing: {
		Software: _referenceTemplate
		RunTimeParameters: [ {
			ProcessParameterName: "name of parameter",
			ProcessParameterValue: "parameter value"
		} ]   //0..N
	},
	ProcessExtent: [ _extentTemplate ], //0..N  scope process to a particular geographic location/locations
	ProcessedElements: [ "elementURI" ]		//0..N, URIs for dataset, entity, attribute instances affected by this process
};

// ISO19157 quality model here...
_resourceQualityTemplate = {
	QualityStatement: "free text assessment of resource quality, including quantitative and qualitative measures",  //should this be a resourceType sepecific property?
	QualityScope: {
					ResultScopeLevel: _controlledConceptTemplate,
					ResultExtent: _extentTemplate,
					ResultScopeEnumeration: [_referenceTemplate]	//list of references to items that the result applies to 			
				}	
	QualityReportElements: [ {		//each item in this list is a data quality element
			StandaloneReport: _referenceTemplate,	//URI for a group of elements that might be extracted as a stand alone object.
			ElementType: _controlledConceptTemplate ,
			ElementConfidence: "general statement of confidence in this quality element assessment",  //guessing what the intention in 19157 is supposed to be
			ElementRepresentatity: "general statement of representativity" //whatever that is, see ISO19157
			ElementHomogeneity: "how uniformly this element value applies across the assigned result scope"
			QualityMeasure: {
				MeasureType: _referenceTemplate,
				MeasureLabel: "Text label for users to understand measure type",
				MeasureDescription: "explanation of measureType"
			},
			QualityEvaluation: {
				EvaluationType: _referenceTemplate,  //links to reference docs for evaluation method should be in here
				EvaluationMethodDescription: "text description of the evaluation method",
				EvaluationProcedure: "text description of procedure used to implement evaluation method"
			},
			QualityElementResult: { 
				ResultScope: {
					ResultScopeLevel: _controlledConceptTemplate,
					ResultExtent: _extentTemplate,
					ResultScopeEnumeration: [_referenceTemplate]	//list of references to items that the result applies to 			
				}
				// one of the following three elements is required
				ConformanceResult: {
					ResultSpecification: _referenceTemplate,
					ResultExplanation: "text explanation of result",
					ConformancePass: "True or false"
				},
				ResultDescription: "text description of test result",
				QuantitativeResult: {
					ResultValue: "value may be single number or a list of numbers or strings",
					ResultValueUnits: _controlledConceptTemplate,
					ResultValueType: _controlledConceptTemplate		// if value is a record, link from concept URI should access a description of the record.
				}
			}			
		}	]
};

_resourceUsageConstraintTemplate = {
	ConstraintsStatement: "free text description of legal or security related constraint on access oto or use of the described resource",
	Constraint: {
		ConstraintType: _controlledConceptTemplate,	//e.g. security, access, usage
		ConstraintTerm: _controlledConceptTemplate
		}  //0..N
};

_publicationDetailsTemplate = { 
//title, date, identifier are inherited from context. Publication details will only apply if the describe resource is an frbr:expression or frbr:item. Linkage to online items should still be through distribution linkage elements. If the resource is a work or manifestation, then expressions and items will be distributions of that resource. Tricky...
	Edition: "identifier for edition",
	EditionDate: _eventDateTemplate,
	SeriesTitle: "series title",
	SeriesIssue: "identifier for issue in series",
	Page: "33-54",
	PublicationDescription: "free text with other details specific to this particular manifestation of the resource"
	//might add physicalDistribution elements here for library usage...
};

_datasetDetailsTemplate = {
	DataSchema: _referenceTemplate ,  //link to one or more resources describing the data schema
	DataSetEntites: [ {
		EntityCount: 400,  //number of instances of this entity in a particular dataset instance
		_entityTemplate
		} ],
}; 

_entityTemplate = {  
//entity and attributes in the entity; ISO19110, ISO11179, FGDC entity-attribute information. Construct here describes concrete entities only.
	EntityURI: "URI",		//allows this entity to be referenced externally 
	EntityReference _referenceTemplate,  //an entity defintion my be include by reference to an external resource. If this is used, the rest of the elements in this object are not necessary and may be ignored in processing.
	EntityType: _controlledConceptTemplate,  //feature dataset (collection of related geographic entities unified by spatial reference), relational table, object...
	EntityName: "name of feature class, table, or other entity manifestation",
	AltEntityName: [ {
		AltEntityNameText: "the name string",
		AltEntityNameLanguage: "ISO three letter language code" 
	} ], //0..N
	PartEntity: [ _entityTemplate ], //compound entity like a feature dataset may have several included entities (lines and polys that have topological relationships)
	EntityAttribute: {
		LocalName: "name of attribute specific to context of this entity",
		Cardinality: "1, 0..1, 1..N, 0..N",
		Attribute: [ _attributeTemplate ]
	} , //0..N
	SpatialTopologyType: _controlledConceptTemplate,
	GeometryType: _controlledConceptTemplate,
	SpatialReferenceSystem:  _referenceTemplate,
	Resolution: {
		ResolutionDenominator: 50000,  //0..1
		ResolutionDistance: { 
			ResolutionDistValue: 5,
			ResolutionUOM: _controlledConceptTemplate
		} //0..1
	}
};

_attributeTemplate = {
	AttributeURI: "URI",  //to allow reference to this attribute definition from other objects
	AttributeReference: _referenceTemplate,  //attribute definition may be by reference, in which case rest of elements in this object are unnecessary.	
	PropertySpecified: _controlledConceptTemplate,
	ConceptualDimension: _controlledConceptTemplate, //0..1 e.g. length, mass, concept, velocity. The value here will be related to the valid UOM for the value.
	DataType: _controlledConceptTemplate, //0..1, integer, float, text, URI, reference...
	Domain: _valueDomainTemplate //0..1
};

_serviceDetailsTemplate = { 
//for metadata describing a service, the distribution section should include links to service end point URL's that will provide the service-specific self description document, e.g. THREDDS catalog, OGC GetCapabilities, OpenSearchDescription, WSDL, WADL, etc.  This detail section allows linking to datasets exposed by the service, generic description of the operations provided by the service, and any important bindings between datasets and operations.  It is anticipated that in most cases, this information will be gleaned from the service self-description document. Links to datasets are useful for discovery of services exposing particular datasets (which may be unknown to the dataset originator or metadata record creator
	ServiceType: _referenceTemplate
	CouplingType: _controlledConceptTemplate,
	Operations: [ _serviceOperationTemplate ], //0..N
	CoupledResource: [ {
		OperatesOn: _referenceTemplate,
		CoupledOperation: _serviceOperationTemplate 	//operations specified in this section should not be duplicated in Operations section unless they may also be invoked in a loosely coupled mode
	} ] //0..N reference includes a URI and links to representation for the target dataset; link to metadata for target dataset should be one of these links	
};

_serviceOperationTemplate = {
	OperationURI: "URI",		
	OperationType: _controlledConceptTemplate,  //operations can be categorized using standard vocabularies to assist search/discovery
	InvocationName: "name used to invoke operation in the context of the service",
	OperationDescription: "free text description of what operation does",
	InvocationLink: _linkTemplate  //one or more links for invoking operation. Suggest convention that in the link, strings that begin with '$' and have names matching the InvocationName or a ParameterName can be treated as template slots that indicate where the invocation name and parameters should be inserted in the invocation URL.
	OperationParameter: { 
		ParameterName: "name of parameter",
		ParameterDescription: "description of how to use parameter",
		ParameterDirection: "in, out, or in/out",
		Cardinality: "1, 0..1, 1..N, 0..N",
		ParameterDataType: _controlledConceptTemplate, //integer, float, text, URI, reference...
		ParameterDomain: _valueDomainTemplate
	 }  //0..N parameters for this operation instance
};

_coverageDetailsTemplate  = {
	CoverageType: _controlledConceptTemplate,
	Portrayal: _referenceTemplate,  //link to visualization of coverage, e.g. a browse graphic.
	FeatureOfInterest: _referenceTemplate , //feature that the grid describes/characterizes
	GridDescription: "text description of coverage gridding scheme",
	NGridDimensions: 3,
	GridAxis: [ _gridAxisTemplate ],  //1..N one instance for each grid dimension
	GeoreferencingDescription: "text description of how coverage grid is or may be georeferenced",
	GeoreferenceStatus: _controlledConceptTemplate  //Term to indicate the status of a coverage with respect to establishing georeferencing. Includes e.g. {georeferencable, georectified, georeferenced...}, for coverage that  could be georeferenced, coverage that is georectified such that grid points are regularly located in a geographic coordinate system, georefenced means that information is included with the coverage (e.g. file header or world file) that defines mapping between coverage grid and geographic location.
};

_gridAxisTemplate = {
	PointOrInterval: _controlledConceptTemplate,
	RegularOrIrregular: _controlledConceptTemplate,
	Spacing: {
		CellLength: 20
		CellUOM: _controlledConceptTemplate
		}, 
	Property: _controlledConceptTemplate, 
	AxisDomain: "explanation of value domain for this axis"
};

_earthImageTemplate = {
	IlluminationElevationAngle: 37,
	IlluminationAzimuthAngle: 245,
	ImagingCondition: _controlledConceptTemplate,
	CloudCoverPercent: 0,
	ProcessingLevel: _controllecConceptTemplate,
	CompressionGenerationQuantity: 22,
	TriangulationIndicator: "True or False", //boolean
	RadiometricCalibration: _referenceTemplate,
	CameraCalibration: _referenceTemplate,
	FilmDistortionInformation: _referenceTemplate,
	LensDistortionInformation: _referenceTemplate
};

_softwareTemplate = {		
//this should be considered a rough draft of what might be useful...
	ApplicationScheme: _referenceTemplate,
	OperatingSystem: _controlledConceptTemplate,
	HarwareRequirements: "text describing necessary hardware environment for software to execute",
	Preconditions: "text description of input requirements and state necessary to start execution"
};

//**************************************************************
// general purpose templates *************************************
_controlledConceptTemplate = {  	//SKOS anyone?
	ConceptURI:  "URI string",
	Label:  "string to display",		//this should be in the language specified by metadataLanguage
	AltLabel: [ {
		labelText: "string to display",
		language:  "ISO three letter language code" 
		} ],
	VocabularyURI: "URI string",
	ConceptLinks: [ _linkTemplate ]  //0..N can provide various links to get related concepts, definitions, etc.
};

_partyTemplate = {
	 Role: _controlledConceptTemplate ,
     Party: { 
		Person: [_individualTemplate ], 
		Organization: _organizationTemplate  
		},
     ContactInformation: {
        Phone: [ {
			PhType: "e.g. office, reception, fax, cel", 
			number:"123-456-7890" 
		} ],
        Email: "example@fake.com",
		 // not clear that there is a good reason to disaggregate the address into street, city, country, postal code, etc...
        Address:  "postal address, ideally formatted appropriate to the target country",
		Links: [ _linkTemplate ]  //0..N
     }
};

_individualTemplate = { 
	IndividualURI: "personURI", 
	Name: "Last Name, First name MI", 
	Position: "position of individual in context of an organization", 
	IndividualInfo: [ _linkTemplate ]  //0..N 
};

_organizationTemplate = { 
	OrgURI: "organizationURI", 
	Name: ["organization name"],  //0..N
	Info: [_linkTemplate]   //0..N; one of these should be for an icon to represent the organization
};

_extentTemplate: {
	ExtentLabel:"string to label this extent in UI",
	ExtentURI: "URI", //give extent an identity, could create a catalog of extents",
	ExtentReference: _referenceTemplate, //extent could be associated by reference, but only useful in a system that could follow links to access the actual geometry.
	BoundingBoxWGS84: {
         NorthBound: 45.0,
         SouthBound: 30.0,
         EastBound: -112.0,
         WestBound: -109.0
     },
	 Geometry:  {   //use GeoJSON encoding here...
		Type: "Polygon",
		Coordinates: [[
				[-180.0, 10.0], [20.0, 90.0], [180.0, -5.0], [-30.0, -90.0]
		]]
	}
	VerticalExtent: {
		VerticalMinimum: 200,
		VerticalMaximum: 400,
		VerticalCRS: _referenceTemplate
	 }
};

// used for situations that need a link to an online resource, typically for navigating linked data space. 
_linkTemplate = {
     URL: "http://fake.server.com/path/to/your/resource?complete=with&any=parameters",
	 Relation: "Term from IANA rel vocabulary for consistency with IETF5988.",
	 Title: "text to label this link in a UI",
     MIMEType: "string from IANA registry  http://www.iana.org/assignments/media-types/application/index.html",
	 Function: [_controlledConceptTemplate ],  //0..N
	 BaseProtocol: "string from IETF protocol registry at http://www.rfc-editor.org/rfcxx00.html",
	 ServiceType: _referenceTemplate,  //exactly 1. URI for identification, links to get documentation for service type
	 ResponseSchema: "URI that specifies the content type (consistent with MIME type), e.g.an XML schema namespace URI", //0..1  Provide separate link element for links producing different output formats.
	 AltTitle: [{
		AltTitleText: "string to display",
		AltTitleLanguage:  "ISO three letter language code" 
		}] ,  //0..N
	Description: "free text description of the target to help UI",
	Length: "advisory length of the linked content in octets",
	HrefLanguage:  "ISO three letter language code for language of target resource content",
	LinkModifier: [ _controlledConceptTemplate ] //term (controlled concept? URI?) that characterize the link or expected behavior, analogous to xlink:actuate. Some compiled terms include noFollow, new, replace, embed, onLoad, onRequest, noReferrer, prefetch //0..N
};

// use when another external linked data resource is intended to be the value of some element. 
// The URI is proxy for that resource, such that text-based identifier comparison can be used when convienent. 
// The associated links are for advertising specific representations or related resources. 
// Some of these are likely to be accessible by dereferncing the URI, but the link elements allow explicit indication of the available representations and how to get them (with no URI redirection...)
_referenceTemplate = {
     URI: "identifier for referenced resource",
     Links: [ _linkTemplate ] //0..N. Links to representation of some referenced resource
};

_eventDateTemplate = {
	EventType: [ _controlledConceptTemplate ], //0..N  event may be categorized in various ways...
	Date: "Please use a format like this: 2011-10-11T14:30"  //exactly 1
};

_valueDomainTemplate = { //choice of one of the following elements:
	NumericDomain: {
		LowerBound: 0,
		UpperBound: 100
	},
	ControlledVocabulary: _referenceTemplate, //attribute value is restricted to terms from a vocabulary (pick list)
	TargetEntity: _referenceTemplate, //if attribute value is link to another entity. The URI identifies an entity type definition, and the reference links should enable access to the linked resource in a specific instance.
	StringLength: 50 //if datatype is text, max lenght of text string
};