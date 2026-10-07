"""Synthetic header regression fixtures; no third-party APK bytes required."""
import struct
import unittest

from dexutil import Dex, OFFSETS


def header_fixture(table=None, count=0, offset=0, size=256):
    data = bytearray(size)
    data[:8] = b"dex\n035\0"
    struct.pack_into("<I", data, OFFSETS["file_size"], size)
    struct.pack_into("<I", data, OFFSETS["header_size"], 112)
    if table:
        struct.pack_into("<I", data, OFFSETS[table + "_size"], count)
        struct.pack_into("<I", data, OFFSETS[table + "_off"], offset)
    return Dex(bytes(data))


class HeaderTableTests(unittest.TestCase):
    TABLES = {"string_ids": 4, "type_ids": 4, "proto_ids": 12,
              "field_ids": 8, "method_ids": 8, "class_defs": 32}

    def test_empty_tables_allow_zero_offsets(self):
        self.assertEqual([], header_fixture().check())

    def test_empty_table_rejects_nonzero_offset(self):
        for table in self.TABLES:
            with self.subTest(table=table):
                self.assertTrue(header_fixture(table, 0, 112).check())

    def test_populated_table_requires_nonzero_offset_after_header(self):
        for table in self.TABLES:
            for offset in (0, 108, 256):
                with self.subTest(table=table, offset=offset):
                    self.assertTrue(header_fixture(table, 1, offset).check())

    def test_complete_span_must_fit(self):
        for table, stride in self.TABLES.items():
            with self.subTest(table=table):
                self.assertEqual([], header_fixture(table, 2, 256 - 2 * stride).check())
                self.assertTrue(header_fixture(table, 3, 256 - 2 * stride).check())

    def test_declared_file_size_still_checked(self):
        dex = header_fixture()
        dex.header["file_size"] -= 1
        self.assertTrue(dex.check())


if __name__ == "__main__":
    unittest.main()
