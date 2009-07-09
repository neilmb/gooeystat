# Copyright (C) 2008, 2009  Spencer Herzberg <spencer.herzberg@gmail.com>

# This file is part of GooeyStat

# GooeyStat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

def debug_on():
    logging.getLogger('').setLevel(logging.DEBUG)

def debug_off():
    logging.getLogger('').setLevel(logging.WARNING)

def mutter(msg, *args, **kwargs):
    """Note a small piece of information.

    In debug mode, this function will print the given message.  Otherwise,
    this function does nothing.
    """
    logging.debug(msg, *args, **kwargs)

