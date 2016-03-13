from sys import argv
import re
from figure import Figure, check_intersection
from context import Context


if len(argv) != 3:
    print "Usage: python eminescu.py [input] [output]"

inputFile = open(argv[1])
outputFile = open(argv[2], "w")

figures = dict()
context = Context()
current_id = 0

for verse in inputFile.readlines():
    verse = verse.lower()
    if verse.find("vreau") != -1:

        if context.number_conditions > 0 and not context.should_evaluate():
            continue

        if verse.find("patrat") != -1:

            match = re.search('latura\s*(\d*\.?\d*)', verse, re.I | re.M)
            dimension = float(match.group(1))
            match = re.search('punctul\s*\(\s*(\d*\.?\d*)\s*,\s*(\d*\.?\d*)\s*\)', verse, re.I | re.M)
            point_x, point_y = float(match.group(1)), float(match.group(2))

            figures[current_id] = Figure("Patrat")
            figures[current_id].add_point(point_x, point_y)
            figures[current_id].add_point(point_x + dimension, point_y)
            figures[current_id].add_point(point_x + dimension, point_y + dimension)
            figures[current_id].add_point(point_x, point_y + dimension)

            current_id += 1

        elif verse.find("dreptunghi") != -1:

            match = re.search('laturi\s*\(\s*(\d*\.?\d*)\s*,\s*(\d*\.?\d*)\s*\)', verse, re.I | re.M)
            dimension_x, dimension_y = float(match.group(1)), float(match.group(2))
            match = re.search('punctul\s*\(\s*(\d*\.?\d*)\s*,\s*(\d*\.?\d*)\s*\)', verse, re.I | re.M)
            point_x, point_y = float(match.group(1)), float(match.group(2))

            figures[current_id] = Figure("Dreptunghi")
            figures[current_id].add_point(point_x, point_y)
            figures[current_id].add_point(point_x + dimension_x, point_y)
            figures[current_id].add_point(point_x + dimension_x, point_y + dimension_y)
            figures[current_id].add_point(point_x, point_y + dimension_y)

            current_id += 1

        elif verse.find("poligon") != -1:
            matches = re.findall('\(\s*(\d*\.?\d*)\s*,\s*(\d*\.?\d*)\s*\)', verse, re.I | re.M)

            figures[current_id] = Figure("Poligon")
            for match in matches:
                figures[current_id].add_point(float(match[0]), float(match[1]))

            current_id += 1

    elif verse.find("muta") != -1:

        if context.number_conditions > 0 and not context.should_evaluate():
            continue

        match = re.search('figura\s*(\d*)', verse, re.I | re.M)
        figure_id = int(match.group(1))
        match = re.search('cu\s*(\d*\.?\d*)', verse, re.I | re.M)
        distance = float(match.group(1))

        if verse.find("stanga") != -1:
            figures[figure_id].do_translation(-distance, 0.)
        elif verse.find("dreapta") != -1:
            figures[figure_id].do_translation(distance, 0.)
        elif verse.find("sus") != -1:
            figures[figure_id].do_translation(0., distance)
        elif verse.find("jos") != -1:
            figures[figure_id].do_translation(0., -distance)

    elif verse.find("roteste") != -1:

        if context.number_conditions > 0 and not context.should_evaluate():
            continue

        match = re.search('figura\s*(\d*)', verse, re.I | re.M)
        figure_id = int(match.group(1))
        match = re.search('cu\s*(\d*\.?\d*)', verse, re.I | re.M)
        angle = float(match.group(1))
        match = re.search('punctul\s*\(\s*(\d*\.?\d*)\s*,\s*(\d*\.?\d*)\s*\)', verse, re.I | re.M)
        coord_x, coord_y = float(match.group(1)), float(match.group(2))

        figures[figure_id].do_rotation(angle, coord_x, coord_y)

    elif verse.find("sterge") != -1:

        if context.number_conditions > 0 and not context.should_evaluate():
            continue

        match = re.search('figura\s*(\d*)', verse, re.I | re.M)
        figure_id = int(match.group(1))

        del figures[figure_id]

    elif verse.find("gata") != -1:
        if context.has_extra():
            context.remove_extra_end()
        else:
            context.remove_layer()

    elif verse.find("altfel") != -1:
        if context.has_extra():
            context.remove_extra_else()
        else:
            context.set_location(False)

    elif verse.find("daca") != -1:

        if context.number_conditions > 0 and not context.should_evaluate():
            context.add_extra()
        else:
            matches = re.findall('figura\s*(\d*)', verse, re.I | re.M)
            figure_id1 = int(matches[0])
            figure_id2 = int(matches[1])

            context.add_layer(check_intersection(figures[figure_id1], figures[figure_id2]))


key_list = figures.keys()
key_list.sort()
for key in key_list:
    points = figures[key].get_points_list()
    points.sort()
    outputFile.write(str(key) + " " + figures[key].name + ":\n")
    for point in points:
        outputFile.write(str(point[0]) + " " + str(point[1]) + "\n")

inputFile.close()
outputFile.close()
