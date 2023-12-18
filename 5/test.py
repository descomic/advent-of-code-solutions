from ddt import ddt, data, unpack
import main
import unittest


@ddt
class Test(unittest.TestCase):
    @data((main.SEED_TO_SOIL_MAP, [[50, 98,  2], [52,  50,  48]]),
          (main.SOIL_TO_FERTILIZER_MAP, [
           [0, 15, 37], [37, 52, 2], [39, 0, 15]]),
          (main.FERTILIZER_TO_WATER_MAP, [
           [49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]]),
          (main.WATER_TO_LIGHT_MAP, [[88, 18, 7], [18, 25, 70]]),
          (main.LIGHT_TO_TEMPERATURE_MAP, [
           [45, 77, 23], [81, 45, 19], [68, 64, 13]]),
          (main.TEMPERATURE_TO_HUMIDITY_MAP, [[0, 69, 1], [1, 0, 69]]),
          (main.HUMIDITY_TO_LOCATION_MAP, [[60, 56, 37], [56, 93, 4]]))
    @unpack
    def test_read_map(self, title: str, expected_map: list[list[int]]):
        with open('5/example.txt', 'r') as file:
            example = file.read()
            map: list[list[int]] = main.read_map(example, title)
            self.assertEqual(expected_map, map)

    def test_get_value_from_map(self):
        seeds: list[tuple[int, int]] = [(55, 13), (79, 14)]

        seed_to_soil_map: list[list[int]] = [[50, 98, 2], [52, 50, 48]]
        soil_to_fertilizer_map: list[list[int]] = [
            [0, 15, 37], [37, 52, 2], [39, 0, 15]]
        fertilizer_to_water_map: list[list[int]] = [
            [49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]]
        water_to_light_map: list[list[int]] = [[88, 18, 7], [18, 25, 70]]
        light_to_temperature_map: list[list[int]] = [
            [45, 77, 23], [81, 45, 19], [68, 64, 13]]
        temperature_to_humidity_map: list[list[int]] = [[0, 69, 1], [1, 0, 69]]
        humidity_to_location_map: list[list[int]] = [[60, 56, 37], [56, 93, 4]]

        expected_soil: list[tuple[int, int]] = [(57, 13), (81, 14)]
        value: list[tuple[int, int]] = main.get_value_from_map(
            seed_to_soil_map, seeds)
        self.assertEqual(expected_soil, value)

        expected_fertilizer: list[tuple[int, int]] = [(57, 13), (81, 14)]
        value = main.get_value_from_map(soil_to_fertilizer_map, value)
        self.assertEqual(expected_fertilizer, value)

        expected_water: list[tuple[int, int]] = [
            (53, 4), (61, 9), (81, 14)
        ]
        value = main.get_value_from_map(fertilizer_to_water_map, value)
        self.assertEqual(expected_water, value)

        expected_light: list[tuple[int, int]] = [(46, 4), (54, 9), (74, 14)]
        value = main.get_value_from_map(water_to_light_map, value)
        self.assertEqual(expected_light, value)

        expected_temperature: list[tuple[int, int]] = [
            (45, 11), (78, 3), (82, 4), (90, 9)
        ]
        value = main.get_value_from_map(light_to_temperature_map, value)
        self.assertEqual(expected_temperature, value)

        expected_humidity: list[tuple[int, int]] = [
            (46, 11), (78, 3), (82, 4), (90, 9)
        ]
        value = main.get_value_from_map(temperature_to_humidity_map, value)
        self.assertEqual(expected_humidity, value)

        expected_location: list[tuple[int, int]] = [
            (46, 15), (82, 3), (86, 4), (94, 5)
        ]
        value = main.get_value_from_map(humidity_to_location_map, value)
        self.assertEqual(expected_location, value)

    def test_get_seeds(self):
        line: str = "seeds: 79 14 55 13"
        expected_seeds: list[tuple[int, int]] = [(79, 14), (55, 13)]
        self.assertEqual(expected_seeds, main.get_seeds(line))

    def test(self):
        with open('5/example.txt', 'r') as file:
            input = file.read()
            self.assertEqual(46, main.get_minimum_location(input))


if __name__ == '__main__':
    unittest.main()
