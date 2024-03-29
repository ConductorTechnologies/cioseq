""" test sequence

   isort:skip_file
"""
import os
import sys
import unittest
from unittest.mock import patch

# SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
# if SRC not in sys.path:
#     sys.path.insert(0, SRC)

from cioseq.sequence import Progression, Sequence, _resolve_frames


class ResolveFramesTest(unittest.TestCase):
    def test_single_integer(self):
        s = _resolve_frames(1)
        self.assertEqual(s[0], 1)
        self.assertEqual(len(s), 1)

    def test_integer_range_args(self):
        s = _resolve_frames(1, 5)
        self.assertEqual(s[0], 1)
        self.assertEqual(s[4], 5)
        self.assertEqual(len(s), 5)

    def test_integer_range_step_args(self):
        s = _resolve_frames(1, 5, 2)
        self.assertEqual(s[0], 1)
        self.assertEqual(s[2], 5)
        self.assertEqual(len(s), 3)

    def test_sort_integer_range_step_args(self):
        s = _resolve_frames(5, 1, 2)
        self.assertEqual(s[0], 1)
        self.assertEqual(s[2], 5)
        self.assertEqual(len(s), 3)

    def test_negative_integer_args(self):
        s = _resolve_frames(-5, -1, 2)
        self.assertEqual(s[0], -5)
        self.assertEqual(s[2], -1)
        self.assertEqual(len(s), 3)

    def test_array(self):
        s = _resolve_frames([1, 2, 6, 4])
        self.assertEqual(s[0], 1)
        self.assertEqual(s[2], 4)
        self.assertEqual(len(s), 4)

    def test_single_number_spec(self):
        s = _resolve_frames("3")
        self.assertEqual(s[0], 3)
        self.assertEqual(len(s), 1)

    def test_range_spec(self):
        s = _resolve_frames("1-3")
        self.assertEqual(s[0], 1)
        self.assertEqual(len(s), 3)

    def test_range_step_spec(self):
        s = _resolve_frames("1-5x2")
        self.assertEqual(s[0], 1)
        self.assertEqual(s[2], 5)
        self.assertEqual(len(s), 3)


class SequenceFactoryTest(unittest.TestCase):
    def test_single_number_is_progression(self):
        s = Sequence.create(1)
        self.assertIsInstance(s, Progression)

    def test_range_is_progression(self):
        s = Sequence.create(1, 10)
        self.assertIsInstance(s, Progression)

    def test_range_step_is_progression(self):
        s = Sequence.create(1, 10, 2)
        self.assertIsInstance(s, Progression)

    def test_single_number_string_is_progression(self):
        s = Sequence.create("1")
        self.assertIsInstance(s, Progression)

    def test_range_string_is_progression(self):
        s = Sequence.create("1-10x2")
        self.assertIsInstance(s, Progression)

    def test_frame_spec_is_not_progression(self):
        s = Sequence.create("1-10, 14, 20-50x4")
        self.assertIsInstance(s, Sequence)
        self.assertNotIsInstance(s, Progression)

    def test_list_sequence_is_not_progression(self):
        s = Sequence.create([1, 3, 4, 6, 8, 9])
        self.assertIsInstance(s, Sequence)
        self.assertNotIsInstance(s, Progression)

    def test_progressive_list_is_progression(self):
        s = Sequence.create([1, 3, 5, 7, 9])
        self.assertIsInstance(s, Progression)

    def test_is_progression_method(self):
        s = Sequence.create([1, 3, 5, 7, 9])
        self.assertTrue(s.is_progression())
        s = Sequence.create([1, 3, 5, 7, 9, 10])
        self.assertFalse(s.is_progression())


