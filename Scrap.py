from IPython.display import clear_output
from Analyze import *

# A Scrap is an object from a Scrapalyze method
class Scrap:
    """
    A Scrap is a class that contains specific methods for formatting the results of Scrapalyze methods.
    """
    
    # Initializes the scrap with the list scraped from the Scrapalyze class
    def __init__(self, contents, fast, show_stats):
        self.contents = contents
        self.fast = fast
        if fast == False:
            self.slow_scrape_embedded_layers()
        if show_stats == True:
            self.stats
            
             
    
    # Display standard statistics for the Scrap
    @property
    def stats(self):
        """
        Stats is a property fuction that outputs statistics about the element you scraped.
        """
        # Length of contents
        try:
            print("Scrap contains {} HTML elements.".format(len(self.contents[0])))   
        except:
            print("The element you have tried to scrape does not exist.")
            
        if self.fast == False:
            # Number of embedded layers
            print("Number of embedded layers: {}".format(self.num_layers))
    
    # Scrape elements and tags from each layer of embedded HTML
    def slow_scrape_embedded_layers(self):
        """
        This method will executed automatically on initialization if the fast argument is set to False.
        """
        i = 1
        self.embedded_layers = {}
        layer_elements = []
        while not isinstance(layer_elements, str):
            layer_tags = self.scrape_embedded_elements(layer=i)[0]
            layer_elements = self.scrape_embedded_elements(layer=i)[1]
            self.num_layers = self.scrape_embedded_elements(layer=i)[2]
            self.embedded_layers[i] = (layer_tags,layer_elements)
            print("Please be patient, loading layer: {}".format(i))
            clear_output(wait=True)
            i += 1
        self.num_layers += 1
        clear_output(wait=True)
        print("Process is complete. Number of layers: {}".format(self.num_layers))
            
    # Scrap tags based upon their layers of embedding
    def scrape_embedded_elements(self, 
                                 layer = 1):
        """
        Iterates through the contents of the initiliazed list.
        Extracts all embedded tags and element for easy internal navigation.
        """
        contents = self.contents
        end = 1
        for i in range(layer):
            layer_tags = []
            layer_elements = []
            for element in contents:
                if not isinstance(element, str):
                    for child in list(element.children):
                        layer_tags.append(child.name)
                        layer_elements.append(child)
                layer_tags = list(set(layer_tags))
                later_elements = list(set(layer_elements))
            contents = layer_elements
            if contents != []:
                end = i
            else:
                layer_elements = "There are no more layers"
                layer_tags = "There are no more layers"
        return layer_tags,layer_elements,end
    
    # Print the scraped embedded elements
    def filter_embedded_layers(self, 
                               layer=1, 
                               specify=[],
                               tags_elements=1):
        """
        Returns the elements or tags of an embedded layer.
        layer: default 1. Displays the first layer of elements. 
        Each increment represents 1 layer i.e. 3 is the third layer of embedded elements.
        specify: default empyt list. Add any HTML tags in the list to display only those elements.
        tags_elements: default 1. Change to 0 if you want to return tags instead of full elements.
        """    
        if self.fast == True:
            scrape_results = []
            if not isinstance(self.scrape_embedded_elements(layer=layer)[tags_elements], str):
                for element in self.scrape_embedded_elements(layer=layer)[tags_elements]:
                    if specify != []:
                        for s in specify:
                            if tags_elements == 1:
                                if element.name == s:
                                    scrape_results.append(element)
                            elif tags_elements == 0:
                                if element == s:
                                    scrape_results.append(element)
                    else:
                        scrape_results.append(element)
                return analyze(scrape_results)
                #return scrape_results
            else:
                return analyze(self.scrape_embedded_elements(layer=layer)[tags_elements])
                #return self.scrape_embedded_elements(layer=layer)[tags_elements]
        else:
            scrape_results = []
            if not isinstance(self.embedded_layers[layer][tags_elements], str):
                for element in self.embedded_layers[layer][tags_elements]:
                    if specify != []:
                        for s in specify:
                            if tags_elements == 1:
                                if element.name == s:
                                    scrape_results.append(element)
                            elif tags_elements == 0:
                                if element == s:
                                    scrape_results.append(element)
                    else:
                        scrape_results.append(element)
                return analyze(scrape_results)
                #return scrape_results
            else:
                return analyze(self.embedded_layers[layer][tags_elements])
                #return self.embedded_layers[layer][tags_elements]
                                    
    
    
        
        

        
    
    