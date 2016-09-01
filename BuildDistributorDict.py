  class USGINAccessOption(USGINISOElement):
  
    def buildDistributors(self, aDistribution ):
        """
        Each distributor may have multiple digitalTrasferOptions, MD_format, standard order process. 
        if only one distributor is present, links from MD_Distribution to transferOptions and format have to be projected to distributor
        if no distributor provided, create an unknown and associate with the required DigitalTransferOptions linksage
        These distributions correspond to ckan package.resources

        returns a list of distributors with transfer options for each
        aDistribution is an MD_distribution element
        used to populate the resourceAccessOptions element in the JSON metadata
        """
        thedistributors = []
        distFormats = []


        # have no distributor, but do have distribution transferOption
        if not (aDistribution["distributors"]):
            #if formats are specified, they are put in in the accessLinks.linkTargetResourceType
            #access links is an array



            if ( aDistribution.get("distributionFormats") and
                        isinstance(aDistribution["distributionFormats"], list)):
                    distFormats = self.buildFormats(aDistribution["distributionFormats"])

            thisDistributor["distributor"]= {"contactID":"missing"}

            if aDistribution.get("distributionTransferOptions"):
                for option in aDistribution["distributionTransferOptions"]:
                    thelinks = self.buildLinks(option,distFormats)
                    for alink in thelinks:
                        thisDistributor["accessLinks"].append(alink)
            thedistributors.append(thisDistributor )
        else:
            for aDistributor in aDistribution["distributors"]:
                thisDistributor = {}
                thisDistributor["distributor"]= {}
                thisDistributor["accessLinks"] = []
                if  (aDistributor["distributor"].get("distributorFormats") and
                       isinstance(aDistributor["distributor"]["distributorFormats"], list)):
                    distFormats=self.buildFormats(aDistributor["distributor"]["distributorFormats"])
                    # for aFormat in aDistributor["distributor"]["distributorFormats"]:
                    #     formatList.append(aFormat)
                elif ( aDistribution.get("distributionFormats") and
                        isinstance(aDistribution["distributionFormats"], list)):
                    distFormats=self.buildFormats(aDistribution["distributionFormats"])
                    # for aFormat in aDistribution["distributionFormats"]:
                    #     formatList.append(aFormat["distributionFormat"])
                else:
                    distFormats = []


                if aDistributor.get("distributorHref"):
                    thisDistributor["distributor"] = {
                        "agentRole":{"conceptPrefLabel":"pointOfcontact" },
                        "contactID":aDistributor["distributorHref"]
                    }

                    if aDistribution.get("distributionTransferOptions"):
                        for option in aDistribution["distributionTransferOptions"]:
                            thelinks = self.buildLinks(option,distFormats)
                            for aLink in thelinks:
                                thisDistributor["accessLinks"].append(aLink)

                else:
                    thisDistributor["distributor"]= {}
                    if  aDistributor["distributor"].get("distributorID"):
                        thisDistributor["distributor"]["contactID"] = aDistributor["distributor"]["distributorID"]
                    # handle the agent; builder returns an object that is separated into keys in the distributor
                    theAgent = self.buildContactInRole(aDistributor["distributor"].get("distributorContact"))
                    thisDistributor["distributor"]["agentRole"] =theAgent["agentRole"]
                    thisDistributor["distributor"]["agent"]= theAgent["agent"]

                    if aDistributor["distributor"].get("distributorTransferOptions"):
                        for option in aDistributor["distributor"]["distributorTransferOptions"]:
                            thelinks = self.buildLinks(option,distFormats)
                            for aLink in thelinks:
                                thisDistributor["accessLinks"].append(aLink)

                    if aDistribution.get("distributionTransferOptions"):
                        for option in aDistribution["distributionTransferOptions"]:
                            thelinks = self.buildLinks(option,distFormats)
                            for aLink in thelinks:
                                thisDistributor["accessLinks"].append(aLink)

                # TODO offline access

                thedistributors.append(thisDistributor)
            return thedistributors