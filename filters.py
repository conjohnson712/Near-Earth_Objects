"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator
from itertools import islice

class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """
    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


"""
    Inspiration for filter design drawn from 'Tasks: 3A' portion of this 
    project's instructions:
    https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/ab4e6345-8dc2-4439-8c67-afa21ae710ce/concepts/c6dc8c7b-97e2-42e6-a77a-64fb39b27203
    (Accessed: 2/18/22)

    Docstring params copied from the class method above for consistency
"""
class DateFilter(AttributeFilter):
    """ A class designed to filter for date, start_date, and end_date """

    @classmethod
    def get(cls, approach):
        """ Function that retrieves the desired attribute 
        
            :param approach: A `CloseApproach` on which to evaluate this filter.
            :returns: The time of the CloseApproach, translated to a date
        """

        return approach.time.date()   # From Tasks 3A: 'On Comparing Dates'

class DistanceFilter(AttributeFilter):
    """A class designed to filter for distance_min and distance_max """

    @classmethod
    def get(cls, approach):
        """ Function that retrieves the desired attribute 
        
            :param approach: A `CloseApproach` on which to evaluate this filter.
            :returns: The distance, in au, of the Close Approach
        """
    
        return approach.distance

class VelocityFilter(AttributeFilter): 
    """ A class designed to filter for velocity_min and velocity_max"""

    @classmethod
    def get(cls, approach): 
        """ Function that retrieves the desired attribute 
        
            :param approach: A `CloseApproach` on which to evaluate this filter.
            :returns: The Velocity, in km/s, of the Close Approach.
        """

        return approach.velocity

class DiameterFilter(AttributeFilter):
    """ A class designed to filter for diameter_min and diameter_max"""

    @classmethod
    def get(cls, approach):
        """ Function that retrieves the desired attribute 
        
            :param approach: A `CloseApproach` on which to evaluate this filter.
            :returns: The diameter, in km, of the Close Approach NEO
        """

        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    """ A class designed to filter for Hazardous Potentiality """

    @classmethod
    def get(cls, approach): 
        """ Function that retrieves the desired attribute 
        
            :param approach: A `CloseApproach` on which to evaluate this filter.
            :returns: The Hazard status of the Close Approach NEO
        """

        return approach.neo.hazardous

def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):


    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurRed
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
   
   
    filters = []
    """ Create an empty list for filters """
    

    """ Date filters use the following operator pattern:
        start_date <= date <= end_date. The operators for the 
        filters follow this also, with 'date' being the relative 
        point of comparison. This concept will be used throughout.

        With parameters defaulted to None, we will use if statements to 
        check against them not being None to cover all edge cases.

        References:

        Inspired from Tasks 3A: 'On Comparing Dates':
        https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/ab4e6345-8dc2-4439-8c67-afa21ae710ce/concepts/c6dc8c7b-97e2-42e6-a77a-64fb39b27203        
    """

    if start_date is not None:
        filters.append(DateFilter(operator.ge, start_date))

    if date is not None: 
        filters.append(DateFilter(operator.eq, date))

    if end_date is not None: 
        filters.append(DateFilter(operator.le, end_date))
    
    if distance_min is not None: 
        filters.append(DistanceFilter(operator.ge, distance_min))

    if distance_max is not None: 
        filters.append(DistanceFilter(operator.le, distance_max))
    
    if velocity_min is not None: 
        filters.append(VelocityFilter(operator.ge, velocity_min))

    if velocity_max is not None:
        filters.append(VelocityFilter(operator.le, velocity_max))

    if diameter_min is not None: 
        filters.append(DiameterFilter(operator.ge, diameter_min))

    if diameter_max is not None: 
        filters.append(DiameterFilter(operator.le, diameter_max))

    if hazardous is not None: 
        filters.append(HazardousFilter(operator.eq, hazardous))


    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.

    References: 
    
    Inspired by the following answers in Knowledge provided by the 
    Mentor Shuaishuai:
    https://knowledge.udacity.com/questions/676611
    https://knowledge.udacity.com/questions/665490
    """
   
    if n in [0, None]:
        return islice(iterator, None)
    else: 
        return islice(iterator, n)
