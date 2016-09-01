#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from dateutil.parser import parse

import logging

log = logging.getLogger(__name__)


# functions originally defined in harvested_metadata.py and  ckanext.spatial.
#  completely define the mapping usedfrom ckanext.spatial.model import ISOElement,
#  ISODocument, ISOResponsibleParty \
#    , ISOBoundingBox, ISOKeyword, ISOReferenceDate, ISOUsage \
#    , ISOAggregationInfo, ISOCoupledResources, ISODataFormat \
#    , ISOResourceLocator, ISOBrowseGraphic

# This defines an alternate ISODocument class, based on that defined in spatial\model\
#  harvested_metadata.py. this mapping of ISO content is used to construct the USGIN
#  extras.md_package ckanext-metadata/ckanext/harvest/usgin.py

# keys (element names) are based on USGINMetadataJSONSchemav3.0

class MappedXmlObject(object):

    elements = []


class MappedXmlElement(MappedXmlObject):

    namespaces = {}

    def __init__(
        self,
        name,
        search_paths=[],
        multiplicity='*',
        elements=[],
        ):

        self.name = name
        self.search_paths = search_paths
        self.multiplicity = multiplicity
        self.elements = elements or self.elements

    def read_value(self, tree):
        values = []
        for xpath in self.get_search_paths():
            if xpath == '':
                log.debug('hook for catching xpaths', self.name)
            if len(xpath) > 1:
                elements = self.get_elements(tree, xpath)

                # if self.get_values(elements):

                for val in self.get_values(elements):
                    values.append(val)

                    # original code only catches values on first xpath that has values;
                    # smr attempt to gather all values from search paths
                    # and then concatenate in fix_multiplicity if the property is supposed to be single valued
                    # if values:
                    #    break

        finalval = self.fix_multiplicity1(values)
        log.debug('read value: xpath %s, return value: %s',
                  self.get_search_paths(), finalval)
        return finalval

    def fix_multiplicity1(self, values):
        """
        When a field contains multiple values, concatenate values as strings.

        In the ISO19115 specification, multiplicity relates to:
        * 'Association Cardinality'
        * 'Obligation/Condition' & 'Maximum Occurence'
        """

        if self.multiplicity == '0':

            # 0 = None

            if values:
                log.warn("Values found for element '%s' when multiplicity should be 0: %s"
                         , self.name, values)
            return ''
        elif self.multiplicity == '-1':

        # smr add catch to flag elements that don't get processed
            # 0 = None

            if values:
                log.warn("Values found for element '%s' but these were not processed"
                         , self.name)
            return ''
        elif self.multiplicity == '1':

            # 1 = Mandatory, maximum 1 = Exactly one
            # if more than one item in values array, concatenate them

            if not values:
                log.warn("Value not found for mandatory element '%s'"
                         % self.name)
                return ''
            elif type(self) == USGINISOElement:
                if len(values) > 1 or type(values[0]) != str:
                    log.info('concatenate multiple string values for mandator element %s'
                             , self.name)
                    valueslist_str = ''
                    for item in values:
                        if type(item) == dict:
                            for key in item:
                                if len(item[key]) > 0:

                                    # thestr = thestr + key + ': '

                                    valueslist_str = valueslist_str \
    + '{' + item[key] + '}, '
                        elif type(item) == list:
                            valueslist_str = valueslist_str + '[' \
                                + ','.join(item) + '], '
                        else:
                            valueslist_str = valueslist_str + item \
                                + ', '
                    if len(values) > 1:
                        log.warn('Multiple values for cardinality 1 element, only the first kept %s'
                                 , self.name)
                    return valueslist_str
            return values[0]
        elif self.multiplicity == '*' or self.multiplicity == '0..*':

            # * = * = zero or more

            return values
        elif self.multiplicity == '0..1':

            # 0..1 = Mandatory, maximum 1 = optional (zero or one)

            if values:
                if type(self) == USGINISOElement:
                    if len(values) > 1 or type(values[0]) != str:
                        log.info('concatenate multiple string values for optional element %s'
                                 , self.name)
                        valueslist_str = ''
                        for item in values:
                            if type(item) == dict:
                                for key in item:
                                    if len(item[key]) > 0:

                                        # thestr = thestr + key + ': '

                                        valueslist_str = valueslist_str \
    + '{' + item[key] + '}, '
                            elif type(item) == list:
                                valueslist_str = valueslist_str + '[' \
                                    + ','.join(item) + '], '
                            else:
                                valueslist_str = valueslist_str + item \
                                    + ', '
                        if len(values) > 1:
                            log.debug('multiple values for cardinality 0..1 element %s'
                                    , self.name)
                        return valueslist_str
                return values[0]  # values exists, and is len(0) or not a USGINISOElemnt, which means in might have an
            else:

                # object for content

                return ''
        elif self.multiplicity == '1..*':

            # 1..* = one or more

            return values
        else:
            log.warning('Valid multiplicity not specified for element: %s'
                        , self.name)

        return values

    def get_search_paths(self):  # returns a list of search paths
        if type(self.search_paths) != type([]):
            search_paths = [self.search_paths]
        else:
            search_paths = self.search_paths
        return search_paths

    def get_elements(self, tree, xpath):
        log.debug(' get_elements %s', xpath)
        return tree.xpath(xpath, namespaces=self.namespaces)

    def get_values(self, elements):
        values = []
        if len(elements) == 0:
            pass
        else:
            for element in elements:
                value = self.get_value(element)

                # if type(value) == list:
                #     valueslist_str = '; '.join([str(mli) for mli in value])
                #     value = valueslist_str
                # if value:

                values.append(value)
        return values

    def get_value(self, element):
        if self.elements:
            value = {}
            for child in self.elements:
                value[child.name] = child.read_value(element)
            return value  # value is an object
        elif type(element) == etree._ElementStringResult:
            value = str(element)
        elif type(element) == etree._ElementUnicodeResult:
            value = unicode(element)
        else:
            value = self.element_tostring(element)
        return value

    def element_tostring(self, element):
        return etree.tostring(element, pretty_print=False)


class USGINISOElement(MappedXmlElement):

    # declare gml and gml3.2 because either one might show up in instances ...

    namespaces = {
        'gts': 'http://www.isotc211.org/2005/gts',
        'gml': 'http://www.opengis.net/gml',
        'gml32': 'http://www.opengis.net/gml/3.2',
        'gmx': 'http://www.isotc211.org/2005/gmx',
        'gsr': 'http://www.isotc211.org/2005/gsr',
        'gss': 'http://www.isotc211.org/2005/gss',
        'gco': 'http://www.isotc211.org/2005/gco',
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'srv': 'http://www.isotc211.org/2005/srv',
        'xlink': 'http://www.w3.org/1999/xlink',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }


class MappedXmlDocument(MappedXmlObject):

    def __init__(self, xml_str=None, xml_tree=None):
        assert xml_str or xml_tree is not None, \
            'Must provide some XML in one format or another'
        self.xml_str = xml_str
        self.xml_tree = xml_tree

    def read_keyvaluepairs(self):
        """
        For all of the elements listed, finds the values of them in the
        XML and returns them as a list of key-value pairs.values in the key-value
        pairs are other objects for nested content
        """

        keyvaluepairs = {}
        tree = self.get_xml_tree()

        for element in self.elements:
            log.debug(' read_keyvaluepairs %s', element.name)
            if 'personName' in element.name:
                log.debug('personName element')

            # pdb.set_trace()
            
            
            keyvaluepairs[element.name] = element.read_value(tree)
            
            #kludge for handling ISO records with no distributor
            if 'distributor' = element.name:
                if not kevaluepairs:
                    for altElement in self.elements
                        if altElement.name="distributionNoDistributor"
                            keyvaluepairs[element.name] = altElement.read_value(tree)
            

        self.infer_values(keyvaluepairs)
        return keyvaluepairs

    def read_value(self, name):
        '''For the given element name, find the value in the XML and return
        it.
        '''

        tree = self.get_xml_tree()
        for element in self.elements:
            if element.name == name:
                return element.read_value(tree)
        raise KeyError

    def get_xml_tree(self):
        if self.xml_tree is None:
            parser = etree.XMLParser(remove_blank_text=True)
            if type(self.xml_str) == unicode:
                xml_str = self.xml_str.encode('utf8')
            else:
                xml_str = self.xml_str
            log.debug(' get tree %s - %s ', parser, xml_str)
            self.xml_tree = etree.fromstring(xml_str, parser=parser)
        return self.xml_tree

    def infer_values(self, values):
        pass