class SequenceFactoryFailTest(unittest.TestCase):
    def test_negative_step(self):
        with self.assertRaises(ValueError):
            Sequence.create(1, 10, -1)

    def test_bad_spec(self):
        with self.assertRaises(ValueError):
            Sequence.create("f")

    def test_bad_spec_step(self):
        with self.assertRaises(ValueError):
            Sequence.create("1-10xf")

    def test_try_to_bypass_factory(self):
        with self.assertRaises(TypeError):
            Sequence("1-10xf")

    def test_try_to_bypass_factory_with_correct_number_of_args(self):
        with self.assertRaises(AssertionError):
            Sequence(object(), "1-10xf")


class StartEndStepIntsTest(unittest.TestCase):
    def test_create_from_start_only(self):
        s = Sequence.create(1)
        self.assertEqual(s.start, 1)
        self.assertEqual(s.end, 1)
        self.assertEqual(s.step, 1)

    def test_create_from_start_end_ints(self):
        s = Sequence.create(1, 5)
        self.assertEqual(s.start, 1)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 1)

    def test_create_with_step_ints(self):
        s = Sequence.create(1, 5, 2)
        self.assertEqual(s.start, 1)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 2)

    def test_create_with_negative_start(self):
        s = Sequence.create(-1, 5, 2)
        self.assertEqual(s.start, -1)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 2)

    def test_create_with_negative_start_end(self):
        s = Sequence.create(-5, -1, 2)
        self.assertEqual(s.start, -5)
        self.assertEqual(s.end, -1)
        self.assertEqual(s.step, 2)

    def test_create_swap_negative_start_end(self):
        s = Sequence.create(-1, -5, 2)
        self.assertEqual(s.start, -5)
        self.assertEqual(s.end, -1)
        self.assertEqual(s.step, 2)


class StartEndStepSpecTest(unittest.TestCase):
    def test_create_from_start_end_spec(self):
        s = Sequence.create("1-5")
        self.assertEqual(s.start, 1)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 1)

    def test_create_from_start_end_spec_backwards(self):
        s = Sequence.create("5-1")
        self.assertEqual(s.start, 1)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 1)

    def test_create_with_step_spec(self):
        s = Sequence.create("1-5x2")
        self.assertEqual(s.start, 1)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 2)

    def test_create_with_start_spec(self):
        s = Sequence.create("5")
        self.assertEqual(s.start, 5)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 1)

    def test_create_with_negative_start(self):
        s = Sequence.create("-1-5x2")
        self.assertEqual(s.start, -1)
        self.assertEqual(s.end, 5)
        self.assertEqual(s.step, 2)

    def test_create_with_negative_start_end(self):
        s = Sequence.create("-5--1x2")
        self.assertEqual(s.start, -5)
        self.assertEqual(s.end, -1)
        self.assertEqual(s.step, 2)

    def test_create_swap_negative_start_end(self):
        s = Sequence.create("-1--5x2")
        self.assertEqual(s.start, -5)
        self.assertEqual(s.end, -1)
        self.assertEqual(s.step, 2)


class SequenceToStringTest(unittest.TestCase):
    def test_progression_range_step_round_down(self):
        s = Sequence.create(0, 10, 3)
        self.assertEqual(str(s), "0-9x3")

    def test_sequence(self):
        s = Sequence.create("1-10, 14, 20-48x4")
        self.assertEqual(str(s), "1-10,14,20-48x4")

    def test_repr_from_progression(self):
        s = Sequence.create(0, 10, 3)
        self.assertEqual(repr(s), "Sequence.create('0-9x3')")

    def test_repr_from_sequence(self):
        s = Sequence.create("1-10, 14, 20-48x4")
        self.assertEqual(repr(s), "Sequence.create('1-10,14,20-48x4')")


