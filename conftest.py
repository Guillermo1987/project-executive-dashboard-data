"""Deja importar los modulos del repositorio desde tests/.

Viven en la raiz y no forman paquete, asi que sin esto `import scanner` falla
segun desde donde se lance pytest.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()))
