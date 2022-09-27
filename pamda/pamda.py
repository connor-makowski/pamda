from pamda.pamda_utils import pamda_utils
from pamda.pamda_core import pamda_core
import type_enforced


@type_enforced.Enforcer
class pamda(pamda_core, pamda_utils):
    pass