class ChunksTest(unittest.TestCase):
    def test_no_chunk_size(self):
        s = Sequence.create("1-100")
        self.assertEqual(s.chunk_size, 100)

    def test_clamp_chunk_size(self):
        s = Sequence.create("1-100", chunk_size=200)
        self.assertEqual(s.chunk_size, 100)

    def test_chunk_size(self):
        s = Sequence.create("1-100", chunk_size=50)
        self.assertEqual(s.chunk_size, 50)

    def test_chunk_size_setter(self):
        s = Sequence.create("1-100")
        s.chunk_size = 50
        self.assertEqual(s.chunk_size, 50)

    def test_best_chunk_size(self):
        s = Sequence.create("1-100")
        s.chunk_size = 76
        self.assertEqual(s.best_chunk_size(), 50)
        s.chunk_size = 37
        self.assertEqual(s.best_chunk_size(), 34)
        s.chunk_size = 100
        self.assertEqual(s.best_chunk_size(), 100)

    def test_create_chunks_linear(self):
        s = Sequence.create("1-100")
        s.chunk_size = 10
        chunks = s.chunks()
        self.assertEqual(list(chunks[0]), list(range(1, 11)))

    def test_create_chunks_cycle(self):
        s = Sequence.create("1-100")
        s.chunk_size = 10
        s.chunk_strategy = "cycle"
        chunks = s.chunks()
        self.assertEqual(list(chunks[0]), list(range(1, 100, 10)))
        s.chunk_size = 7
        chunks = s.chunks()
        self.assertEqual(list(chunks[0]), list(range(1, 100, 15)))

    def test_cycle_chunks_same_as_cycle_progressions_if_input_progression(self):
        s = Sequence.create("1-100")
        s.chunk_size = 10
        s.chunk_strategy = "cycle"
        c_chunks = s.chunks()
        s.chunk_strategy = "cycle_progressions"
        cp_chunks = s.chunks()
        self.assertEqual(list(c_chunks[0]), list(cp_chunks[0]))

    def test_cycle_progression_chunks_are_progressions(self):
        s = Sequence.create("1-1001x3,135-149x2,379,454")
        s.chunk_size = 10
        s.chunk_strategy = "cycle_progressions"
        for chunk in s.chunks():
            self.assertIsInstance(chunk, Progression)

    def test_chunk_count(self):
        s = Sequence.create("1-100")
        s.chunk_size = 7
        self.assertEqual(s.chunk_count(), 15)
        s.chunk_size = 15
        self.assertEqual(s.chunk_count(), 7)
        s.chunk_size = 10
        self.assertEqual(s.chunk_count(), 10)

    def test_progression_count_with_chunk_size(self):
        s = Sequence.create("1-3,6-12x2,13,14-36x3")
        s.chunk_size = 4
        s.chunk_strategy = "progressions"
        self.assertEqual(s.chunk_count(), 5)

    def test_progression_count_without_chunk_size(self):
        s = Sequence.create("1-3,6-12x2,13,14-36x3")
        s.chunk_size = -1
        s.chunk_strategy = "progressions"
        self.assertEqual(s.chunk_count(), 4)

    def test_progression_count_all_progressions(self):
        s = Sequence.create("1-3,6-12x2,13,14-36x3")
        s.chunk_size = -1
        s.chunk_strategy = "progressions"
        for chunk in s.chunks():
            self.assertIsInstance(chunk, Progression)
            
    def test_cap_chunk_count_even(self):
        s = Sequence.create("1-100")
        s.chunk_size = 10
        s.cap_chunk_count(4)
        self.assertEqual(s.chunk_count(), 4)
        self.assertEqual(s.chunk_size, 25)

    def test_cap_chunk_count_with_remainder(self):
        s = Sequence.create("1-100")
        s.chunk_size = 10
        s.cap_chunk_count(3)
        self.assertEqual(s.chunk_count(), 3)
        self.assertEqual(s.chunk_size, 34)
        
    def test_doesnt_cap_chunk_count_when_not_exceded(self):
        s = Sequence.create("1-100")
        s.chunk_size = 3
        s.cap_chunk_count(50)
        self.assertEqual(s.chunk_count(), 34)
        self.assertEqual(s.chunk_size, 3)

