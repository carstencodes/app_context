#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of app_context
# (see https://github.com/carstencodes/app_context).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

import unittest

import app_context


class BasicTest(unittest.TestCase):
    def test_item_exists(self) -> None:
        var = app_context.create_application_environment()
        self.assertIsNotNone(var)

    def test_item_is_of_correct_type(self) -> None:
        var = app_context.create_application_environment()
        self.assertTrue(isinstance(var, app_context.ApplicationEnvironment))


if __name__ == "__main__":
    unittest.main()
