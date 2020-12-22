#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of pip-licenses-reader
# (see https://github.com/carstencodes/pip-licenses-reader).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

import unittest

import appenv


class BasicTest(unittest.TestCase):
    def test_item_exists(self) -> None:
        var = appenv.create_application_environment()
        self.assertIsNotNone(var)

    def test_item_is_of_correct_type(self) -> None:
        var = appenv.create_application_environment()
        self.assertTrue(isinstance(var, appenv.ApplicationEnvironment))


if __name__ == "__main__":
    unittest.main()
