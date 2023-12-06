import re

with open('input.txt', 'r') as file:
    lines = file.read().splitlines()
# parse seeds
seeds = [int(seed) for seed in re.findall(r'\d+', lines[0])]
# parse maps
maps = {}
for line in lines[1:]:
    if ':' in line:
        key = line
        maps[key] = []
    elif line != '':
        values = tuple(int(x) for x in re.findall(r'\d+', line))
        maps[key].append(values)

# part 1
def find_location(seed, maps):
    for key, values in maps.items():
        # value: (destination, source, length)
        for value in values:
            if value[1] <= seed < value[1] + value[2]:
                seed = seed - value[1] + value[0]
                break
    return seed

locations = [find_location(seed, maps) for seed in seeds]
min_location = min(locations)
print(min_location)

# part 2
def get_new_ranges(map, seeds_range):
    new_ranges = []
    for seed in seeds_range:
        for dest, source, len in map:
            source_end = source + len - 1
            dest_end = dest + len - 1
            if seed[1]<source or seed[0]>source_end:
                continue
            res_start = max(seed[0], source)
            res_end = min(seed[1], source_end)
            diff = dest - source
            new_ranges.append((res_start + diff, res_end + diff))
            if seed[0]<res_start-1:
                seeds_range.append((seed[0], res_start-1))
            if seed[1]-1>res_end:
                seeds_range.append((res_end+1, seed[1]))
            break
        else:
            new_ranges.append((seed[0], seed[1]))
    return new_ranges

def find_locations_range(seeds_range, maps):
    new_ranges = list(seeds_range)
    for key, values in maps.items():
        map_ranges = list(new_ranges)
        # clear the current ranges when entering a new map
        new_ranges.clear()
        new_ranges.extend(get_new_ranges(values, map_ranges))
    return new_ranges

seeds_range = []
seeds_range = [(start, start + length - 1) for start, length in zip(seeds[::2], seeds[1::2])]
locations_range = find_locations_range(seeds_range, maps)
print(min(min(locations_range)))
