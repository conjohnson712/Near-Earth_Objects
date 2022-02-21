"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""

from helpers import cd_to_datetime, datetime_to_str
import datetime

class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
  
    def __init__(self, designation, name=None, diameter=float('nan'), 
                 hazardous=False):
        """Create a new `NearEarthObject`.

        :param designation: A unique value that designates NEOs, like an ID
        :param name: An optional value that acts as a 2nd unique Identifier
        :param diameter: A NEO's diameter in au units
        :param hazardous: A determination of an NEO's Hazardousness
        :return: An empty list of approaches for later use
        
        
        Default values for key terms are given above and reiterated 
        below with if/else statements. Assertion statements were added 
        to all values to ensure they are the correct type. Spaces were 
        added between arguments for readability. 
        """
        
        self.designation = designation
        assert isinstance(self.designation, str), "Designation must resolve to a string"

        self.name = name # Originally had an assertion, but raised errors

        self.diameter = diameter
        assert isinstance(self.diameter, float), "Diameter must be a float"

        self.hazardous = hazardous #Originally had assertion, raised errors
        

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO. First 
           checks to see if the NEO has a name. If not, the full name
           is the designation alone. Otherwise, the name is added.
        """
        
        if self.name is None:
            return f"{self.designation}"
        else:
            return f"{self.designation} ({self.name})"

    def serialize(self): 
        """ Returns a dictionary representation of self 
            attributes relevant to NEO.

            Returns: Keys of self attributes
        """

        return { 
            "designation": self.designation,
            "name": self.name, 
            "diameter_km": self.diameter, 
            "potentially_hazardous": self.hazardous
        }

    def __str__(self):
        """Return `str(self)`. First determines if the NEO is 
           hazardous, then gives a different response depending on the 
           result. Self.fullname was used to save space and time from 
           determining if the NEO has a name. ':.3f' was added to 
           self.diameter, following the trend from __repr__ to limit the 
           number of decimal places to three. 
        """

        if self.hazardous == True:
            self.hazardous = "IS hazardous"
        else: 
            self.hazardous = "is NOT hazardous"

        return f"""The NearEarthObject(NEO), {self.fullname}, has a 
        diameter of {self.diameter:.3f} au and {self.hazardous}!"""

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, _designation, time=None, distance=float(0.0), 
                 velocity=float(0.0), neo=None):
        """Create a new `CloseApproach`.

           :param _designation: The unique identifier used for CloseApproach
           :param time: Datetime representing the time of CloseApproach
           :param distance: Float representing distance from Earth in au units
           :param velocity: Float representing velocity of CloseApproach
           :param neo: Determination of if CloseApproach is also an NEO
           :return: self.neo which is used in other modules.
           
           Default values were given with the arguments, as well as 
           reiterated below using if/else statements. Each value has 
           been given an assertion statement to ensure they are the 
           required type. Spaces were added between arguments for 
           readability.
        """
       
        self._designation = _designation
        assert isinstance(self._designation, str), """_designation must 
        resolve to a string"""

        self.time = time
        assert isinstance(self.time, datetime.datetime), """time must be 
        a datetime"""

        self.distance = distance
        assert isinstance(self.distance, float), "distance must be a float"

        self.velocity = velocity
        assert isinstance(self.velocity, float), "velocity must be a float"

        # Create an attribute for the referenced NEO, originally None.
        self.neo = self._designation
    

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.

        _______________________________________

        An if/else statement was added to determine if there is a value 
        for self.time. If not, a message is returned. If so, then the 
        value is run through the datetime_to_str function. 
        """
        
        if self.time is not None:
            return datetime_to_str(self.time)
        

    def serialize(self): 
        """ Returns a dictionary representation of self attributes relevant
            to CloseApproach
        
            Returns: Keys of self attributes
        """

        return {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity
        }

    def __str__(self):
        """Return `str(self)`. Numerical arguments were given ':.2f' at 
        the end, following the trend from __repr__, to limit the decimal 
        values to two digits. 
        """

        return f"""On {self.time_str}, a CloseApproach, {self.neo.fullname},  
                came within {self.distance:.2f} au of Earth, hurdling at a 
                velocity of {self.velocity:.2f} km/s!
                """

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")