class IntersectionTest(unittest.TestCase):
    def test_does_intersect(self):
        s = Sequence.create("1-10")
        i = s.intersection(range(5, 15))
        self.assertEqual(list(i), list(range(5, 11)))

    def test_does_not_intersect(self):
        s = Sequence.create("1-10")
        i = s.intersection(range(25, 35))
        self.assertEqual(i, None)


class UnionTest(unittest.TestCase):
    def test_creates_union_from_range(self):
        s = Sequence.create("1-10")
        u = s.union(range(5, 15))
        self.assertEqual(list(u), list(range(1, 15)))

    def test_creates_union_from_other_sequence(self):
        s1 = Sequence.create("1-10")
        s2 = Sequence.create("5-15")
        u = s1.union(s2)
        self.assertEqual(list(u), list(Sequence.create("1-15")))


class DifferenceTest(unittest.TestCase):
    def test_removes_sequence_from_other_sequence(self):
        s1 = Sequence.create("1-10")
        s2 = Sequence.create("5-15")
        d = s1.difference(s2)
        self.assertEqual(list(d), list(Sequence.create("1-4")))

    def test_return_none_if_no_frames(self):
        s1 = Sequence.create("1-10")
        s2 = Sequence.create("1-12")
        d = s1.difference(s2)
        self.assertIsNone(d)

    def test_return_unchanged_if_nothing_changed(self):
        s1 = Sequence.create("1-10")
        s2 = Sequence.create("12-15")
        d = s1.difference(s2)
        self.assertEqual(list(d), list(s1))

    def test_return_new_object_if_nothing_changed(self):
        s1 = Sequence.create("1-10")
        s2 = Sequence.create("12-15")
        d = s1.difference(s2)
        self.assertIsNot(d, s1)


class ChunkIntersectionTest(unittest.TestCase):
    def test_intersecting_chunks(self):
        s = Sequence.create("1-50", chunk_size=5)
        rhs = Sequence.create("1,2,7")
        result = s.intersecting_chunks(rhs)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result[0]), [1, 2, 3, 4, 5])

    def test_intersecting_chunks_when_excess(self):
        s = Sequence.create("1-50", chunk_size=5)
        rhs = Sequence.create("1,2,7,52")
        result = s.intersecting_chunks(rhs)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result[0]), [1, 2, 3, 4, 5])

    def test_intersecting_chunks_when_none(self):
        s = Sequence.create("1-50", chunk_size=5)
        rhs = Sequence.create("52-60")
        result = s.intersecting_chunks(rhs)
        self.assertEqual(len(result), 0)

    def test_intersecting_chunks_when_negative(self):
        s = Sequence.create("-1--50", chunk_size=5)
        rhs = Sequence.create("-1,-2,-7,-52")
        result = s.intersecting_chunks(rhs)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result[0]), [-10, -9, -8, -7, -6])


class SequenceIteratorTest(unittest.TestCase):
    def test_iterator_sorted_no_dups(self):
        s = Sequence.create("1-10, 8-20x2, 19, 17")
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 17, 18, 19, 20]
        self.assertEqual(list(s), expected)


