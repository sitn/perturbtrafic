

from owslib.wfs import WebFeatureService
import xmltodict
import json

class WFSQuery():

    @classmethod
    def do_query_wfs(cls, request, typename, propertyname, bbox, return_template, filter):

        """
        Query a WFS service
        """

        try:

            settings = request.registry.settings
            url = settings['spch_wfs_url']
            version = settings['version']
            srsname = settings['srsname']

            localites_typename = settings['localites_typename']
            cadastre_typename = settings['cadastre_typename']
            communes_typename = settings['communes_typename']

            wfs = WebFeatureService(url=url, version=version)

            response = wfs.getfeature(typename=typename,
                                      propertyname=propertyname,
                                      srsname=srsname,
                                      bbox=bbox,
                                      filter=filter)

            #gml = ElementTree.fromstring(response.read())
            xpars = xmltodict.parse(response.read())
            #wfs_json = json.dumps(xpars)

            formattedFeatures = []

            if "wfs:FeatureCollection" in xpars and "gml:featureMember" in xpars["wfs:FeatureCollection"]:
                features = xpars["wfs:FeatureCollection"]["gml:featureMember"]

                for feature in features:

                    currentTypename = None

                    if "ms:" + localites_typename in feature:
                        currentTypename = localites_typename
                    elif "ms:" + cadastre_typename in feature:
                        currentTypename = cadastre_typename
                    elif "ms:" + communes_typename in feature:
                        currentTypename = communes_typename

                    if "ms:" + currentTypename in feature:
                        atts = feature["ms:" + currentTypename]
                        one_return_obj = cls.substitute(atts, return_template)
                        formattedFeatures.append(json.loads(one_return_obj))

            return formattedFeatures

        except Exception as error:
            raise Exception(str(error))
            #return []


    @classmethod
    def substitute(cls, attributes, template):
        """
        Substitute according to a template
        """
        result = template

        for key in attributes.keys():
            result = result.replace('{' + key + '}', attributes[key])

        return result