# process CI_OnlineResource. Defines a subset of the USGIN
#   LinkObject properties

class USGINEventDate(USGINISOElement):
    #base element is gmd:CI_Date
    elements = [USGINControlledConcept(name='eventTypes',
                    search_paths=['gmd:dateType/gmd:CI_DateTypeCode'],
                    multiplicity='*'),
                USGINISOElement(name='eventDateTime',
                    search_paths=['gmd:date/gco:Date/text()',
                    'gmd:date/gco:DateTime/text()'], 
                            multiplicity='1')
               ]

# use for ISO code lists,
class USGINControlledConcept(USGINISOElement):

    elements = [USGINISOElement(name='conceptURI',
                search_paths=['@codelistValue'], multiplicity='1'),
                USGINISOElement(name='conceptPrefLabel',
                search_paths=['text()'], multiplicity='0..1'),
                USGINISOElement(name='conceptAltLabels',
                search_paths=[], multiplicity='*'),
                USGINISOElement(name='vocabularyURI',
                search_paths=['@codeList'], multiplicity='0..1'),
                USGINISOElement(name='conceptLinks', search_paths=[],
                multiplicity='*')]


# implements USGIN JSON metdata reference object--
# expected root elment is a property with a value that is either gmd:MD_Identifier or
# gmd:CI_Citation