class ProgressionsTest(unittest.TestCase):
    def test_empty(self):
        result = Progression.factory([])
        self.assertEqual(result, [])

    def test_single(self):
        result = Progression.factory([3])
        self.assertEqual(len(result), 1)
        self.assertEqual(str(result[0]), "3")

    def test_two(self):
        result = Progression.factory([3, 7])
        self.assertEqual(len(result), 1)
        self.assertEqual(str(result[0]), "3-7x4")

    def test_progression_at_start(self):
        result = Progression.factory([3, 5, 7, 10, 15])
        self.assertEqual(len(result), 2)
        self.assertEqual(str(result[0]), "3-7x2")

    def test_progression_at_end(self):
        result = Progression.factory([3, 5, 8, 10, 12])
        self.assertEqual(str(result[1]), "8-12x2")

    def test_order(self):
        numbers = [3, 5, 8, 10, 12]
        numbers.reverse()
        result = Progression.factory(numbers)
        self.assertEqual(str(result[0]), "3-5x2")
        self.assertEqual(str(result[1]), "8-12x2")

    def test_from_range(self):
        result = Progression.factory(range(2, 97, 3))
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 32)

    def test_range_max_size_one(self):
        result = Progression.factory([2, 4, 6, 8, 10], max_size=1)
        self.assertEqual(len(result), 5)

    def test_range_max_2(self):
        result = Progression.factory([2, 4, 6, 8, 10], max_size=2)
        self.assertEqual(len(result), 3)

    def test_range_max_16(self):
        result = Progression.factory(range(2, 197, 3), max_size=16)
        self.assertEqual(len(result[0]), 16)
        self.assertEqual(len(result), 5)

    def test_seq_to_longest_progressions(self):
        s = Sequence.create("1-10, 14, 20-48x4")
        progs = Progression.factory(s)
        self.assertEqual(len(progs), 3)

    def test_seq_to_limited_length_progressions(self):
        s = Sequence.create("1-10, 14, 20-48x4")
        progs = Progression.factory(s, max_size=4)
        self.assertEqual(len(progs), 6)


class PermutationsTest(unittest.TestCase):
    def test_one_substitution(self):
        template = "image.%(frame)04d.tif"
        result = list(Sequence.permutations(template, frame="0-20x2"))
        self.assertIn("image.0008.tif", result)
        self.assertIn("image.0012.tif", result)
        self.assertEqual(len(result), 11)

    def test_two_the_same_substitution(self):
        template = "/path/%(frame)d/image.%(frame)04d.tif"
        result = list(Sequence.permutations(template, frame="0-20x2"))
        self.assertIn("/path/8/image.0008.tif", result)
        self.assertIn("/path/12/image.0012.tif", result)
        self.assertEqual(len(result), 11)

    def test_three_substitutions(self):
        template = "image_%(uval)02d_%(vval)02d.%(frame)04d.tif"
        kw = {"uval": "1-2", "vval": "1-2", "frame": "10-11"}
        result = list(Sequence.permutations(template, **kw))
        self.assertIn("image_01_01.0010.tif", result)
        self.assertIn("image_02_02.0011.tif", result)
        self.assertIn("image_02_01.0010.tif", result)
        self.assertEqual(len(result), 8)


class OffsetTest(unittest.TestCase):
    def test_offset_positive_value(self):
        s = Sequence.create("1-10")
        s = s.offset(5)
        self.assertEqual(list(s), list(range(6, 16)))

    def test_offset_negative_value(self):
        s = Sequence.create("11-20")
        s = s.offset(-5)
        self.assertEqual(list(s), list(range(6, 16)))

    def test_negative_result_offset(self):
        s = Sequence.create("1-10")
        s = s.offset(-3)
        self.assertEqual(list(s), list(range(-2, 8)))

    def test_offset_sequence_has_same_chunk_size(self):
        s = Sequence.create("1-10", chunk_size=3)
        o = s.offset(5)
        self.assertEqual(o.chunk_size, s.chunk_size)

    def test_offset_sequence_has_same_chunk_strategy(self):
        s = Sequence.create("1-10", chunk_strategy="cycle")
        o = s.offset(5)
        self.assertEqual(o.chunk_strategy, s.chunk_strategy)


