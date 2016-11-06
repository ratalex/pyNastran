"""tests the pyNastran solver"""
from __future__ import print_function, unicode_literals
import os
import unittest

import pyNastran
from pyNastran.bdf.test.test_bdf import run_and_compare_fems
from pyNastran.bdf.dev_vectorized.bdf import read_bdf as read_bdfv
from pyNastran.bdf.bdf import read_bdf
#from pyNastran.utils.log import SimpleLogger
#from pyNastran.bdf.dev_vectorized.solver.solver import Solver

pkg_path = pyNastran.__path__[0]
test_path = os.path.join(pkg_path, '..', 'models')
#log = SimpleLogger('warning', encoding='utf8')

class TestReadWriteVectorized(unittest.TestCase):
    """tests the pyNastran solver"""

    def test_solid_bending(self):
        """vectorized vs. standard test on solid_bending.bdf"""
        bdf_filename = os.path.join(test_path, 'solid_bending', 'solid_bending.bdf')
        bdf_filename_out = os.path.join(test_path, 'solid_bending', 'solid_bending2.bdf')

        vmodel = read_bdfv(bdf_filename)
        vmodel.write_bdf(bdf_filename_out)
        run_and_compare_fems(
            bdf_filename, bdf_filename_out, debug=False, xref=True, check=True,
            punch=False, cid=None, mesh_form=None,
            print_stats=False, encoding=None,
            sum_load=False, size=8, is_double=False,
            stop=False, nastran='', post=-1, dynamic_vars=None,
            quiet=False, dumplines=False, dictsort=False,
            nerrors=0, dev=False, crash_cards=None,
        )
        os.remove(bdf_filename_out)

    def test_bwb(self):
        """vectorized vs. standard test on BWB_saero.bdf"""
        bdf_filename = os.path.join(test_path, 'bwb', 'BWB_saero.bdf')
        bdf_filename_out = os.path.join(test_path, 'bwb', 'BWB_saero2.bdf')

        vmodel = read_bdfv(bdf_filename)
        vmodel.write_bdf(bdf_filename_out)
        run_and_compare_fems(
            bdf_filename, bdf_filename_out, debug=False, xref=True, check=True,
            punch=False, cid=None, mesh_form='combined',
            print_stats=False, encoding=None,
            sum_load=False, size=8, is_double=False,
            stop=False, nastran='', post=-1, dynamic_vars=None,
            quiet=False, dumplines=False, dictsort=False,
            nerrors=0, dev=False, crash_cards=None,
        )
        os.remove(bdf_filename_out)

    def test_isat_01(self):
        """vectorized vs. standard test on ISat_Dploy_Sm.dat"""
        bdf_filename = os.path.join(test_path, 'iSat', 'ISat_Dploy_Sm.dat')
        bdf_filename_out = os.path.join(test_path, 'iSat', 'ISat_Dploy_Sm2.dat')

        vmodel = read_bdfv(bdf_filename)
        vmodel.write_bdf(bdf_filename_out)
        run_and_compare_fems(
            bdf_filename, bdf_filename_out, debug=False, xref=True, check=True,
            punch=False, cid=None, mesh_form=None,
            print_stats=False, encoding=None,
            sum_load=False, size=8, is_double=False,
            stop=False, nastran='', post=-1, dynamic_vars=None,
            quiet=False, dumplines=False, dictsort=False,
            nerrors=0, dev=False, crash_cards=None,
        )
        os.remove(bdf_filename_out)

    def test_isat_02(self):
        """vectorized vs. standard test on ISat_Launch_Sm_4pt.dat"""
        bdf_filename = os.path.join(test_path, 'iSat', 'ISat_Launch_Sm_4pt.dat')
        bdf_filename_outv = os.path.join(test_path, 'iSat', 'ISat_Launch_Sm_4ptv.dat')
        bdf_filename_out = os.path.join(test_path, 'iSat', 'ISat_Launch_Sm_4pt2.dat')

        vmodel = read_bdfv(bdf_filename)
        vmodel.write_bdf(bdf_filename_outv)
        model = read_bdf(bdf_filename)
        model.write_bdf(bdf_filename_out)

        run_and_compare_fems(
            bdf_filename, bdf_filename_outv, debug=False, xref=True, check=True,
            punch=False, cid=None, mesh_form=None,
            print_stats=False, encoding=None,
            sum_load=False, size=8, is_double=False,
            stop=False, nastran='', post=-1, dynamic_vars=None,
            quiet=False, dumplines=False, dictsort=False,
            nerrors=0, dev=False, crash_cards=None,
        )
        os.remove(bdf_filename_out)

    def test_isat_03(self):
        """vectorized vs. standard test on ISat_Launch_Sm_Rgd.dat"""
        bdf_filename = os.path.join(test_path, 'iSat', 'ISat_Launch_Sm_Rgd.dat')
        #bdf_filename_outv = os.path.join(test_path, 'iSat', 'ISat_Launch_Sm_Rgdv.dat')
        bdf_filename_out = os.path.join(test_path, 'iSat', 'ISat_Launch_Sm_Rgd2.dat')

        vmodel = read_bdfv(bdf_filename)
        vmodel.write_bdf(bdf_filename_out)
        run_and_compare_fems(
            bdf_filename, bdf_filename_out, debug=False, xref=True, check=True,
            punch=False, cid=None, mesh_form=None,
            print_stats=False, encoding=None,
            sum_load=False, size=8, is_double=False,
            stop=False, nastran='', post=-1, dynamic_vars=None,
            quiet=False, dumplines=False, dictsort=False,
            nerrors=0, dev=False, crash_cards=None,
        )
        os.remove(bdf_filename_out)

    def test_isat_04(self):
        """vectorized vs. standard test on iSat_launch_100Hz.dat"""
        bdf_filename = os.path.join(test_path, 'iSat', 'iSat_launch_100Hz.dat')
        #bdf_filename_outv = os.path.join(test_path, 'iSat', 'ISat_Launch_Sm_Rgdv.dat')
        bdf_filename_out = os.path.join(test_path, 'iSat', 'iSat_launch_100Hz2.dat')

        vmodel = read_bdfv(bdf_filename)
        vmodel.write_bdf(bdf_filename_out)
        run_and_compare_fems(
            bdf_filename, bdf_filename_out, debug=False, xref=True, check=True,
            punch=False, cid=None, mesh_form=None,
            print_stats=False, encoding=None,
            sum_load=False, size=8, is_double=False,
            stop=False, nastran='', post=-1, dynamic_vars=None,
            quiet=False, dumplines=False, dictsort=False,
            nerrors=0, dev=False, crash_cards=None,
        )
        #os.remove(bdf_filename_out)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()