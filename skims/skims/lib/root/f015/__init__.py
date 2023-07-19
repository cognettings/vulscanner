from lib.root.f015.c_sharp import (
    c_sharp_insecure_authentication,
)
from lib.root.f015.java import (
    java_basic_authentication,
    java_insecure_authentication,
)
from lib.root.f015.python import (
    python_danger_basic_auth,
)
from lib.root.f015.terraform import (
    tfm_azure_linux_vm_insecure_authentication,
    tfm_azure_virtual_machine_insecure_authentication,
)

__all__ = [
    "c_sharp_insecure_authentication",
    "java_basic_authentication",
    "java_insecure_authentication",
    "python_danger_basic_auth",
    "tfm_azure_linux_vm_insecure_authentication",
    "tfm_azure_virtual_machine_insecure_authentication",
]
