from opt.models import MotivationRole
from opt.models import BaseModule
from opt.models import KpiModule

from opt.models import EmployeeCalc
from opt.models import BaseModuleCalc
from opt.models import KpiModuleCalc


class AssemblyEmplCalc(object):
    """матрешка для сборки расчета по сотруднику"""
    ecObj = EmployeeCalc()
    bmc_Obj = BaseModuleCalc()
    kpimc_Obj = KpiModuleCalc()

    def __init__(self, emplCalc):
        ecObj = emplCalc
        bmc_Obj = ecObj.get_base_module_calc()
        kpimc_Obj = ecObj.get_kpi_module_calc()

    def build():
        pass
        
class AssemblyMotiveRole(object):
    """матрешка для сборки мотивационной роли"""
    mrObj = MotivationRole()
    bm_Obj = BaseModule()
    kpim_Obj = KpiModule()
    
    def __init__(self, motiveRole):
        mrObj = mrObj
        bm_Obj = ecObj.get_base_module()
        kpim_Obj = ecObj.get_kpi_module()
    
    def build():
        pass