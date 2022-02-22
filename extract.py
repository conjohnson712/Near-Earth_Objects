"""Extract data on near-Earth objects and close approaches CSV and JSON.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of
`NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON
file, formatted as described in the project instructions, into a
collection of `CloseApproach` objects.

The main module calls these functions with the arguments provided at
the command line, and uses the resulting collections to build an
`NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from helpers import cd_to_datetime  # Imported for row['time']
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about
    near-Earth objects.
    :return: A collection of `NearEarthObject`s.

    Default values are enforced using if/else statements. Spaces added
    between statements for readability. Key values used in neo_data_out
    were designed to match the headers from the csv file. Arguments are
    ordered by order of appearance in the NearEarthObject class.

    Row['pha'] was originally Row['hazardous'], but raised errors that
    I could only seem to solve by making it match the CSV file header
    for hazardous.

    References:
    Structure of function inspired by Lesson 5, Content 9: CSV I/O:
    https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/5f6da81f-9ca0-4a6b-9b3c-66cadfd9a1c1/concepts/e86aadb6-0dd7-4bf9-9950-b1d772e6e71c
    (Accessed: 2/18/22)
    """
    with open(neo_csv_path, 'r') as neo_infile:
        neo_data_in = []

        reader = csv.DictReader(neo_infile)  # DictReader uses headers
        for row in reader:
            if row['pdes'] is not None:
                row['pdes'] = str(row['pdes'])

            if row['name'] in [None, '']:
                row['name'] = None
            else:
                row['name'] = str(row['name'])

            if row['diameter'] is "":
                row['diameter'] = float('nan')
            else:
                row['diameter'] = float(row['diameter'])

            if row['pha'] in ['N', '']:
                row['pha'] = False
            else:
                row['pha'] = True

            neo_data_out = NearEarthObject(
                designation=row['pdes'],
                name=row['name'],
                diameter=row['diameter'],
                hazardous=row['pha']
            )

            neo_data_in.append(neo_data_out)
    return (neo_data_in)


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data
     about close approaches.
    :return: A collection of `CloseApproach`es.

    References:
    Structure of function inspired by Lesson 5, Concept 6: JSON I/O:
    https://classroom.udacity.com/nanodegrees/nd303/parts/31252231-c52a-4a03-836f-f155c9a01edd/modules/cdd764fd-cd4e-4610-b206-8ea2f5a36968/lessons/5f6da81f-9ca0-4a6b-9b3c-66cadfd9a1c1/concepts/9c97771c-96d8-40f8-97e8-1e988369f46b
    (Accessed: 2/18/22)

    The general structure from load_neos was followed for this function.
    Row names for ca_data_out were chosen to match those found in the
    cad_json file.

    Row['time'] posed a key error. Inspiration for a solution came from
    the following Google search result:
    https://realpython.com/python-keyerror/  (Accessed: 2/18/22)
    """
    with open(cad_json_path, 'r') as ca_infile:  # ca = Close Approach
        ca_data_in = []

        contents = json.load(ca_infile)
        content_data = contents["data"]

        for row in content_data:
            if row[0] is not None:
                row[0] = str(row[0])

            if row[3] is None:
                row[3] = "Time Unknown to NASA"
            else:
                row[3] = cd_to_datetime(row[3])

            if row[4] is None:
                row[4] = float('nan')
            else:
                row[4] = float(row[4])

            if row[7] is None:
                row[7] = float('nan')
            else:
                row[7] = float(row[7])

            ca_data_out = CloseApproach(
                _designation=row[0],
                time=row[3],
                distance=row[4],
                velocity=row[7]
            )

            ca_data_in.append(ca_data_out)
    return (ca_data_in)
