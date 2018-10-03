# encoding: utf-8
"""RoCo: Rooot conversion package, reading and writing various root system files
"""

#-----------------------------------------------------------------------------
#  Copyright (C) 2018 Daniel Leitner

#  Distributed under the terms of the GNU General Public License. You should
#  have received a copy of the license along with this program. If not,
#  see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------

__version__ = '1'

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Reader
from python.roco.vtk_tools import read_vtp
from python.roco.rootsys import read_rootsys

# Writer
from python.roco.vtk_tools import write_rsml
from python.roco.vtk_tools import write_vtp
from python.roco.vtk_tools import write_dgf
from python.roco.vtk_tools import write_msh

# Helper
from python.roco.rsml import Metadata

