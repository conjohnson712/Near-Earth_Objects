"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.

        Inspiration on how to complete this segment came from:
        The following Mentor response in Knowledge: 
        https://knowledge.udacity.com/questions/632763

        Lesson 2, Concept 17: Dictionaries: 
        https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/f54b2b40-94d2-4d75-b26b-163f583d5175/concepts/b0daa716-c1d0-4f3a-9608-5506bf99db0e

        Lesson 2, Concept 20: Comprehensions:
        https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/f54b2b40-94d2-4d75-b26b-163f583d5175/concepts/d44e42d5-0eee-4c28-a8a7-c3c67df00bec
        """
        self._neos = neos
        self._approaches = approaches

        

        # Create Empty dictionaries for Designation and Name Key-Value 
        # pairs to be stored in
        self._designation_dict = {} 
        self._name_dict = {} 


        # Scan through neos for designations and names
        for neo in self._neos:
            if neo.designation is not None: 
                self._designation_dict[neo.designation] = neo
            

            if neo.name is not None: 
                self._name_dict[neo.name] = neo
            


        # Scan through approaches for designations and neo
        # ca = CloseApproach
        for ca in self._approaches: 
            self._designation_dict[ca._designation] = neo
            
            if ca.neo is not None: 
                ca.neo = neo
                
            
            neo.approaches.append(ca)


    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        
        Inspired by .get portion of Lesson 2, Concept 17: Dictionaries: 
        https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/f54b2b40-94d2-4d75-b26b-163f583d5175/concepts/b0daa716-c1d0-4f3a-9608-5506bf99db0e

        .upper was used to ensure that the designation is in all caps to match 
        the data. .get allows for the default None to be set. 
        """
     

        return self._designation_dict.get(designation.upper(), None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.

        .capitalize() was added to ensure the names match those in the data. 
        .get allows for the default value of None to be set

        References: 

        Inspired by .get portion of Lesson 2, Concept 17: Dictionaries: 
        https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/f54b2b40-94d2-4d75-b26b-163f583d5175/concepts/b0daa716-c1d0-4f3a-9608-5506bf99db0e
        """
        
        
        return self._name_dict.get(name.capitalize(), None)

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.

        References: 

        Inspired by pseudocode from the following Knowledge question: 
        https://knowledge.udacity.com/questions/633232

        And from Lesson 3, Concept 13/14: Higher Order Functions Exercise 
        https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/406e03f0-82b1-46aa-b7c1-0223223240cb/concepts/e6d2975e-ce00-4a31-b778-dca024115eab
        """

        for approach in self._approaches:
            flag = False in map(lambda x: x(approach), filters)
        
            if flag == True: 
                yield approach
