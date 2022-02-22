"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`,
each of which accept an `results` stream of close approaches and a path
to which to write the data.

These functions are invoked by the main module with the output of the
`limit' function and the filename supplied by the user at the command
line. The file's extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each
    output row corresponds to the information in a single close approach
    from the `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data
     should be saved.

    References:
    Lesson 5, Concept 9: CSV I/O
    https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/5f6da81f-9ca0-4a6b-9b3c-66cadfd9a1c1/concepts/e86aadb6-0dd7-4bf9-9950-b1d772e6e71c

    Tasks
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')

    # Outfile names kept consistent with infile names from extract.py
    with open(filename, "w", newline="") as neo_outfile:
        writer = csv.DictWriter(neo_outfile, fieldnames=fieldnames)
        writer.writeheader()

        # ca = CloseApproach
        for approach in results:
            writer.writerow({
                'datetime_utc': approach.time,
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach._designation,
                'name': approach.neo.name,
                'diameter_km': approach.neo.diameter,
                'potentially_hazardous': approach.neo.hazardous
            })


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the
    output is a list containing dictionaries, each mapping
    `CloseApproach` attributes to their values and the 'neo' key
    mapping to a dictionary of the associated NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data
     should be saved.

    References:
    Lesson 5, Concept 6: JSON I/O:
    https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/5f6da81f-9ca0-4a6b-9b3c-66cadfd9a1c1/concepts/9c97771c-96d8-40f8-97e8-1e988369f46b

    Tasks
    """

    json_list = []

    for approach in results:
        json_headers = {
            'datetime_utc': approach.time_str,
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': {
                'designation': approach._designation,
                'name': approach.neo.name,
                'diameter_km': approach.neo.diameter,
                'potentially_hazardous': approach.neo.hazardous
            }
        }
        json_list.append(json_headers)

    with open(filename, "w") as json_outfile:
        json.dump(json_list, json_outfile, indent=4)
