
metadataSchema = {
	description : 'A metadata record has two sections, one with information for management of the metadata itself, and one that describes some individual resource. Each metadata record describes exactly 1 resource. The metadata record can be considered a representation of the resource, but it has an identity that is distinct from the identity of the described resource.  There may be more than one metadata record in the system describing a single resource; these should have distinct metadata lineages.
		specifications followed here-  JSON pointer--http: tools.ietf.org/html/rfc6901',
	$schema : 'http://json-schema.org/draft-04/schema#',
	id : 'http://resources.usgin.org/uri-gin/usgin/schema/json',
	metadataRecord : {
		id : '#metadataRecord',
		type : 'object',
		properties : {
			MetadataInfo : {
				description : 'information about the metadata record',
				$ref : '#/metadataRecordInfo'
			},
			DescribedResource : {
				description : 'exactly 1. what the metadata record is about',
				$ref : '#/resourceDescription'
			}
		},
		required : ['MetadataInfo', 'DescribedResource']
	},

	metadataRecordInfo : {
		id : '#metadataRecordInfo',
		type : 'object',
		description : 'these are data items for managing the metadata record as a resource.'
		properties : {
			MDRecordURI : {
				type : 'string',
				format : 'uri'
			},
			MDUpdateDate : {
				type : 'string',
				format : 'date-time',
				description : 'exactly 1. This is time stamp for most recent change to metadata content in this record. Update history should be in Maintenance section; this is a convienence property'
			},
			MDSpecification : {
				description : 'Identifies the specification & profile for interpreting this document',
				$ref : '#/definitions/referenceTemplate'
			},
			.
			MDMaintenance : {
				$ref : '#/maintenance'
			},
			MDLanguage : {
				type : 'string',
				format : 'ISO three letter language code'
				pattern : '/[a-zA-Z]{3}/',
				description : 'exactly 0..1 default is eng if no value is specified.'
			},
			MDLineage : {
				$ref : '#/lineage'
			}
		},
		required : ['MDRecordURI', 'MDUpdateDate', 'MDSpecification', 'MDLanguage']
	},
	resourceDescription : {
		id : '#resourceDescription',
		type : 'object',
		description : 'basic metadata that might apply to any resource',
		properties : {
			Title : {
				type : 'string'
			},
			Description : {
				type : 'string'
			},
			Originator : {
				type : 'array',
				items : {
					$ref : '#/definitions/party'
				}
			},
			OriginDate : {
				description : 'Each date should scope a different origin event',
				type : 'array',
				items : {
					$ref : '#/definitions/eventDate'
				}
			},
			ResourceURI : {
				type : 'string',
				format : 'URI'
			},
			AlternateTitles : {
				type : 'array',
				items : {
					AltTitle : {
						type : 'object',
						properties : {
							AltTitleText : {
								type : 'string'
							},
							AltTitleLanguage : {
								type : 'string',
								format : 'ISO three letter language code'
							}
						}
					}
				}
			},
			SpatialExtent : {
				description : 'allow multiple bounding box extents for non contiguous resource, e.g. map of US coasts.',
				type : 'array',
				items : {
					$ref : '#/definitions/extent'
				}
			},
			TemporalScope : {
				description : '0..N  scope using named time ordinal eras (e.g. geologic time) should be specified using temporal keywords (vocabulary is a time scale)',
				type : 'array',
				items : {
					timeInterval : {
						type : 'object',
						properties : {
							begin : {
								$ref : '#/definitions/eventDate'
							},
							end : {
								$ref : '#/definitions/eventDate'
							}
						},
						required : ['begin']
					}
				}
			},
			ResourceType : {
				type : 'array',
				items : {
					$ref : '#/definitions/controlledConcept'
				},
				description : '0..N.  ResourceType is a specially recognized keywordTheme that categorizes the resource; at least one type category should be specified, as the type will guide processing of other parts of the metadata record. Resource categorization can be done on many axes. Some example schemes include  Functional Requirements for Bibliographic Records (FRBR) entity, which include _work_,_expression_,_manifestation_, and _item_ (see http: en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records#FRBR_Entities), frbr form here as well (e.g. e.g., novel, play, poem, essay, biography, symphony, concerto, sonata, map, drawing, painting, photograph, etc.), ISO scopeCodes that type resources. The different category schmes can be disambiguated by their VocabularyURI values, but concepts in each should have URIs that are sufficient.'
			},
			Tags : {
				description : '0..N  free form keywords',
				type : 'array',
				items : {
					tag : {
						type : 'string'
					}
				}
			},
			KeywordGroup : {
				type : 'object',
				properties : {
					KeywordTheme : {
						description : 'typical themes might include place, temporal, thematic, ISO topic category etc...',
						type : {
							$ref : '#/definitions/controlledConcept'
						}
					},
					Keywords : {
						type : 'array',
						items : {
							$ref : '#/definitions/controlledConcept'
						}
					}
				}
			},
			ResourceLanguage : {
				type : 'string',
				format : 'ISO three letter language code'
			},
			Distribution : {
				type : 'array',
				items : {
					Distributor : {
						type : {
							$ref : '#/definitions/party'
						}
					},
					OnlineAccess : {
						type : 'array',
						items : {
							$ref : '#/definitions/link'
						}
					}, //format information is included in link elements for online resources
					OfflineAccess : {
						properties : {
							AccessInformation : {
								type : 'string',
								description : 'free text description of how to get resource; only necessary for offline access, otherwise link.description provides details. The links here will be to frbr:expression of the resource. Include turnaround time and business hours information here',
								distributionMedium : {
									properties : {
										MediumType : {
											type : {
												$ref : '#/definitions/controlledConcept'
											}
										},
										MediumFormat : {
											type : {
												$ref : '#/definitions/controlledConcept'
											}
										}
									},
									required : ['MediumType']
								},
								Fees : {
									type : 'string',
									description : 'text explanation of any payment required to access resource'
								}
							}
						}
					}
				}
			},
			RelatedResource : {
				type : 'array',
				items : {
					$ref : '#/definitions/reference'
				}
			}, //0..N.  browseGraphic is a related resource, many other possibilities here...
			Lineage : {
				type : {
					$ref : '#/lineage'
				}
			},
			Quality : {
				type : {
					$ref : '#/resourceQuality'
				}
			},
			UsageConstraint : {
				type : {
					$ref : '#/resourceUsageConstraint'
				}
			},
			ResourceMaintenance : {
				type : {
					$ref : '#/maintenanceTemplate',
					description : ' only one here, because particular maintainence events that update the resource should be recorded in the lineage. This element provides information on how often maintenance is expected to occur and who is doing the maintenance. The resource maintenance contact will be the point of contact for reporting issues with the resource content.'
				}
			},
			ResourceTypeDetails : {
				properties : {
					Publication : {
						type : {
							$ref : '#/publicationDetails'
						}
					},
					Dataset : {
						type : {
							$ref : '#/datasetDetails'
						}
					},
					Service : {
						type : {
							$ref : '#/serviceDetails'
						}
					},
					CoverageDataset : {
						type : {
							$ref : '#/coverageDetails'
						}
					},
					EarthImageCoverage : {
						type : {
							$ref : '#/earthImage'
						}
					},
					Software : {
						type : {
							$ref : '#/software'
						}
					}
				} //extension point-- other detail types might be added, e.g. _specimenTemplate, _bookTemplate, _physicalItemTemplate...
			}
		}
	},
	maintenanceTemplate : {
		id : '#maintenance',
		properties : {
			MaintenanceContact : {
				type : 'array',
				items : {
					$ref : '#/definitions/party'
				}
			},
			// 1..N minimum is contact info for metadata issue reporting */
			Note : {
				type : 'string',
				description : 'free text information about maintenance plans, workflow, process...'
			},
			Interval : {
				type : 'string',
				description : 'time interval between planned maintenance events e.g. 6 months'
			},
			Frequency : {
				type : {
					$ref : '#/definitions/controlledConcept'
				}
			}, //0..1
			Date : {
				type : 'array',
				items : {
					$ref : '#/definitions/eventDate'
				},
				description : '0..N if nothing changes, can time-stamp to indicate maintenance check points. If record is updated, a process step in metadataLineage should be added.'
			}
		}
	},
	lineageTemplate : {
		id : '#lineage',
		properties : {
			LineageStatement : {
				type : 'string',
				description : 'free text description of provenance of resource and processing steps in its production'
			},
			History : {
				type : 'array',
				items : {
					$ref : '#/processStep'
				}
			}
			//0..N
		}
	},
	processStepTemplate : {
		id : '#processStep',
		properties : {
			Label : {
				type : 'string',
				description : 'text to characterize,identify this step for user interface listing'
			},
			Party : {
				type : 'array',
				items : {
					$ref : '#/definitions/party'
				},
				description : '0..N parties responsible for processing step'
			},
			ProcessType : {
				type : 'array',
				items : {
					$ref : '#/definitions/controlledConcept'
				}
			}, //0..N
			ProcessDescription : {
				type : 'string'
			},
			SequenceNo : {
				type : 'integer',
				description : 'number each step to all putting them in order. Order of listing is not significant'
			},
			InputResource : {
				type : 'array',
				items : {
					$ref : '#/definitions/reference'
				}
			}, //0..N
			OutputResource : {
				type : 'array',
				items : {
					$ref : '#/definitions/reference'
				}
			}, //0..N
			Event : {
				type : 'array',
				items : {
					$ref : '#/definitions/eventDate'
				},
				description : 'allow array, may have beginning, end, intermediate times...'
			},
			Rationale : {
				type : 'string',
				description : 'discussion of why the process step was done'
			},
			ComputerProcessing : {
				properties : {
					Software : {
						type : {
							$ref : '#/definitions/reference'
						}
					},
					RunTimeParameters : {
						type : 'array',
						items : [
							ProcessParameterName : {
								type : 'string',
								description : 'name of parameter'
							},
							ProcessParameterValue : {
								type : 'string',
								description : 'parameter value'
							}
						]//0..N
					}
				}
			},
			ProcessExtent : {
				type : 'array',
				items : {
					$ref : '#/definitions/extent'
				},
				description : '0..N  scope process to a particular geographic location/locations'
			},
			ProcessedElements : {
				type : 'array',
				items : {
					type : 'string'
				},
				description : '0..N, URIs for dataset, entity, attribute instances affected by this process'
			}
		}
	},
	resourceQualityTemplate : {
		id : '#resourceQuality',
		description : 'ISO19157 quality model here...',
		type : 'object',
		properties : {
			QualityStatement : {
				type : 'string',
				description : 'free text assessment of resource quality, including quantitative and qualitative measures'
			},
			QualityScope : {
				properties : {
					ResultScopeLevel : {
						type : {
							$ref : 'controlledConcept'
						}
					},
					ResultExtent : {
						type : {
							$ref : 'extent'
						}
					},
					ResultScopeEnumeration : {
						type : 'array',
						items : {
							$ref : '#/definitions/reference'
						},
						description : 'list of references to items that the result applies to'
					}
				}
			},
			QualityReportElements : {
				type : 'array',
				description : 'each item in this list is a data quality element',
				items : [StandaloneReport : {
						type : {
							$ref : '#/definitions/reference'
						},
						description : 'URI for a group of elements that might be extracted as a stand alone object'
					},
					ElementType : {
						type : {
							$ref : '#/definitions/controlledConcept'
						}
					},
					ElementConfidence : {
						type : 'string',
						description : 'general statement of confidence in this quality element assessment, guessing what the intention in 19157 is supposed to be'
					},
					ElementHomogeneity : {
						type : 'string',
						description : 'how uniformly this element value applies across the assigned result scope'
					},
					QualityMeasure : {
						properties : {
							MeasureType : {
								type : {
									$ref : '#/definitions/reference'
								}
							},
							MeasureLabel : {
								type : 'string',
								description : 'Text label for users to understand measure type'
							},
							MeasureDescription : {
								type : 'string',
								description : 'explanation of measureType'
							}
						}
					},
					QualityEvaluation : {
						properties : {
							EvaluationType : {
								type : {
									$ref : '#/definitions/reference'
								},
								description : 'links to reference docs for evaluation method should be in here'
							},
							EvaluationMethodDescription : {
								type : 'string',
								description : 'text description of the evaluation method'
							},
							EvaluationProcedure : {
								type : 'string',
								description : 'text description of procedure used to implement evaluation method'
							}
						}
					},
					QualityElementResult : {
						properties : {
							ResultScope : {
								properties : {
									ResultScopeLevel : {
										type : {
											$ref : '#/definitions/controlledConcept'
										}
									},
									ResultExtent : {
										type : {
											$ref : '#/definitions/extent'
										}
									},
									ResultScopeEnumeration : {
										type : 'array',
										items : {
											$ref : '#/definitions/reference'
										},
										description : 'list of references to items that the result applies to'
									}
								}
							},
							// one of the following three elements is required
							ResultValue : {
								oneof : [
									ConformanceResult : {
										properties : {
											ResultSpecification : {
												type : {
													$ref : '#/definitions/reference'
												}
											},
											ResultExplanation : {
												type : 'string',
												description : 'text explanation of result'
											},
											ConformancePass : {
												type : 'boolean'
											}
										}
									},
									ResultDescription : {
										type : 'string',
										description : 'text description of test result'
									},
									QuantitativeResult : {
										properties : {
											ResultValue : {
												type : 'string',
												description : 'value may be single number or a list of numbers or strings'
											},
											ResultValueUnits : {
												type : {
													$ref : '#/definitions/controlledConcept'
												}
											},
											ResultValueType : {
												type : {
													$ref : '#/definitions/controlledConcept'
												},
												description : 'if value is a record,link from concept URI should access a description of the record.'
											}
										}
									}
								]
							}
						}
					}
				]
			}
		}
	},
	resourceUsageConstraintTemplate : {
		id : '# resourceUsageConstraint',
		type : 'object',
		properties : {
			ConstraintsStatement : {
				type : 'string',
				description : 'free text description of legal or security related constraint on access oto or use of the described resource'
			},
			Constraints : {
				type : 'array',
				items : [
					ConstraintType : {
						type : {
							$ref : '#/definitions/controlledConcept'
						},
						description : 'e.g.security, access, usage'
					},
					ConstraintTerm : {
						type : {
							$ref : '#/definitions/controlledConcept'
						}
					}
				]
			} //0..N
		}
	},
	publicationDetailsTemplate : {
		id : '# publicationDetails',
		description : 'title, date, identifier are inherited from context.Publication details will only apply if the describe resource is an frbr:expression or frbr:item. Linkage to online items should still be through distribution linkage elements.If the resource is a work or manifestation,then expressions and items will be distributions of that resource. Tricky...',
		type : 'object',
		properties : {
			Edition : {
				type : 'string',
				description : 'identifier for edition'
			},
			EditionDate : {
				type : {
					$ref : '#/definitions/eventDate'
				}
			},
			SeriesTitle : {
				type : 'string'
			},
			SeriesIssue : {
				type : 'string',
				description : 'identifier for issue in series'
			},
			Page : {
				type : 'string'
			},
			PublicationDescription : {
				type : 'string',
				description : 'free text with other details specific to this particular manifestation of the resource.might add physicalDistribution elements here for library usage...'
			}
		}
	},
	datasetDetailsTemplate : {
		id : '# datasetDetails',
		type : 'object',
		properties : {
			DataSchema : {
				type : {
					$ref : '#/definitions/reference'
				},
				description : 'link to one or more resources describing the data schema'
			},
			DataSetEntites : {
				type : 'array',
				items : [
					EntityCount : {
						type : 'integer',
						description : 'number of instances of this entity in a particular dataset instance'
					},
					EntityDescription : {
						type : {
							$ref : '#/entity'
						}
					}
				]
			},
		}
	},
	entityTemplate : {
		id : '#entity',
		description : 'entity and attributes in the entity; ISO19110, ISO11179, FGDC entity - attribute information.Construct here describes concrete entities only.',
		type : 'object',
		properties : {
			EntityURI : {
				type : 'string',
				format : 'URI',
				description : 'allows this entity to be referenced externally'
			},
			EntityReference : {
				type : {
					$ref : '#/definitions/referenceTemplate'
				},
				description : 'an entity defintion my be include by reference to an external resource.If this is used, the rest of the elements in this object are not necessary and may be ignored in processing.'
			},
			EntityType : {
				type : {
					$ref : '#/definitions/controlledConcept'
				},
				description : 'feature dataset(collection of related geographic entities unified by spatial reference), relational table, object...'
			},
			EntityName : {
				type : 'string',
				description : 'name of feature class, table,or other entity manifestation'
			},
			AltEntityName : {
				type : 'array',
				items : [AltEntityNameText : {
						type : 'string'
					},
					AltEntityNameLanguage : {
						type : 'string',
						format : 'ISO three letter language code'
					}
				]
			},
			PartEntity : {
				type : 'array',
				items : {
					type : {
						$ref : '#/entity'
					}
				},
				description : 'compound entity like a feature dataset may have several included entities(lines and polys that have topological relationships)'
			},
			EntityAttribute : {
				properties : {
					LocalName : {
						type : 'string',
						description : 'name of attribute specific to context of this entity'
					},
					Cardinality : {
						type : 'string',
						enum : ['1', '0..1', '1..N', '0..N']
					},
					Attributes : {
						type : 'array',
						items : {
							type : {
								$ref : '#/attributeTemplate'
							}
						}
					},
					SpatialTopologyType : {
						$ref : _controlledConceptTemplate
					},
					GeometryType : {
						type : {
							$ref : 'controlledConcept'
						}
					},
					SpatialReferenceSystem : {
						type : {
							$ref : 'reference'
						}
					},
					Resolution : {
						properties : {
							ResolutionDenominator : {
								type : 'integer'
							}, //0..1
							ResolutionDistance : {
								properties : {
									ResolutionDistValue : {
										type : 'float'
									},
									ResolutionUOM : {
										type : {
											$ref : 'controlledConcept'
										}
									}
								}
							} //0..1
						}
					}
				}
			}
		}
	},
	attributeTemplate : {
		id : '#attribute',
		type : 'object',
		properties : {
			AttributeURI : {
				type : 'string',
				format : 'URI',
				description : 'to allow reference to this attribute definition from other objects'
			},
			AttributeReference : {
				type : {
					$ref : '#/definitions/reference'
				},
				description : 'attribute definition may be by reference, in which case rest of elements in this object are unnecessary.'
			},
			PropertySpecified : {
				type : {
					$ref : '#/definitions/controlledConcept'
				}
			},
			ConceptualDimension : {
				type : {
					$ref : '#/definitions/controlledConcept'
				},
				description : '0..1 e.g.length, mass, concept, velocity.The value here will be related to the valid UOM for the value.'
			},
			DataType : {
				type : {
					$ref : '#/definitions/controlledConcept'
				},
				description : '0..1, integer, float, text, URI, reference...'
			},
			Domain : {
				type : {
					$ref : '#/definitions/valueDomain'
				}
			} //0..1
		}
	},
	serviceDetailsTemplate : {
		id : '#serviceDetails',
		description : 'for metadata describing a service, the distribution section should include links to service end point URLs that will provide the service - specific self description document, e.g.THREDDS catalog, OGC GetCapabilities, OpenSearchDescription, WSDL, WADL, etc. This detail section allows linking to datasets exposed by the service, generic description of the operations provided by the service, and any important bindings between datasets and operations.It is anticipated that in most cases, this information will be gleaned from the service self - description document.Links to datasets are useful for discovery of services exposing particular datasets(which may be unknown to the dataset originator or metadata record creator',
		type : 'object',
		properties : {
			ServiceType : {
				$ref : '#/definitions/reference'
			},
			CouplingType : {
				$ref : '#/definitions/controlledConcept'
			},
			Operations : {
				type : 'array',
				items : {
					$ref : '#/serviceOperation'
				}
			}, //0..N
			CoupledResources : {
				type : 'array',
				items : {
					coupledResource : {
						type : 'object',
						properties : {
							OperatesOn : {
								$ref : '#/definitions/reference'
							},
							CoupledOperation : {
								$ref : '#/serviceOperation'
							}
						},
						description : 'operations specified in this section should not be duplicated in Operations section unless they may also be invoked in a loosely coupled mode'
					}
				}
			}
		}
	},
	serviceOperationTemplate : {
		id : '#serviceOperation',
		type : 'object',
		properties : {
			OperationURI : {
				type : 'string',
				format : 'URI'
			},
			OperationType : {
				$ref : '#/definitions/controlledConcept'
			},
			description : 'operations can be categorized using standard vocabularies to assist search/discovery',
			InvocationName : {
				type : 'string',
				description : 'name used to invoke operation in the context of the service'
			},
			OperationDescription : {
				type : 'string',
				description : 'free text description of what operation does'
			},
			InvocationLink : {
				description : 'one or more links for invoking operation. Suggest convention that in the link, strings that begin with $ and have names matching the InvocationName or a ParameterName can be treated as template slots that indicate where the invocation name and parameters should be inserted in the invocation URL.'
				$ref : '#/definitions/link'
			},
			OperationParameter : {
				type : 'object',
				properties : {
					ParameterName : {
						type : 'string',
						description : 'name of parameter'
					},
					ParameterDescription : {
						type : 'string',
						description : 'description of how to use parameter'
					},
					ParameterDirection : {
						type : 'string',
						enum : ['in', 'out', 'in/out']
					},
					Cardinality : {
						type : 'string',
						enum : ['1', '0..1', '1..N', '0..N'],
						ParameterDataType : {
							$ref : '#/definitions/controlledConcept'
						}, //integer, float, text, URI, reference...
						ParameterDomain : {
							$ref : '#/definitions/valueDomainTemplate'
						}
					}
				} //0..N parameters for this operation instance
			}
		}
	},
	coverageDetailsTemplate : {
		id : '#coverageDetails',
		type : 'object',
		properties : {
			CoverageType : {
				$ref : '#/definitions/controlledConcept'
			},
			Portrayal : {
				$ref : '#/definitions/reference',
				description : 'link to visualization of coverage, e.g. a browse graphic.'
			},
			FeatureOfInterest : {
				description : 'feature that the grid describes/characterizes',
				$ref : '#/definitions/reference'
			},
			GridDescription : {
				type : 'string',
				description : 'text description of coverage gridding scheme'
			},
			NGridDimensions : {
				type : 'integer'
			},
			GridAxis : {
				type : 'array',
				items : {
					$ref : '#/gridAxis'
				},
				minItems : 1,
				description : '1..N one instance for each grid dimension'
			},
			GeoreferencingDescription : {
				type : 'string',
				description : 'text description of how coverage grid is or may be georeferenced'
			},
			GeoreferenceStatus : {
				description : 'Term to indicate the status of a coverage with respect to establishing georeferencing. Includes e.g. {georeferencable, georectified, georeferenced...}, for coverage that  could be georeferenced, coverage that is georectified such that grid points are regularly located in a geographic coordinate system, georefenced means that information is included with the coverage (e.g. file header or world file) that defines mapping between coverage grid and geographic location.',
				$ref : '#/definitions/controlledConcept'
			}
		}
	},
	gridAxisTemplate : {
		id : '#gridAxis',
		type : 'object',
		properties : {
			PointOrInterval : {
				$ref : '#/definitions/controlledConcept'
			},
			RegularOrIrregular : {
				$ref : '#/definitions/controlledConcept'
			},
			Spacing : {
				type : 'object',
				properties : {
					CellLength : {
						type : 'number'
					},
					CellUOM : {
						$ref : '#/definitions/controlledConcept'
					}
				}
			},
			Property : {
				$ref : '#/definitions/controlledConcept'
			},
			AxisDomain : {
				type : 'string',
				description : 'explanation of value domain for this axis'
			}
		}
	},
	earthImageTemplate : {
		id : '#earthImage',
		type : 'object',
		properties : {
			IlluminationElevationAngle : {
				type : 'number'
			},
			IlluminationAzimuthAngle : {
				type : 'number'
			},
			ImagingCondition : {
				$ref : '#/definitions/controlledConcept'
			},
			CloudCoverPercent : {
				type : 'number'
			},
			ProcessingLevel : {
				$ref : '#/controllecConcept'
			},
			CompressionGenerationQuantity : {
				type : 'number'
			},
			TriangulationIndicator : {
				type : 'boolean'
			},
			RadiometricCalibration : {
				$ref : '#/definitions/reference'
			},
			CameraCalibration : {
				$ref : '#/definitions/reference'
			},
			FilmDistortionInformation : {
				$ref : '#/definitions/reference'
			},
			LensDistortionInformation : {
				$ref : '#/definitions/reference'
			}
		}
	},
	softwareTemplate : {
		id : '#software',
		type : 'object',
		description : 'this should be considered a rough draft of what might be useful...',
		properties : {
			ApplicationScheme : {
				$ref : '#/definitions/reference'
			},
			OperatingSystem : {
				$ref : '#/definitions/controlledConcept'
			},
			HarwareRequirements : {
				type : 'string',
				description : 'text describing necessary hardware environment for software to execute'
			},
			Preconditions : {
				type : 'string',
				description : 'text description of input requirements and state necessary to start execution'
			}
		}
	},

	//**************************************************************
	// general purpose templates *************************************

	definitions : {
		controlledConceptTemplate : {
			id : '#controlledConcept',
			type : 'object',
			properties : {
				ConceptURI : {
					type : 'string',
					format : 'URI'
				},
				Label : {
					type : 'string',
					description : 'This should be in the language specified by metadataLanguage'
				},
				AltLabels : {
					type : 'array',
					items : {
						altLabel : {
							type : 'object',
							properties : {
								labelText : {
									type : 'string'
								},
								language : {
									type : 'string',
									format : 'ISO three letter language code'
								},
								locale : {
									type : 'string',
									description : 'text that defines a context for use of this label'
								}
							}
						}
					}
				},
				VocabularyURI : {
					type : 'string',
					format : 'URI'
				},
				ConceptLink : {
					type : 'array',
					items : {
						$ref : '#/definitions/link'
					},
					description : '0..N can provide various links to get related concepts, definitions, source, etc.'
				}
			}
		},
		partyTemplate : {
			id : '#party',
			type : 'object',
			properties : {
				Role : {
					$ref : '#/definitions/controlledConcept'
				},
				Agent : {
					type : 'object',
					properties : {
						Persons : {
							type : 'array',
							items : {
								$ref : '#/definitions/individual'
							}
						},
						Organization : {
							$ref : '#/definitions/organization'
						}
					}
				},
				ContactInformation : {
					type : 'object',
					properties : {
						PhoneNumbers : {
							type : 'array',
							description : 'e.g.office, reception, fax, cel',
							items : {
								Phone : {
									type : 'object',
									properties : {
										PhType : {
											type : 'string'
										},
										number : {
											type : 'string'
										}
									}
								}
							}
						},
						Email : {
							type : 'string',
							format : 'email'
						},

						Address : {
							type : 'string',
							description : 'postal address,ideally formatted appropriate to the target country. One field because there is no clear reason to disaggregate the address into street, city, country, postal code, etc...'
						}
						Links : {
							type : 'array',
							itmes : {
								$ref : '#/definitions/link'
							}

						}
					}
				}
			}
		},
		individualTemplate : {
			id : '#individual',
			type : 'object',
			properties : {
				IndividualURI : {
					type : 'string',
					format : 'uri'
				},
				Name : {
					type : 'string',
					description : 'format--Last Name,First name MI'
				}
				Position : {
					type : 'string',
					description : 'position of individual in context of an organization'
				},
				IndividualInfo : {
					type : 'array',
					items : {
						$ref : '#/definitions/link'
					}
				}
			}
		},
		organizationTemplate : {
			id : '#organization',
			type : 'object',
			properties : {
				OrgURI : {
					type : 'string',
					format : 'uri'
				},
				Name : {
					type : 'array',
					items : {
						type : 'string'
					},
					minItems : 1
				},
				Info : {
					type : 'array',
					items : {
						$ref : '#/definitions/link'
					},
					description : 'one of these should be for an icon to represent the organization',
					minItems : 0
				}
			}
		},
		extentTemplate : {
			id : '#extent',
			type : 'object',
			properties : {
				ExtentLabel : {
					type : 'string',
					description : 'string to label this extent in UI'
				},
				ExtentURI : {
					type : 'string',
					description : 'give extent an identity, could create a catalog of extents'
					format : 'uri'
				},
				ExtentReference : {
					description : 'extent could be associated by reference, but only useful in a system that could follow links to access the actual geometry.',
					$ref : '#/definitions/reference'
				},
				BoundingBoxWGS84 : {
					type : 'object',
					properties : {
						NorthBound : {
							type : 'number',
							minimum : -90,
							maximum : 90
						},
						SouthBound : {
							type : 'number',
							minimum : -90,
							maximum : 90
						},
						EastBound : {
							type : 'number',
							minimum : -180,
							maximum : 180
						},
						WestBound : {
							type : 'number',
							minimum : -180,
							maximum : 180
						},
					}
				},
				Geometry : {
					description : 'use GeoJSON encoding. Schema by fge on Github',
					$ref : 'https://raw.githubusercontent.com/fge/sample-json-schemas/master/geojson/geojson.json'
				},
				VerticalExtent : {
					type : 'object',
					properties : {
						VerticalMinimum : {
							type : 'number'
						},
						VerticalMaximum : {
							type : 'number'
						},
						VerticalCRS : {
							$ref : '#/definitions/reference'
						}
					}
				}
			}
		},

		linkTemplate : {
			id : '#link',
			description : 'used for situations that need a link to an online resource, typically for navigating linked data space.',
			type : 'object',
			properties : {
				URL : {
					type : 'string',
					format : 'uri'
				},
				Relation : {
					type : 'string',
					description : 'Term from IANA rel vocabulary for consistency with IETF5988'
				},
				Title : {
					type : 'string',
					description : 'text to label this link in a UI'
				},
				MIMEType : {
					type : 'string',
					description : 'string from IANA registry http : //www.iana.org/assignments/media-types/application/index.html'
				},
				Function : {
					type : 'array',
					$ref : '#/definitions/controlledConcept'
				},
				BaseProtocol : {
					type : 'string',
					description : 'string from IETF protocol registry at http : //www.rfc-editor.org/rfcxx00.html'
				},
				ServiceType : {
					$ref : '#/definitions/reference',
					description : 'exactly 1. URI for identification, links to get documentation for service type'
				},
				ResponseSchema : {
					type : 'string',
					description : 'URI that specifies the content type(consistent with MIME type),.g.an XML schema namespace URI, //0..1  Provide separate link element for links producing different output formats.'
				},
				AltTitles : {
					type : 'array',
					items : {
						AltTitle : {
							type : 'object',
							properties : {
								AltTitleText : {
									type : 'string',
									description : 'string to display'
								},
								AltTitleLanguage : {
									type : 'string',
									format : 'ISO three letter language code',
									pattern : '/[a-zA-Z]{3}/'
								}
							}
						}
					}
				},
				Description : {
					type : 'string',
					description : 'free text description of the target to help UI'
				},
				Length : {
					type : 'integer',
					description : 'advisory length of the linked content in octets'
				},
				HrefLanguage : {
					type : 'string',
					format : 'ISO three letter language code',
					pattern : '/[a-zA-Z]{3}/',
					description : 'language of target resource content'
				},
				LinkModifier : {
					description : 'term (controlled concept or URI?) that characterize the link or expected behavior, analogous to xlink:actuate. Some compiled terms include noFollow, new, replace, embed, onLoad, onRequest, noReferrer, prefetch //0..N',
					$ref : '#/definitions/controlledConcept'
				}
			}
		},

		referenceTemplate : {
			id : '#reference',
			description : '// use when another external linked data resource is intended to be the value of some element. The URI is proxy for that resource, such that text-based identifier comparison can be used when convienent. The associated links are for advertising specific representations or related resources. Some of these are likely to be accessible by dereferncing the URI, but the link elements allow explicit indication of the available representations and how to get them (with no URI redirection...)',
			type : 'object'
			properties : {
				URI : {
					type : 'string',
					format : 'uri',
					description : 'identifier for referenced resource'
				},
				Links : {
					type : 'array',
					items : {
						$ref : _linkTemplate
					},
					description : 'Links to representation of some referenced resource'

				}
			}
		},
		eventDateTemplate : {
			id : '#eventDate',
			type : 'object',
			properties : {
				EventType : {
					type : 'array',
					items : {
						$ref : '#/definitions/controlledConcept'
					},
					description : '0..N  event may be categorized in various ways...'
				},
				Date : {
					type : 'string',
					format : 'date-time',
					description : 'Use ISO 8601: 2011-10-11T14:30'
				}
			}
		},
		valueDomainTemplate : {
			id : '#valueDomain',
			type : 'object',
			description : 'choice of one of the following elements:',
			oneOf : [{
					NumericDomain : {
						type : 'object',
						properties {
							LowerBound : {
								type : 'number'
							},
							UpperBound : {
								type : 'number'
							}
						}
					}
				}, {
					ControlledVocabulary : {
						$ref : '#/definitions/reference',
						description : 'attribute value is restricted to terms from a vocabulary (pick list)'
					}
				}, {
					TargetEntity : {
						$ref : '#/definitions/reference',
						description : 'if attribute value is link to another entity. The URI identifies an entity type definition, and the reference links should enable access to the linked resource in a specific instance.'
					}
				}, {
					StringLength : {
						type : 'integer',
						description : 'if datatype is text, max lenght of text string'
					}
				}
			]
		}
	}
}