class USGINAgent(USGINISOElement):

    # this class is for a contact--person or org, with contact info, but no role
    # context is CI_ResponsibleParty
    # implments a subset of the USGIN JSON metadata AgentObject

    elements = [  
        USGINISOElement(name='personName',
                        search_paths=['gmd:individualName/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='organizationNames',
                        search_paths=['gmd:organisationName/gco:CharacterString/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='personPosition',
                        search_paths=['gmd:positionName/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINAccessLink(name='agentLinks',
                           search_paths=['gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource'
                           ], multiplicity='*'),
        USGINISOElement(name='phoneContacts',
                        search_paths=['//gmd:voice','//gmd:facsimile'], 
                        multiplicity='*'
                       elements=[
                            USGINISOElement(name='phoneNumber',
                                search_paths=['gco:CharacterString/text()'], 
                                multiplicity='1'),
                            USGINISOElement(name='phoneService',
                                search_paths=['local-name(.)'], 
                                    multiplicity='0..1'),
                        ]
                    ),
        USGINISOElement(name='contactEmails',
                        search_paths=['gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString/text()'], 
                        multiplicity='*'),
        ISOPostalAddress(name='agentPostalAddress',
                        search_paths=['gmd:contactInfo/gmd:CI_Contact'], 
                         multiplicity='0..1'),
        ]


class USGINContact(USGINISOElement):

    # this class represents an Agent (contact, party) in a specific role
    # implemented the contactRef object in USGIN JSON metadata
    # context is the role name that has CI_ResponsibleParty as the role filler type

    elements = [
        USGINControlledConcept(name='agentRole',
                search_paths=['gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'
                ], multiplicity='1'), 
        USGINISOElement(name='agentHref',
                search_paths=['@xlink:href'], multiplicity='0..1'),
        USGINAgent(name='agent',
                search_paths=['gmd:CI_ResponsibleParty'],
                multiplicity='0..1')]  # catch any xlinks on the contact container property


# class for bibliographic citation

class ISOPostalAddress(USGINISOElement):

    elements = [
        USGINISOElement(name='delivery-point',
                search_paths=['gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString/text()'
                ], multiplicity='0..1'), 
        USGINISOElement(name='city',
                search_paths=['gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString/text()'
                ], multiplicity='0..1'),
        USGINISOElement(name='administrative-area',
                search_paths=['gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString/text()'
                ], multiplicity='0..1'),
        USGINISOElement(name='postal-code',
                search_paths=['gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString/text()'
                ], multiplicity='0..1'), 
        USGINISOElement(name='country',
                search_paths=['gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString/text()'
                ], multiplicity='0..1')]  # delivery-point


                                          # city
                                          # administrative area
                                          # postal code
                                          # country

# parse from CI_Contact

class ISOContactInfo(USGINISOElement):

    elements = [USGINISOElement(name='contactEmails',
                search_paths=['gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString/text()'
                ], multiplicity='*'),
                USGINISOElement(name='telephone-voice',
                search_paths=['gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString/text()'
                ], multiplicity='*'),
                ISOPostalAddress(name='postal-address',
                search_paths=['gmd:address/gmd:CI_Address'],
                multiplicity='0..1'),
                USGINAccessLink(name='contact-link',
                search_paths=['gmd:onlineResource/gmd:CI_OnlineResource'
                ], multiplicity='0..1')]  # email


                                          # modified to account for multiple e-mails
                                          # SMR addition
                                          # ignore facsimile numbers...
                                          # Telephone Voice
                                          # Modified to allow multiple phone number...
                                          # end smr addition
                                          # contact onlineResource (link)


    # handle MD_Format

class USGINCitation(USGINISOElement):
    #base element is CI_Citation
    elements=[
                USGINISOElement(name='citationHref',
                    search_paths=['../@xlink:href'], 
                    multiplicity='0..1'),
                USGINISOElement(name='citationTitle',
                    search_paths=['gmd:title/gco:CharacterString/text()'], 
                    multiplicity='1'),
                USGINISOElement(name='citationIdentifiers', 
                    search_paths=[
                    'gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()',
                    'gmd:ISBN/gco:CharacterString/text()',
                    'gmd:ISSN/gco:CharacterString/text()'
                    ], 
                    multiplicity='*'),
                ISOResponsibleParty(name='citationResponsibleParties',
                    search_paths=['gmd:citedResponsibleParty'], 
                    multiplicity='*'),
                USGINEventDate(name='citationDates',
                   search_paths=['gmd:date/gmd:CI_Date'], 
                   multiplicity='1..*'),
                USGINISOElement(name='citationAlternateTitles',
                    search_paths=['gmd:alternateTitle/gco:CharacterString/text()'], 
                    multiplicity='*'),
                USGINISOElement(name='edition',
                    search_paths=['gmd:edition/gco:CharacterString/text()'],
                    multiplicity='0..1'),
                USGINISOElement(name='editionDate',
                    search_paths=['gmd:editionDate/gco:Date/text()',
                                 'gmd:editionDate/gco:DateTime/text()'],
                    multiplicity='0..1'),
                USGINISOElement(
                    name='seriesName',
                    search_paths=['gmd:series/gmd:CI_Series/gmd:name/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINISOElement(
                    name='seriesIssue',
                    search_paths=['gmd:series/gmd:CI_Series/gmd:issueIdentification/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINISOElement(
                    name='page',
                    search_paths=['gmd:series/gmd:CI_Series/gmd:page/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINISOElement(
                    name='publicationDescription',
                    search_paths=['gmd:otherCitationDetails/gco:CharacterString/text()', 
                                  'gmd:collectiveTitle/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINControlledConcept(
                    name='publicationPresentationForm',
                    search_paths=['gmd:presentationForm/gmd:CI_PresentationFormCode'
                        ], 
                    multiplicity='0..1'),
                    ]

    

class ISODataFormat(USGINISOElement):

    elements = [  # base element is MD_Format
                  # don't handle format distributor for now; message will get put in log.
        USGINISOElement(name='formatID', search_paths=['@id'],
                        multiplicity='0..1'),
        USGINISOElement(name='formatHref', search_paths=['../@xlink:href'],
                        multiplicity='0..1'),
        USGINISOElement(name='formatName',
                        search_paths=['gmd:name/gco:CharacterString/text()'
                        ], multiplicity='1'),
        USGINISOElement(name='formatVersion',
                        search_paths=['gmd:version/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='formatAmendmentNumber',
                        search_paths=['gmd:amendmentNumber/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='formatspecification',
                        search_paths=['gmd:specification/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='formatDecompressionTechnique',
                        search_paths=['gmd:fileDecompressionTechnique/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='notHandledformatDistributor',
                        search_paths=['gmd:formatDistributor'],
                        multiplicity='-1'),
        ]


# handles srv:SV_CoupledREsource/resource

class ISOCoupledResources(USGINISOElement):

    # assumes that operatesOn is implemented as an xlink href. should log a warning if there is an inline MD_DataIdentification
    # this appears to be junk; the apiso.xsd implementation of service metadata does not follow the UML in ISO19119.  Leave here for now, but isn't processed into USGIN JSON.

    elements = [USGINISOElement(name='title',
                search_paths=['@xlink:title'], multiplicity='0..1'),
                USGINISOElement(name='href', search_paths=['@xlink:href'
                ], multiplicity='0..1'), USGINISOElement(name='uuid',
                search_paths=['@uuidref'], multiplicity='0..1'),
                USGINISOElement(name='notHandledcoupledInlineDataIdentification'
                , search_paths=['MD_DataIdentification'],
                multiplicity='-1')]  # smr fix multiplicities


                                     # shouldn't have inline MD_DataIdenfication; multiplicity -1 will put warning in log

class GMLTimePeriod(USGINISOElement):

    elements = [
        USGINISOElement(name='timePeriodId',
                        search_paths=['@id'
                        ], multiplicity='0..1'),
        USGINISOElement(name='timePeriodDescription',
                        search_paths=['gml:description/text()',
                        'gml32:description/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='timePeriodBeginPosition',
                search_paths=['gml:begin/gml:TimeInstant/gml:timePosition/text()',
                'gml32:begin/gml32:TimeInstant/gml32:timePosition/text()', 
                              'gml:beginPosition/text()'], 
                                multiplicity='0..1'),
        USGINISOElement(name='timePeriodEndPosition',
                search_paths=['gml:end/gml:TimeInstant/gml:timePosition/text()',
                'gml32:end/gml32:TimeInstant/gml32:timePosition/text()'
                , 'gml:endPosition/text()'], 
                                multiplicity='0..1')]


# base element is gmd:temporalElement so can catch hrefs.

class ISOTemporalExtent(USGINISOElement):

    elements = [  # topology time elements not handled
            # base is gmd:temporalElement property; value might be EX_TemporalExtent or EX_SpatialTemporalExtent
        #  also account for possible gml 3.0 or gml 3.2 namespaces
        USGINISOElement(name='timeFrameURI', 
                        search_paths=[
            'gmd:EX_TemporalExtent/gmd:extent/gml:TimeInstant/@frame',
            'gmd:EX_TemporalExtent/gmd:extent/gml32:TimeInstant/@frame',
            'gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/@frame',
            'gmd:EX_TemporalExtent/gmd:extent/gml32:TimePeriod/@frame',
            'gmd:EX_SpatialTemporalExtent/gmd:extent/gml:TimeInstant/@frame',
            'gmd:EX_SpatialTemporalExtent/gmd:extent/gml32:TimeInstant/@frame',
            'gmd:EX_SpatialTemporalExtent/gmd:extent/gml:TimePeriod/@frame',
            'gmd:EX_SpatialTemporalExtent/gmd:extent/gml32:TimePeriod/@frame',
            ], multiplicity='0..1'),
        USGINISOElement(name='timeInstant',
                        search_paths=['gmd:EX_TemporalExtent/gmd:extent/gml:TimeInstant',
                        'gmd:EX_TemporalExtent/gmd:extent/gml32:TimeInstant',
                        'gmd:EX_SpatialTemporalExtent/gmd:extent/gml:TimeInstant',
                        'gmd:EX_SpatialTemporalExtent/gmd:extent/gml32:TimeInstant)'
                        ], multiplicity='0..1',
            elements=[
                USGINISOElement(name='timeInstantId',
                        search_paths=['@id'
                        ], multiplicity='0..1'),
                USGINISOElement(name='timeInstantDescription',
                        search_paths=['gml:description/text()',
                        'gml32:description/text()'
                        ], multiplicity='0..1'),
                USGINISOElement(name='timeInstantTimePosition',
                        search_paths=['gml:timePosition/text()',
                        'gml32:timePosition/text()'
                        ], multiplicity='1'),
                ]
        ),
        GMLTimePeriod(name='timePeriod',
                      search_paths=['gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod',
                      'gmd:EX_TemporalExtent/gmd:extent/gml32:TimePeriod',
                      'gmd:EX_SpatialTemporalExtent/gmd:extent/gml:TimePeriod',
                      'gmd:EX_SpatialTemporalExtent/gmd:extent/gml32:TimePeriod'
                      ], multiplicity='0..1'),
        
        USGINISOElement(name='notHandledtimeEdge',
                        search_paths=['gmd:EX_TemporalExtent/gmd:extent/gml:TimeEdge',
                        'gmd:EX_TemporalExtent/gmd:extent/gml32:TimeEdge',
                        'gmd:EX_SpatialTemporalExtent/gmd:extent/gml:TimeEdge',
                        'gmd:EX_SpatialTemporalExtent/gmd:extent/gml32:TimeEdge'
                        ], multiplicity='-1'),
        USGINISOElement(name='notHandledtimeNode',
                        search_paths=['gmd:EX_TemporalExtent/gmd:extent/gml:TimeNode',
                        'gmd:EX_TemporalExtent/gmd:extent/gml32:TimeNode',
                        'gmd:EX_SpatialTemporalExtent/gmd:extent/gml:TimeNode',
                        'gmd:EX_SpatialTemporalExtent/gmd:extent/gml32:TimeNode'
                        ], multiplicity='-1'),
        USGINISOElement(name='temporalExtentReference',
            search_paths=['@xlink:href'],
            multiplicity='0..1',
            elements=[
                USGINISOElement(
                    name='referenceURIs',
                    search_paths=['.'],
                    multiplicity='*'),  #multiplicity forces implementation as array
                USGINISOElement(
                    name='referenceLabel',
                    search_paths=['../@xlink:title'],
                    multiplicity='0..1'),
            ]
        )
        ]

# MD_BrowseGraphic

class ISOBrowseGraphic(USGINISOElement):

    elements = [USGINISOElement(name='browseGraphicName',
                search_paths=['gmd:fileName/gco:CharacterString/text()'
                ], multiplicity='1'),
                USGINISOElement(name='browseGraphicDescription',
                search_paths=['gmd:fileDescription/gco:CharacterString/text()'
                ], multiplicity='0..1'),
                USGINISOElement(name='browseGraphicResourceType',
                search_paths=['gmd:fileType/gco:CharacterString/text()'
                ], multiplicity='0..1')]


# MD_Keywords   maps to USGIN JSON resourceIndexTerms

class ISOKeywords(USGINISOElement):

    elements = [  # smr add typeCode codelist
                  # smr add thesaurus information
        USGINISOElement(name='keywords',
                        search_paths=['gmd:keyword/gco:CharacterString/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='keywordTypeURI',
                        search_paths=['gmd:type/gmd:MD_KeywordTypeCode/@codeListValue'
                        ], multiplicity='0..1'),
        USGINISOElement(name='keywordTypeLabel',
                        search_paths=['gmd:type/gmd:MD_KeywordTypeCode/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='keywordTypeVocabularyURI',
                        search_paths=['gmd:type/gmd:MD_KeywordTypeCode/@codeList'
                        ], multiplicity='0..1'),
        USGINISOElement(name='keywordReferenceTitle',
                        search_paths=['gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='keywordReferenceIdentifier',
                        search_paths=['gmd:thesaurusName/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        ]


        # end thesaurus information

        # If more Thesaurus information is needed at some point, this is the
        # place to add it

# MD_Usage

class ISOUsage(USGINISOElement):

    elements = [USGINISOElement(name='specificUsage',
                search_paths=['gmd:specificUsage/gco:CharacterString/text()'
                ], multiplicity='0..1'),
                ISOResponsibleParty(name='specificUsageUserContact',
                search_paths=['gmd:userContactInfo'],
                multiplicity='0..1'),
                USGINISOElement(name='specificUsageLimitations',
                search_paths=['gmd:userDeterminedLimitations/gco:CharacterString/text()'
                ], multiplicity='0..1'),
                USGINISOElement(name='specificUsageDateTime',
                search_paths=['gmd:usageDateTime/gco:DateTime/text()'],
                multiplicity='0..1')]  # smr add usageDateTime and  limitations


# MD_AggregationInfo

class ISOAggregationInfo(USGINISOElement):

    elements = [
        USGINISOElement(name='relatedResourceLabel',
                        search_paths=['gmd:aggregateDatasetName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='relatedResourceIdentifier',
                        search_paths=['gmd:aggregateDatasetIdentifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'
                        ,
                        'gmd:aggregateDatasetName/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='relationTypeLabel',
                        search_paths=['gmd:associationType/gmd:DS_AssociationTypeCode/text()'
                        ,
                        'gmd:associationType/gmd:DS_AssociationTypeCode/@codeListValue'
                        ], multiplicity='0..1'),
        USGINISOElement(name='relationTypeConceptURI',
                        search_paths=['gmd:associationType/gmd:DS_AssociationTypeCode/@codeListValue'
                        ], multiplicity='1'),
        USGINISOElement(name='relationTypeVocabularyURI',
                        search_paths=['gmd:associationType/gmd:DS_AssociationTypeCode/@codeList'
                        ], multiplicity='0..1'),
        USGINISOElement(name='relatedInitiativeTypeConceptURI',
                        search_paths=['gmd:initiativeType/gmd:DS_InitiativeTypeCode/@codeListValue'
                        ], multiplicity='0..1'),
        USGINISOElement(name='relatedInitiativeLabel',
                        search_paths=['gmd:initiativeType/gmd:DS_InitiativeTypeCode/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='relatedInitiativeTypeVocabularyURI',
                        search_paths=['gmd:initiativeType/gmd:DS_InitiativeTypeCode/@codeList'
                        ], multiplicity='0..1'),
        ]


# smr MD_DigitalTransferOptions
# in order to associate formats with links,
#  USGIN JSON groups transferOptions on Distributor,

class USGINAccessLink(USGINISOElement):
    #base element is gmd:CI_OnlineResource
        elements=[
            USGINISOElement(name='linkURL',
                            search_paths=['gmd:linkage/gmd:URL/text()'
                            ], multiplicity='1'),
            USGINISOElement(name='linkRelations',
                            search_paths=['gmd:function/gmd:CI_OnLineFunctionCode'
                            ], 
                            multiplicity='*',
                            elements=[
                                USGINISOElement(name='relURI',
                                        search_paths=['@codeListValue'], 
                                        multiplicity='0..1'),
                                USGINISOElement(name='relLabel',
                                                search_paths=['text()'], 
                                                multiplicity='0..1'),
                                USGINISOElement(name='relVocabularyURI',
                                                search_paths=['@codeList'], 
                                                multiplicity='0..1')
                                ]
                            ),
            USGINISOElement(name='linkTitle',
                            search_paths=['gmd:name/gco:CharacterString/text()'
                            ], multiplicity='0..1'),
            ISODataFormat(name="linkTargetResourceTypes",
                           search_paths="../../../../gmd:distributionFormat/gmd:MD_Format",
                           multiplicity="*"),
            USGINISOElement(name='linkOverlayAPI',
                            search_paths=['gmd:protocol/gco:CharacterString/text()'
                            ], multiplicity='0..1'),
            USGINISOElement(name='linkDescription',
                            search_paths=['gmd:description/gco:CharacterString/text()'
                            ], multiplicity='0..1'),
            USGINISOElement(name='linkTransferSize',
                            search_paths=['../gmd:transferSize/gco:Real/text()'
                            ], multiplicity='0..1'),
            ]

# MD_StandardOrderProcess
class ISODistributor(USGINISOElement):

    elements = [
        USGINISOElement(name='distributorID',
                search_paths=['@id'], multiplicity='0..1'),
        ISOResponsibleParty(name='distributorContact',
            search_paths=['gmd:distributorContact'],
            multiplicity='1'),
        USGINISOElement(name='distributorFormats',
            search_paths=['gmd:distributorFormat'], multiplicity='*', 
            elements=[
                USGINISOElement(name='theFormatHref',
                    search_paths=['@xlink:href'], multiplicity='0..1'),
                ISODataFormat(name='theFormat',
                    search_paths=['gmd:MD_Format'], multiplicity='0..1')]
            ),
        USGINISOElement(name='distributorTransferOptions',
            search_paths=['gmd:distributorTransferOptions'],
            multiplicity='*',
            elements=[
                USGINISOElement(name='transferOptionHref',
                        search_paths=['@xlink:href'], multiplicity='0..1'),
                ISOTransferOptions(name='digitalTransferOptions',
                        search_paths=['gmd:MD_DigitalTransferOptions'],
                        multiplicity='0..1')]
            ),
        ISOOrderProcess(name='distributorAccessInstructions',
                search_paths=['gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess'
                ], multiplicity='*')
    ]


# MD_Constraints, used for metadatConstraints and resourceConstraints

class ISOConstraints(USGINISOElement):

    elements = [
        USGINISOElement(name='useLimitation',
                        search_paths=['gmd:MD_Constraints/gmd:useLimitation/gco:CharacterString/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='legalUseLimitation',
                        search_paths=['gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='legalOtherRestrictionConstraints',
                        search_paths=['gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='legalAccessRestrictionCode',
                        search_paths=['gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/@codeListValue'
                        ,
                        'gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='legalUseRestrictionCode',
                        search_paths=['gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode/@codeListValue'
                        ,
                        'gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='securityUseLimitation',
                        search_paths=['gmd:MD_SecurityConstraints/gmd:useLimitation/gco:CharacterString/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='securityClassificationCode',
                        search_paths=['gmd:MD_SecurityConstraints/gmd:classification/gmd:ClassificationCode/@codeListValue'
                        ,
                        'gmd:MD_SecurityConstraints/gmd:classification/gmd:ClassificationCode/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='securityUserNote',
                        search_paths=['gmd:MD_SecurityConstraints/gmd:userNote/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='securityClassificationSystem',
                        search_paths=['gmd:MD_SecurityConstraints/gmd:classificationSystem/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='securityHandlingDescription',
                        search_paths=['gmd:MD_SecurityConstraints/gmd:handlingDescription/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='constraintRestrictionCodelist',
                        search_paths=['gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/@codeList'
                        ,
                        'gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode/@codeList'
                        ,
                        'gmd:MD_SecurityConstraints/gmd:classification/gmd:ClassificationCode/@codeList'
                        ], multiplicity='*'),
        ]


# gmd:MD_MaintenanceInformation

class ISOMaintenance(USGINISOElement):

    elements = [  # updateFrequency
                  # maintenanceNote; concatenate all the other stuff;
                  # updateScopeDescription is a collection of attributesinstance, datasets, other, not clear what
                  # might show up there; hopefully it gets converted to some kind of usable text...
        USGINISOElement(name='maintenanceFrequencyURI',
                        search_paths=['gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/@codeListValue'
                        ], multiplicity='1'),
        USGINISOElement(name='maintenanceFrequencyText',
                        search_paths=['gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='maintenanceFrequencyVocabularyURI',
                        search_paths=['gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/@codeList'
                        ], multiplicity='0..1'),
        USGINISOElement(name='dateNextUpdate',
                        search_paths=['gmd:dateOfNextUpdate/gco:Date',
                        'gmd:dateOfNextUpdate/gco:DateTime'],
                        multiplicity='0..1'),
        USGINISOElement(name='maintenanceInterval',
                        search_paths=['gmd:userDefinedMaintenanceFrequencey/gts:TM_PeriodDuration'
                        ], multiplicity='0..1'),
        USGINISOElement(name='MaintenanceNote',
            search_paths=['gmd:maintenanceNote/gco:CharacterString/text()',
            'gmd:updateScope/gmd:MD_ScopeCode/@codeListValue',
            'gmd:updateScopeDescription/gmd:MD_ScopeDescription/text()'
            ], 
            multiplicity='0..1'),
        ISOResponsibleParty(name='maintenanceContacts',
                            search_paths=['gmd:contact'],
                            multiplicity='*'),
        ]


# gmd:MD_Distribution. Has three parts, distributor, transferOptions, and Format;
#   each of the last two may be nested inside a distributor element as well.
#   USGIN processing refactors so if there are multiple distributions, they are all nested inside
#   a distributor;

class ISODistributionNoDistributor(USGINISOElement):
    #base element is MD_Distribution
    elements = [
        USGINISOElement(name='distributor', 
                search_paths=['gmd:distributor'], 
                multiplicity='0..1', 
                elements=[
                    USGINISOElement(name='agentHref',
                        search_paths=['@xlink:href'], multiplicity='0..1'), 
                    ]
                ),
                #formats are attached to the online and offline distribution options
        USGINAccessLink(name='accessLinks', 
            search_paths=['gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:online/gmd:CI_OnlineResource'], 
            multiplicity='*', 
            ),
        USGINISOElement(name='unitsOfDistribution', 
            search_paths=['gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString/text()'], 
            multiplicity='0..1', 
            ),
        USGINISOElement(name='offlineAccess', 
                search_paths=['gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:offLine'], 
                multiplicity='0..1',
                elements=[
                     USGINControlledConcept(name='offlineMediumType', 
                            search_paths=['gmd:MD_Medium/gmd:mediumFormat/gmd:MD_MediumNameCode'], 
                            multiplicity='0..1', 
                        ),
                    USGINISOElement(name='offlineMediumFormats', 
                            search_paths=['gmd:MD_Medium/gmd:mediumFormat/gmd:MD_MediumFormatCode'], 
                            multiplicity='*', 
                        ),
                    ISODataFormat(name="offlineFileFormats",
                           search_paths="../../../../gmd:distributionFormat/gmd:MD_Format",
                           multiplicity="*"
                        ),
                    USGINISOElement(name='offlineMediumNote', 
                            search_paths=['gmd:MD_Medium/gmd:mediumNote/gco:CharacterString/text()'], 
                            multiplicity='0..1', 
                        ),
                    USGINISOElement(name='transferSize', 
                            search_paths=['../gmd:transferSize/gco:Real/text()'], 
                            multiplicity='0..1', 
                        ),
                    ]
                ),
    ]  

class USGINDistributorAccess(USGINISOElement):
    #base ISO path is gmd:MD_Distributor
    elements = [
        USGINISOElement(name='distributorHref',
                search_paths=['@xlink:href'], 
                multiplicity='0..1'),
        USGINContact(name='distributor', 
                search_paths=['gmd:distributorContact'], 
                multiplicity='0..1'),
                #formats are attached to the online and offline distribution options
        USGINAccessLink(name='accessLinks', 
            search_paths=['gmd:distributorTransferOptions/gmd:MD_DigitalTransferOptions/gmd:online/gmd:CI_OnlineResource',
                         '../../gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:online/gmd:CI_OnlineResource'], 
            multiplicity='*', 
            ),
        USGINISOElement(name='unitsOfDistribution', 
            search_paths=['gmd:distributorTransferOptions/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString/text()',
                         '../../gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString/text()'], 
            multiplicity='0..1', 
            ),
        USGINISOElement(name='accessInstructions',
                search_paths=['gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:orderingInstructions/gco:CharacterString/text()', 'gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:turnaround/gco:CharacterString/text()',            
                ], 
                multiplicity='0..1'),
        USGINISOElement(name='offlineAccess', 
                search_paths=['gmd:distributorTransferOptions/gmd:MD_DigitalTransferOptions/gmd:offLine',
                             '../../gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:offLine'], 
                multiplicity='0..1',
                elements=[
                     USGINControlledConcept(name='offlineMediumType', 
                            search_paths=['gmd:MD_Medium/gmd:mediumFormat/gmd:MD_MediumNameCode'], 
                            multiplicity='0..1', 
                        ),
                    USGINISOElement(name='offlineMediumFormats', 
                            search_paths=['gmd:MD_Medium/gmd:mediumFormat/gmd:MD_MediumFormatCode'], 
                            multiplicity='*', 
                        ),
                    ISODataFormat(name="offlineFileFormats",
                           search_paths="../../../../gmd:distributionFormat/gmd:MD_Format",
                           multiplicity="*"
                        ),
                    USGINISOElement(name='offlineMediumNote', 
                            search_paths=['gmd:MD_Medium/gmd:mediumNote/gco:CharacterString/text()'], 
                            multiplicity='0..1', 
                        ),
                    USGINISOElement(name='transferSize', 
                            search_paths=['../gmd:transferSize/gco:Real/text()'], 
                            multiplicity='0..1', 
                        ),
                    ]
                ),
    
        USGINISOElement(name='fees',
                search_paths=['gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:fees/gco:CharacterString/text()'],
                multiplicity='0..1'),
        USGINISOElement(name='availableDateTimes',
                search_paths=['gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:plannedAvailableDateTime/gco:DateTime/text()'
                ], multiplicity='*'),
    ]  
    

class USGINDistributor(USGINISOElement):

    elements = [
        USGINISOElement(name='distributorID',
                search_paths=['@id'], multiplicity='0..1'),
        ISOResponsibleParty(name='distributorContact',
            search_paths=['gmd:distributorContact'],
            multiplicity='1'),
        USGINISOElement(name='distributorFormats',
            search_paths=['gmd:distributorFormat'], multiplicity='*', 
            elements=[
                USGINISOElement(name='theFormatHref',
                    search_paths=['@xlink:href'], multiplicity='0..1'),
                ISODataFormat(name='theFormat',
                    search_paths=['gmd:MD_Format'], multiplicity='0..1')]
            ),
        USGINISOElement(name='distributorTransferOptions',
            search_paths=['gmd:distributorTransferOptions'],
            multiplicity='*',
            elements=[
                USGINISOElement(name='transferOptionHref',
                        search_paths=['@xlink:href'], multiplicity='0..1'),
                ISOTransferOptions(name='digitalTransferOptions',
                        search_paths=['gmd:MD_DigitalTransferOptions'],
                        multiplicity='0..1')]
            ),
        ISOOrderProcess(name='distributorAccessInstructions',
                search_paths=['gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess'
                ], multiplicity='*')
    ]


# MD_Constraints, used for metadatConstraints and resourceConstraints

class ISOSpatialExtent(USGINISOElement):

    """
    root is EX_Extent
    """

    elements = [  # extent, controlled-- move the geographicIdentifier values from extent-free-text to here...
                  #  don't have a handler for EX_BoundingPolygon... should throw warning if have one
                  # smr add time instant, for gml ns only; if is instant make extent-begin=extent-end..
                  # also that gml3.2 should be invalid with gmd...
                  # vertical extent has minimumValue and maximumValue properties. Have to check what this search_path actually does.
        USGINISOElement(name='extentDescription',
                        search_paths=['gmd:description/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='extentReference',
                        search_paths=['gmd:geographicElement/gmd:EX_GeographicDescription'
                        ], multiplicity='*',
                        elements=[USGINISOElement(name='extentTypeCode'
                        ,
                        search_paths=['gmd:extentTypeCode/gco:Boolean/text()'
                        ], multiplicity='0..1'),
                        USGINISOElement(name='extentReferenceCode',
                        search_paths=['gmd:geographicIdentifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='extentReferenceAuthorityTitle'
                        ,
                        search_paths=['gmd:geographicIdentifier/gmd:MD_Identifier/gmd:authority/gmd:CI_Citation/gmd:title/gco:CharacterString/text()'
                        ], multiplicity='0..1')]),
        USGINISOElement(name='notHandledExtentPolygonORSpatialTemporal'
                        ,
                        search_paths=['gmd:geographicElement/gmd:EX_BoundingPolygon'
                        ,
                        'gmd:temporalElement/gmd:EX_SpatialTemporalExtent'
                        ], multiplicity='-1'),
        USGINISOElement(name='boundingBoxesWGS84',
                        search_paths=['gmd:geographicElement/gmd:EX_GeographicBoundingBox'
                        ], multiplicity='*',
                        elements=[USGINISOElement(name='extentTypeCode'
                        ,
                        search_paths=['gmd:extentTypeCode/gco:Boolean/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='west',
                        search_paths=['gmd:westBoundLongitude/gco:Decimal/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='east',
                        search_paths=['gmd:eastBoundLongitude/gco:Decimal/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='north',
                        search_paths=['gmd:northBoundLatitude/gco:Decimal/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='south',
                        search_paths=['gmd:southBoundLatitude/gco:Decimal/text()'
                        ], multiplicity='1')]),
        USGINISOElement(name='verticalExtentElements',
                        search_paths=['gmd:verticalElement/gmd:EX_VerticalExtent'
                        ], multiplicity='*',
                        elements=[USGINISOElement(name='minVerticalValue'
                        ,
                        search_paths=['gmd:minimumValue/gco:Real/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='maxVerticalValue',
                        search_paths=['gmd:maximumValue/gco:Real/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='verticalCRShref',
                        search_paths=['gmd:verticalCRS/@xlink:href'],
                        multiplicity='1'),
                        USGINISOElement(name='verticalCRStitle',
                        search_paths=['gmd:verticalCRS/@xlink:title'],
                        multiplicity='0..1')]),
        ]


class ISOQualityElement(USGINISOElement):
    """
    root is DQ_Element, which has 15 concrete subtypes in ISO19115, all with same conent model
    this class handles the content. PUts ISO19157 quality type class name in qualityElementType.
    Soft type the eleiemtn type instead of hard type
    """
    elements = [
        USGINISOElement(name='qualityElementURI',
                search_paths=['../@xlink:href'
                ], multiplicity='1'),        
        USGINISOElement(name='qualityElementType',
            search_paths=['local-name(.)'], 
            multiplicity='1'),
        USGINISOElement(name='qualityMeasureIdentifier',
                search_paths=['gmd:measureIdentification/gmd:MD_Identifier'
                ], 
                multiplicity='0..1'
                elements=[
                    USGINISOElement(name='referenceLabel',
                        search_paths=['gmd:code/gco:CharacterString/text()'], 
                        multiplicity='0..1'),
                    USGINISOElement(name='referenceURIs',
                        search_paths=['gmd:authority/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'], 
                        multiplicity='*'),
                    USGINISOElement(name='citation',
                        search_paths=['gmd:authority/gmd:CI_Citation'], 
                        multiplicity='*', 
                        elements=[
                            USGINISOElement(name='citationTitle',
                                search_paths=['gmd:title/gco:CharacterString/text()'], 
                                multiplicity='0..1'),
                        ]
                                )
                ]
            ),
        USGINISOElement(name='qualityMeasureLabel',
                        search_paths=['gmd:nameOfMeasure/gco:CharacterString/text()',
                                      '../@xlink:title'],
                        multiplicity='0..1'),
        USGINISOElement(name='qualityElementMeasureDescription',
                        search_paths=['gmd:measureDescription/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINControlledConcept(name='qualityEvaluationType',
                       search_paths=['gmd:evaluationMethodType/gmd:DQ_EvaluationMethodTypeCode'
                       ], multiplicity='0..1'),
        USGINISOElement(name='qualityElementEvaluationMethodDescription',
                        search_paths=['gmd:evaluationMethodDescription/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name="qualityEvaluationProcedure",
                        search_paths=["gmd:evaluationMethodProcedure/gmd:CI_Citation/"],
                        multiplicity="0..1"
                        elements=[
                            USGINISOElement(name='citationTitle',
                                search_paths=['gmd:title/gco:CharacterString/text()'], 
                                multiplicity='0..1'),
                            USGINISOElement(name='citationIdentifiers',
                                search_paths=  ['gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'], 
                                multiplicity='*')
                                ]
                        ),
        USGINISOElement(name='qualityElementDateTime',
                        search_paths=['gmd:dateTime/gco:DateTime/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='qualityElementResults',
            search_paths=['gmd:result'], 
            multiplicity='1..*',
            elements=[
                            USGINISOElement(name='qualityQuantitativeResultValue'
                                , search_paths=['gmd:DQ_QuantitativeResult'],
                                multiplicity='0..1',
                                elements=[
                                    USGINISOElement(name='quantitativeResultValue', 
                                        search_paths=['gmd:value'],
                                        multiplicity='1..*'),
                                    USGINISOElement(name='quantitativeResultErrorStatistic', 
                                        search_paths=['gmd:value'],
                                        multiplicity='1..*'),
                                    USGINISOElement(name='quantitativeResultUnits',
                                        search_paths=['gmd:value'], 
                                        multiplicity='1..*'), 
                                    USGINISOElement(name='quantitativeResultType', 
                                        search_paths=['gmd:value'],
                                        multiplicity='1..*')
                                    ]
                                ),
                            USGINISOElement(name='qualityResultSpecificationTitle',
                                search_paths=['gmd:specification/gmd:CI_Citation/gmd:title/gco:CharacterString/text()'], 
                                multiplicity='0..1'),
                            USGINISOElement(name='qualityResult',
                                search_paths=['gmd:result'], 
                                multiplicity='1..*'), 
                            USGINISOElement(name='qualityElementResult',
                                search_paths=['gmd:result'],
                                multiplicity='1..*'), 
                            USGINISOElement(name='qualityElementResult',
                                search_paths=['gmd:result'], 
                                multiplicity='1..*'
                                )
                            ]
                       ),
            ]



class USGINLineageSource(USGINISOElement):
    #base element is LI_Source
    elements:[
        USGINISOElement(name='sourceDescription',
            search_paths=['gmd:description/gco:CharacterString/text()'], 
            multiplicity='0..1'),
        USGINISOElement(name='sourceScaleDenominator',
            search_paths=['gmd:scaleDenominator/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer/text()'], 
            multiplicity='0..1'),
        USGINISOElement(name='sourceSRS',
               search_paths=['gmd:sourceReferenceSystem/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier'], 
                multiplicity='0..1',
                elements=[
                    USGINISOElement(name='sourceSRSCode',
                        search_paths=['gmd:RS_Identifier/gmd:code/gco:CharacterString/text()'], 
                        multiplicity='1'),
                    USGINISOElement(name='sourceSRSCodeSpace',
                        search_paths=['gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString/text()'], 
                        multiplicity='0..1'),
                    USGINISOElement(name='sourceSRSCodeVersion',
                        search_paths=['gmd:RS_Identifier/gmd:version/gco:CharacterString/text()'], 
                        multiplicity='0..1'),
                    USGINISOElement(name='sourceSRSAuthorityName',
                        search_paths=['gmd:RS_Identifier/gmd:authority/gmd:CI_Citation/gmd:title/gco:CharacterString/text()'], 
                        multiplicity='0..1')
                ]
            ),
        USGINCitation(name='sourceCitation',
            search_paths=['gmd:sourceCitation/gmd:CI_Citation'], 
            multiplicity='0..1'),
        ISOSpatialExtent(name='sourceExtent',
            search_paths=['gmd:sourceExtent/gmd:EX_Extent'], 
            multiplicity='*')
        ]
    
class USGINLineageProcessStep(USGINISOElement):
    #base element is gmd:LI_ProcessStep
    elements=[
        USGINContact(name='stepLabel',
            search_paths=['gmd:description/gco:CharacterString/text()'], 
            multiplicity='0..1'),
        USGINContact(name='stepProcessors',
            search_paths=['gmd:processor'], 
            multiplicity='*'),
        USGINISOElement(name='stepProcessDescription',
            search_paths=['gmd:description/gco:CharacterString/text()'], 
            multiplicity='0..1'),
        USGINLineageSource(name='stepInputResources',
            search_paths=['gmd:source/gmd:LI_Source'], 
            multiplicity='*'
            ),  
        USGINLineageSource(name='stepOutputResources',  
            #catch sources that are not linked to process step
            #there will be some information loss if there are LI_Source/sourceStep associations
            search_paths=['../gmd:source/gmd:LI_Source'], 
            multiplicity='*'
            ),
        USGINISOElement(name='stepDateTimes',
            search_paths=['gmd:dateTime/gco:DateTime/text()'], 
            multiplicity='*'),
        USGINISOElement(name='stepRationale',
            search_paths=['gmd:rationale/gco:CharacterString/text()'], 
            multiplicity='0..1'),
    ]


class USGINMetadataInfo(USGINISOElement):

    elements = [  
        USGINISOElement(name='metadataIdentifier',
                        search_paths=['gmd:fileIdentifier/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='metadataLastUpdate',
                        search_paths=['gmd:dateStamp/gco:DateTime/text()', 'gmd:dateStamp/gco:Date/text()'],
                        multiplicity='1'),
        ISOResponsibleParty(name='metadataContacts',
                        search_paths=['gmd:contact'],
                        multiplicity='1..*'),
        USGINISOElement(name='metadataSpecification',
                        search_paths=["gmd:metadataStandardName", "gmd:metadataStandardVersion"],
                        multiplicity='0..1'
                       elements=[
                            USGINISOElement(name='referenceLabel',
                                search_paths=["gco:CharacterString/text()"],
                                multiplicity='1'),
                            USGINISOElement(name='referenceURIs',
                                search_paths=["gco:CharacterString/text()"],
                                multiplicity='1..*'),
                        ]),
        USGINISOElement(name='parentMetadata',
                        search_paths=['gmd:parentIdentifier'
                        ], 
                        multiplicity='0..1'
                        elements=[
                            USGINISOElement(name='referenceLabel',
                                search_paths=["gco:CharacterString/text()"],
                                multiplicity='1'),
                            USGINISOElement(name='referenceURIs',
                                search_paths=["gco:CharacterString/text()"],
                                multiplicity='1..*'),
                        ]),

        ISOMaintenance(name='metadataMaintenance',
                    search_paths=['gmd:metadataMaintenance/gmd:MD_MaintenanceInformation'
                       ], 
                    multiplicity='0..1'),
        USGINISOElement(name='metadataLanguage',
                    search_paths=['gmd:language'],
                    multiplicity='0..1'
                    elements = [ #language object
                        USGINISOElement(name='languageCode',
                            search_paths=[
                                "gmd:LanguageCode/@codeListValue",
                                "gco:CharacterString/text()"
                            ],
                            multiplicity='1'),
                         USGINISOElement(name='metadataLanguageCodeList',
                            search_paths=["gmd:LanguageCode/@codeList"
                            ], 
                            multiplicity='0..1')
                    ]),
        ISOConstraints(name='metadataUsageConstraint',
                    search_paths=['gmd:metadataConstraints'],
                    multiplicity='*'),
        USGINISOElement(name='metadataCharacterSet',
                        search_paths=['gmd:characterSet/gmd:CharacterSetCode/@codeListValue'
                        ], 
                        multiplicity='0..1'),
        USGINISOElement(name='metadataCharacterSetCodeList',
                        search_paths=['gmd:characterSet/gmd:CharacterSetCode/@codeList'
                        ], 
                        multiplicity='0..1'),
        ]


class USGINResourceDescription(USGINISOElement):

        # don't process SpatialRepresentation; -1 multiplicity throws warning in the log
        # TODO Need to build handlers for MD_GridSpatialRepresentation and MD_VectorSpatialRepresentation
        # the spatial represenations should be bound to particular distributions....

    elements = [  
        USGINISOElement(name='resourceTitle',
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString/text()',
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString/text()'
            ], 
            multiplicity='1'),
        USGINISOElement(name='resourceAbstract',
            search_paths=                                                   
                ['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/text()',
                'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:abstract/gco:CharacterString/text()',
                'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/gco:CharacterString/text()'
            ], 
            multiplicity='1'),
        USGINISOElement(name='resourceIdentifiers', search_paths=[
            'gmd:dataSetURI/gco:CharacterString/text()',
            'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'
                ,
            'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()'
                ,
            'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:ISBN/gco:CharacterString/text()'
                ,
            'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:ISBN/gco:CharacterString/text()'
                ,
            'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:ISSN/gco:CharacterString/text()'
                ,
            'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:ISSN/gco:CharacterString/text()'
                ,
            ], 
            multiplicity='*'),
        ISOResponsibleParty(name='citationResponsibleParties',
            search_paths=
                ['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty',
                'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty'
                ], 
                multiplicity='*'),
        USGINEventDate(name='citationDates',
                           search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date'
                           ,
                           'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date'
                           ], multiplicity='1..*'),
        USGINISOElement(name='citationAlternateTitles',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:alternateTitle/gco:CharacterString/text()'
                        ,
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:alternateTitle/gco:CharacterString/text()'
                        ], multiplicity='*'),
        USGINISOElement(
            name='citationDetails', 
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation', 
                          'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation'
                ],
            multiplicity='0..1',
            elements=[
                USGINISOElement(
                    name='edition',
                    search_paths=['gmd:edition/gco:CharacterString/text()'
                        ],
                    multiplicity='0..1'),
                USGINISOElement(name='editionDate',
                    search_paths=['gmd:editionDate/gco:Date/text()',
                                 'gmd:editionDate/gco:DateTime/text()'],
                    multiplicity='0..1'),
                USGINISOElement(
                    name='seriesName',
                    search_paths=['gmd:series/gmd:CI_Series/gmd:name/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINISOElement(
                    name='seriesIssue',
                    search_paths=['gmd:series/gmd:CI_Series/gmd:issueIdentification/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINISOElement(
                    name='page',
                    search_paths=['gmd:series/gmd:CI_Series/gmd:page/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINISOElement(
                    name='publicationDescription',
                    search_paths=['gmd:otherCitationDetails/gco:CharacterString/text()', 
                                  'gmd:collectiveTitle/gco:CharacterString/text()'
                        ], 
                    multiplicity='0..1'),
                USGINControlledConcept(
                    name='publicationPresentationForm',
                    search_paths=['gmd:presentationForm/gmd:CI_PresentationFormCode'
                        ], 
                    multiplicity='0..1'),
                ]
            )
              
        USGINControlledConcept(
            name='resourceTypes',
            search_paths=["gmd:hierarchyLevel/gmd:MD_ScopeCode", "gmd:hierarchyLevelName/gco:CharacterString" ],
            multiplicity='*'
                        ),
        USGINControlledConcept(
            name='resourceStatus',
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode',
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:status/gmd:MD_ProgressCode',
                        ], 
            multiplicity='*'),        USGINISOElement(name='notHandledresourceSpatialRepresentation',
                        search_paths=['gmd:spatialRepresentationInfo'],
                        multiplicity='-1'),
        ISOResponsibleParty(
            name='resourceContacts',
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact',
                            'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:pointOfContact'
                            ], 
            multiplicity='1..*'),
        ISOBrowseGraphic(name='resourceBrowseGraphic',
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:graphicOverview/gmd:MD_BrowseGraphic',
                         'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:graphicOverview/gmd:MD_BrowseGraphic'
                         ], 
            multiplicity='*'),
        ISOTemporalExtent(name='resourceTemporalExtents',
                          search_paths=['gmd:temporalElement'],
                          multiplicity='*'),
        USGINISOElement(name='resourceCharacterSet',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue'
                        ], 
                multiplicity='0..1'),
        USGINISOElement(name='resourceLanguages',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language'
                        ], 
                        multiplicity='*',
                        elements=[
                            USGINISOElement(name='languageCode',
                                search_paths=['gmd:LanguageCode/@codeListValue',
                                'gmd:LanguageCode/text()',
                                'gmd:CharacterString/text()'
                                ], 
                                multiplicity='1'
                )
            ]
         ),
        ISOSpatialExtent(name='resourceSpatialExtents',
                  search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent'
                  ,
                  'gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent'
                  ], multiplicity='*'),
        USGINISOElement(name='resourceSpatialDescription',
                search_paths=['gmd:referenceSystemInfo/gmd:MD_ReferenceSystem',
                                      'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType',
                                      'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution'
                ], 
                multiplicity='0..1',
                elements=[
                    USGINControlledConcept(name='resourceSpatialRepresentationTypes',
                        search_paths=['gmd:MD_SpatialRepresentationTypeCode'
                        ], multiplicity='*'
                    ),
                    USGINISOElement(name='resourceSpatialReferenceSystems',
                        search_paths=['gmd:referenceSystemIdentifier'], 
                        multiplicity='*',
                        elements=[
                            USGINISOElement(name='resourceSRSCode',
                            search_paths=['gmd:RS_Identifier/gmd:code/gco:CharacterString/text()'
                                         ], 
                            multiplicity='1'),
                            USGINISOElement(name='resourceSRSCodeSpace',
                                search_paths=['gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString/text()'
                                ], multiplicity='0..1'),
                            USGINISOElement(name='resourceSRSCodeVersion',
                                search_paths=['gmd:RS_Identifier/gmd:version/gco:CharacterString/text()'
                                ], multiplicity='0..1'),
                            USGINISOElement(name='resourceSRSAuthorityName',
                                search_paths=['gmd:RS_Identifier/gmd:authority/gmd:CI_Citation/gmd:title/gco:CharacterString/text()'
                                ], multiplicity='0..1')]),
                    USGINISOElement(name='resourceSpatialResolution',
                        search_paths=['gmd:MD_Resolution'
                        ], multiplicity='*',
                        elements=[
                            USGINISOElement(name='resolutionScaleDenominator',
                                search_paths=['gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer/text()'], 
                                multiplicity='0..1'),
                            USGINISOElement(name='resolutionDistanceValue',
                                search_paths=['gmd:distance/gco:Distance/text()'
                                ], multiplicity='0..1'),
                            USGINISOElement(name='resolutionUOM',
                                search_paths=['gmd:distance/gco:Distance/@uom'
                                ], multiplicity='0..1',
                                elements=[
                                    USGINISOElement(name='conceptURI',
                                        search_paths=['.'], 
                                        multiplicity='0..1'
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
        ISOKeywords(name='resourceIndexTerms',
                    search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords'
                    ,
                    'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords'
                    ], multiplicity='*'),
        USGINDistributorAccess(name='resourceAccessOptions',
                search_paths=['//gmd:MD_Distributor'], 
                multiplicity='*'),   #
        USGINISOElement(name='resourceLineageStatement',
                search_paths=['../gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString/text()'],
                    multiplicity='0..1'),
        USGINISOElement(name='resourceLineageScopeLevel',
            search_paths=['gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode/@codeListValue'], 
            multiplicity='0..1'),
        USGINLineageProcessStep(name='resourceLineageSteps',
            search_paths=['../gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep'
                        ], 
            multiplicity='*'),

        USGINISOElement(name='resourceQualityItems',
            search_paths=['gmd:dataQualityInfo/gmd:DQ_DataQuality'], 
            multiplicity='*', 
            elements=[
                USGINControlledConcept(name='qualityResultScopeLevel',
                    search_paths=['gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode'], 
                    multiplicity='1'),
                ISOQualityElement(name="qualityReport",
                    search_paths=["gmd:report"],
                    multiplicity="*"
                ),
        USGINISOElement(name='publicationPresentationForm',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/text()'
                        ,
                        'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/@codeListValue'
                        ,
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/text()'
                        ,
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/@codeListValue'
                        ], multiplicity='*'),
        USGINISOElement(name='publicationPresentationFormCodelist',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/@codeList'
                        ,
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/@codeList'
                        ], multiplicity='*'),

        USGINISOElement(name='resourcePurpose',
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString/text()',
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:purpose/gco:CharacterString/text()'
                        ], 
            multiplicity='0..1'),
        USGINISOElement(name='resourceCredit',
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:credit/gco:CharacterString/text()',
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:credit/gco:CharacterString/text()'
                        ], 
            multiplicity='*'),
        ISOMaintenance(name='resourceMaintenance',
            search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation',
                       'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation'
                       ], 
            multiplicity='*'),
        USGINISOElement(name='resourceFormats',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceFormat'
                        ,
                        'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceFormat'
                        ], multiplicity='*',
                        elements=[USGINISOElement(name='nativeFormatHref'
                        , search_paths=['@xlink:href'],
                        multiplicity='0..1'),
                        ISODataFormat(name='nativeFormat',
                        search_paths=['gmd:resourceFormat/MD_Format'],
                        multiplicity='0..1')]),
        ISOUsage(name='resourceSpecificUsage',
                 search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage'
                 ,
                 'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage'
                 ], multiplicity='*'),
        ISOConstraints(name='resourceUsageConstraints',
                       search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints'
                       ,
                       'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceConstraints'
                       ]),
        ISOAggregationInfo(name='relatedResources',
                           search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:aggregationInfo/gmd:MD_AggregateInformation'
                           ,
                           'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:aggregationInfo/gmd:MD_AggregateInformation'
                           ], multiplicity='*'),
        USGINISOElement(name='serviceType',
                        search_paths=['gmd:identificationInfo/srv:SV_ServiceIdentification/srv:serviceType/gco:LocalName/text()'
                        ], multiplicity='0..1'),
        USGINISOElement(name='resolutionDistanceValue',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='resolutionUOM',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance/@uom'
                        ], multiplicity='*'),
        USGINISOElement(name='resolutionScaleDenominator',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='topicCategory',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode/text()'
                        ], multiplicity='*'),
        USGINISOElement(name='resourceEnvironmentDescription',
                        search_paths=['gmd:identificationInfo/gmd:MD_DataIdentification/gmd:environmentDescription/gco:CharacterString/text()'
                        ], multiplicity='0..1'),
        ISOCoupledResources(name='serviceOperatesOnReferences',
                            search_paths=['gmd:identificationInfo/srv:SV_ServiceIdentification/srv:operatesOn'
                            ], multiplicity='*'),
        USGINISOElement(name='serviceOperatesOn',
                        search_paths=['gmd:identificationInfo/srv:SV_ServiceIdentification/srv:coupledResource/srv:SV_CoupledResource'
                        ], multiplicity='*',
                        elements=[ISOCoupledResources(name='serviceOperatesOnResourceID'
                        ,
                        search_paths=['srv:identifier/gco:CharacterString/text()'
                        ], multiplicity='1'),
                        USGINISOElement(name='serviceOperatesOnScopedName'
                        , search_paths=['gco:ScopedName/text()'],
                        multiplicity='0..1'),
                        USGINISOElement(name='serviceOperationName',
                        search_paths=['srv:operationName/gco:CharacterString/text()'
                        ], multiplicity='0..1')]),  
        USGINISOElement(name='notHandledApplicationSchema',
                        search_paths=['gmd:applicationSchemaInfo'],
                        multiplicity='-1'),
        USGINISOElement(name='notHandledPortrayalCatalogue',
                        search_paths=['gmd:portrayalCatalogueInfo'],
                        multiplicity='-1'),
        USGINISOElement(name='notHandledContentInfo',
                        search_paths=['gmd:contentInfo'],
                        multiplicity='-1'),
        ]


    # this is the main dictionary that gets used by usgin.py to
# construct the extras.md_package JSON object for USGIN metadata handling
# note: the operations stuff in sv_serviceIdentification is not handled.
# the big show--putting it all together in one dictionary

class USGINXmlMapping(MappedXmlDocument):

    """ this class constructs a dictionary of all the ISO content elements
        each with multiplicity, key name, search_paths list. Used as dictionary
     to pull xml content into a dictionary for mapping to other formats;
     returns a list of objects in the .elements attribute"""

    #  new mapping by SMR to ISO19115-2 and 19110, using USING metadata JSON v3.0
    # 2016-01-21

    elements = [
        USGINContact(
            name='contacts',
            search_paths=['//gmd:CI_ResponsibleParty/..'],
            multiplicity='*'), 
        USGINMetadataInfo(
            name='metadataInfo',
            search_paths=["gmd:MD_Metadata","gmi:MI_Metadata"], 
            multiplicity='1'),
        USGINResourceDescription(
            name='describedResource',
            search_paths=["gmd:MD_Metadata","gmi:MI_Metadata"], 
            multiplicity='1')
        ]

    def infer_values2(self, values):

        # Todo: Infer name.

        self.infer_date_released(values)
        self.infer_date_updated(values)
        self.infer_date_created(values)
        self.infer_url(values)

        # Todo: Infer resources.
        # self.infer_tags(values)
        # self.infer_publisher(values)
        # self.infer_contact(values)
        # self.infer_contact_email(values)

        return values

    def infer_date_released(self, values):
        value = ''
        for date in values['citationDates']:
            if date['eventTypeConceptLabel'] == 'publication':
                value = date['eventDateTime']
                break
        values['date-released'] = value

        # from usgin.py

        if value:
            date_obj = parse(value)
            value = date_obj.replace(tzinfo=None)
        values['publication_date'] = value  # add to account for NgdsXmlMapping

    def infer_date_updated(self, values):
        value = ''
        dates = []

        # Use last of several multiple revision dates.

        for date in values['citationDates']:
            if date['eventTypeConceptLabel'] == 'revision':
                dates.append(date['eventDateTime'])

        if len(dates):
            if len(dates) > 1:
                dates.sort(reverse=True)
            value = dates[0]

        values['date-updated'] = value

    def infer_date_created(self, values):
        value = ''
        for date in values['citationDates']:
            if date['eventTypeConceptLabel'] == 'creation':
                value = date['eventDateTime']
                break
        values['date-created'] = value

    def infer_url(self, values):
        value = ''
        for locator in values['resourceAccessLinks']:
            if locator['function'] == 'information':
                value = locator['linkURL']
                break
        values['url'] = value