class ExpandFilenameTest(unittest.TestCase):
    def test_expand_result_same_length(self):
        s = Sequence.create("8-12")
        template = "image.#.exr"
        result = s.expand(template)
        self.assertEqual(len(result), 5)

    def test_expand_single_hash(self):
        s = Sequence.create("8-12")
        template = "image.#.exr"
        result = s.expand(template)
        self.assertIn("image.8.exr", result)
        self.assertIn("image.12.exr", result)

    def test_expand_padded_hash(self):
        s = Sequence.create("8-12")
        template = "image.#####.exr"
        result = s.expand(template)
        self.assertIn("image.00008.exr", result)
        self.assertIn("image.00012.exr", result)

    def test_expand_many_captures(self):
        s = Sequence.create("8-12")
        template = "/some/directory_###/image.#####.exr"
        result = s.expand(template)
        self.assertIn("/some/directory_012/image.00012.exr", result)
        self.assertIn("/some/directory_008/image.00008.exr", result)

    def test_invalid_template_raises(self):
        s = Sequence.create("8-12")
        template = "image.26.exr"
        with self.assertRaises(ValueError):
            s.expand(template)


class ResolveDollarTimeVarsTest(unittest.TestCase):
    def test_resolve_one_file_no_padding(self):
        s = Sequence.create("1")
        template = "image.$F.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.1.exr")

    def test_resolve_no_match_leaves_untouched(self):
        s = Sequence.create("1")
        template = "image.ho.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.ho.exr")

    def test_resolve_many_matches(self):
        s = Sequence.create("1")
        template = "image.$F.$5F.$2F.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.1.00001.01.exr")

    def test_resolve_one_template_to_many_filenames(self):
        s = Sequence.create("1-5")
        template = "image.$2F.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 5)
        self.assertIn("image.02.exr", result)
        self.assertIn("image.05.exr", result)

    def test_resolve_many_templates_to_many_filenames(self):
        s = Sequence.create("1-3")
        templates = [
            "/folder_1/image.$2F.exr",
            "/folder_2/image.$2F.exr",
            "/folder_3/image.$2F.exr",
        ]
        result = s.expand_dollar_f(*templates)
        self.assertEqual(len(result), 3)
        self.assertIn("/folder_2/image.02.exr", result)
        self.assertIn("/folder_3/image.03.exr", result)

    def test_resolve_number_after_f(self):
        s = Sequence.create("1")
        template = "image.$F.$F5.$F2.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.1.00001.01.exr")

    def test_resolve_lowercase_f(self):
        s = Sequence.create("1")
        template = "image.$f.$f5.$f2.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.1.00001.01.exr")


class ResolveFormatTest(unittest.TestCase):
    def test_resolve_one_file_no_padding(self):
        s = Sequence.create("1")
        template = "image.{frame}.exr"
        result = s.expand_format(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.1.exr")

    def test_resolve_no_match_leaves_untouched(self):
        s = Sequence.create("1")
        template = "image.ho.exr"
        result = s.expand_format(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.ho.exr")

    def test_resolve_many_matches(self):
        s = Sequence.create("1")
        template = "image.{frame}.{frame:05d}.{frame:02d}.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "image.1.00001.01.exr")

    def test_resolve_one_template_to_many_filenames(self):
        s = Sequence.create("1-5")
        template = "image.{frame:02d}.exr"
        result = s.expand_dollar_f(template)
        self.assertEqual(len(result), 5)
        self.assertIn("image.02.exr", result)
        self.assertIn("image.05.exr", result)

    def test_resolve_many_templates_to_many_filenames(self):
        s = Sequence.create("1-3")
        templates = [
            "/folder_1/image.{frame:02d}.exr",
            "/folder_2/image.{frame:02d}.exr",
            "/folder_3/image.{frame:02d}.exr",
        ]
        result = s.expand_dollar_f(*templates)
        self.assertEqual(len(result), 3)
        self.assertIn("/folder_2/image.02.exr", result)
        self.assertIn("/folder_3/image.03.exr", result)


class ToCustomSpecTest(unittest.TestCase):
    def test_spec_single_number(self):
        s = Sequence.create(10)
        self.assertEqual(s.to(":", "%", ";"), "10")

    def test_spec_range(self):
        s = Sequence.create(0, 10)
        self.assertEqual(s.to(":", "%", ";"), "0:10")

    def test_spec_step_range(self):
        s = Sequence.create(1, 9, 2)
        self.assertEqual(s.to(":", "%", ";"), "1:9%2")

    def test_spec_complex(self):
        s = Sequence.create("1-10, 14, 20-48x4")
        self.assertEqual(s.to(":", "%", ";"), "1:10;14;20:48%4")

    def test_complex_add_spaces(self):
        s = Sequence.create("1-10, 14, 20-48x4")
        self.assertEqual(s.to(":", "%", "; "), "1:10; 14; 20:48%4")

    def test_no_step(self):
        s = Sequence.create("1-4, 6-10x2, 20-28x4")
        self.assertEqual(s.to("-", "", ","), "1-4,6,8,10,20,24,28")


class SubsampleTest(unittest.TestCase):
    def test_counts_from_1_to_10(self):
        s = Sequence.create("1-10")
        ss = s.subsample(1)
        self.assertEqual(len(ss), 1)
        self.assertEqual(list(ss), [6])
        ss = s.subsample(2)
        self.assertEqual(len(ss), 2)
        self.assertEqual(list(ss), [3, 8])
        ss = s.subsample(3)
        self.assertEqual(len(ss), 3)
        self.assertEqual(list(ss), [2, 6, 9])
        ss = s.subsample(4)
        self.assertEqual(len(ss), 4)
        self.assertEqual(list(ss), [2, 4, 7, 9])
        ss = s.subsample(5)
        self.assertEqual(len(ss), 5)
        self.assertEqual(list(ss), [2, 4, 6, 8, 10])
        ss = s.subsample(6)
        self.assertEqual(len(ss), 6)
        self.assertEqual(list(ss), [1, 3, 5, 6, 8, 10])
        ss = s.subsample(7)
        self.assertEqual(len(ss), 7)
        self.assertEqual(list(ss), [1, 3, 4, 6, 7, 8, 10])
        ss = s.subsample(8)
        self.assertEqual(len(ss), 8)
        self.assertEqual(list(ss), [1, 2, 4, 5, 6, 7, 9, 10])
        ss = s.subsample(9)
        self.assertEqual(len(ss), 9)
        self.assertEqual(list(ss), [1, 2, 3, 4, 6, 7, 8, 9, 10])
        ss = s.subsample(10)
        self.assertEqual(len(ss), 10)
        self.assertEqual(list(ss), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        ss = s.subsample(11)
        self.assertEqual(len(ss), 10)
        self.assertEqual(list(ss), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_step_sequence(self):
        s = Sequence.create("1-20x2")
        ss = s.subsample(1)
        self.assertEqual(len(ss), 1)
        self.assertEqual(list(ss), [11])
        ss = s.subsample(2)
        self.assertEqual(len(ss), 2)
        self.assertEqual(list(ss), [5, 15])
        ss = s.subsample(3)
        self.assertEqual(len(ss), 3)
        self.assertEqual(list(ss), [3, 11, 17])
        ss = s.subsample(4)
        self.assertEqual(len(ss), 4)
        self.assertEqual(list(ss), [3, 7, 13, 17])
        # test subsample full sequence
        ss = s.subsample(10)
        self.assertEqual(len(ss), 10)
        self.assertEqual(list(ss), list(range(1, 21, 2)))

    def test_irregular_sequence(self):
        s = Sequence.create("1-5, 9-11x2,25-100x20")
        ss = s.subsample(1)
        self.assertEqual(len(ss), 1)
        self.assertEqual(list(ss), [9])
        ss = s.subsample(2)
        self.assertEqual(len(ss), 2)
        self.assertEqual(list(ss), [3, 45])
        ss = s.subsample(3)
        self.assertEqual(len(ss), 3)
        self.assertEqual(list(ss), [2, 9, 65])
        ss = s.subsample(4)
        self.assertEqual(len(ss), 4)
        self.assertEqual(list(ss), [2, 5, 11, 65])
        # test subsample full sequence
        ss = s.subsample(11)
        self.assertEqual(len(ss), 11)
        self.assertEqual(list(ss), list(s))


class CalcFMLTest(unittest.TestCase):
    def test_counts_from_1_to_100(self):
        s = Sequence.create("1-100")
        ss = s.calc_fml(3)
        self.assertEqual(len(ss), 3)
        self.assertEqual(list(ss), [1, 51, 100])
        ss = s.calc_fml(-1)
        self.assertEqual(len(ss), 1)
        self.assertEqual(list(ss), [1])
        ss = s.calc_fml(200)
        self.assertEqual(len(ss), 100)
        self.assertEqual(list(ss), list(s))

    def test_irregular_sequence(self):
        s = Sequence.create("1,2,7,8,10,100")
        ss = s.calc_fml(3)
        self.assertEqual(len(ss), 3)
        self.assertEqual(list(ss), [1, 8, 100])

        ss = s.calc_fml(4)
        self.assertEqual(len(ss), 4)
        self.assertEqual(list(ss), [1, 7, 10, 100])
        # [1, 2, 3, 4, 5, 9, 11, 25, 45, 65, 85]
        s = Sequence.create("1-5, 9-11x2,25-100x20")
        ss = s.calc_fml(1)
        self.assertEqual(len(ss), 1)
        self.assertEqual(list(ss), [1])
        ss = s.calc_fml(2)
        self.assertEqual(len(ss), 2)
        self.assertEqual(list(ss), [1, 85])
        ss = s.calc_fml(3)
        self.assertEqual(len(ss), 3)
        self.assertEqual(list(ss), [1, 9, 85])
        ss = s.calc_fml(4)
        self.assertEqual(len(ss), 4)
        self.assertEqual(list(ss), [1, 4, 11, 85])
        # test subsample full sequence
        ss = s.calc_fml(11)
        self.assertEqual(len(ss), 11)
        self.assertEqual(list(ss), list(s))


class IndexingTest(unittest.TestCase):
    def test_spec_single_number(self):
        s = Sequence.create("1-10x2")
        self.assertEqual(s[0], 1)

    def test_spec_range(self):
        s = Sequence.create("1-10x2")
        self.assertEqual(s[-1], 9)


class CreateFromFilenames(unittest.TestCase):
    @patch("cioseq.sequence.glob")
    def test_basic(self, mock_glob):
        filenames = ["image.0001.exr", "image.0002.exr", "image.0003.exr"]
        mock_glob.return_value = filenames
        s = Sequence.create(prefix="image.", extension=".exr")
        self.assertEqual(list(s), [1, 2, 3])

    @patch("cioseq.sequence.glob")
    def test_when_other_files_exist(self, mock_glob):
        filenames = [
            "image.0001.exr",
            "image.0002.exr",
            "image.0003.exr",
            "image2.0004.exr",
        ]
        mock_glob.return_value = filenames
        s = Sequence.create(prefix="image.", extension=".exr")
        self.assertEqual(list(s), [1, 2, 3])

    @patch("cioseq.sequence.glob")
    def test_raises_when_no_files_exist(self, mock_glob):
        mock_glob.return_value = []
        with self.assertRaises(ValueError):
            s = Sequence.create(prefix="image.", extension=".exr")

    @patch("cioseq.sequence.glob")
    def test_raises_if_no_files_with_a_number(self, mock_glob):
        mock_glob.return_value = ["image.exr", "foo.exr", "bar.exr", "yum.exr"]
        with self.assertRaises(ValueError):
            s = Sequence.create(prefix="image.", extension=".exr")

    @patch("cioseq.sequence.glob")
    def test_no_prefix(self, mock_glob):
        mock_glob.return_value = ["001.exr", "002.exr", "003.exr", "yum.exr"]
        s = Sequence.create(prefix="", extension=".exr")
        self.assertEqual(list(s), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
