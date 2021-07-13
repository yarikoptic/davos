from pathlib import PurePosixPath
from typing import (
    Any, 
    ClassVar, 
    Final, 
    Literal, 
    NoReturn, 
    Optional, 
    Protocol, 
    Union
)
from google.colab._shell import Shell                            # type: ignore
from IPython.core.interactiveshell import InteractiveShell       # type: ignore

__all__: list[Literal['DavosConfig']]

_Environment = Literal['Colaboratory', 'IPython<7.0', 'IPython>=7.0', 'Python']
IpythonShell = Union[InteractiveShell, Shell]

class IpyShowSyntaxErrorPre7(Protocol):
    def __call__(self, filename: Optional[str] = ...) -> None: ...
    
class IpyShowSyntaxErrorPost7(Protocol):
    def __call__(self, filename: Optional[str] = ..., running_compile_code: bool = ...) -> None: ...

class SingletonConfig(type):
    __instance: ClassVar[Optional[DavosConfig]]
    def __call__(cls, *args: Any, **kwargs: Any) -> DavosConfig: ...
    
class DavosConfig(metaclass=SingletonConfig):
    _active: bool
    _auto_rerun: bool
    _conda_avail: Optional[bool]
    _conda_env: Optional[str]
    _conda_envs_dirs: Optional[dict[str, str]]
    _confirm_install: bool
    _environment: Final[_Environment]
    _ipy_showsyntaxerror_orig: Optional[Union[IpyShowSyntaxErrorPre7, IpyShowSyntaxErrorPost7]]
    _ipython_shell: Final[Optional[IpythonShell]]
    _noninteractive: bool
    _pip_executable: str
    _smuggled: dict[str, str]
    _stdlib_modules: Final[set[str]]
    _suppress_stdout: bool
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def active(self) -> bool: ...
    @active.setter
    def active(self, state: bool) -> None: ...
    @property
    def auto_rerun(self) -> bool: ...
    @auto_rerun.setter
    def auto_rerun(self, value: bool) -> None: ...
    @property
    def conda_avail(self) -> bool: ...
    @conda_avail.setter
    def conda_avail(self, _: Any) -> NoReturn: ...
    @property
    def conda_env(self) -> Optional[str]: ...
    @conda_env.setter
    def conda_env(self, new_env: str) -> None: ...
    @property
    def conda_envs_dirs(self) -> Optional[dict[str, str]]: ...
    @conda_envs_dirs.setter
    def conda_envs_dirs(self, _: Any) -> NoReturn: ...
    @property
    def confirm_install(self) -> bool: ...
    @confirm_install.setter
    def confirm_install(self, value: bool) -> None: ...
    @property
    def environment(self) -> _Environment: ...
    @environment.setter
    def environment(self, _: Any) -> NoReturn: ...
    @property
    def ipython_shell(self) -> Optional[IpythonShell]: ...
    @ipython_shell.setter
    def ipython_shell(self, _: Any) -> NoReturn: ...
    @property
    def noninteractive(self) -> bool: ...
    @noninteractive.setter
    def noninteractive(self, value: bool) -> None: ...
    @property
    def pip_executable(self) -> str: ...
    @pip_executable.setter
    def pip_executable(self, exe_path: Union[PurePosixPath, str]) -> None: ...
    @property
    def smuggled(self) -> dict[str, str]: ...
    @smuggled.setter
    def smuggled(self, _: Any) -> NoReturn: ...
    @property
    def suppress_stdout(self) -> bool: ...
    @suppress_stdout.setter
    def suppress_stdout(self, value: bool) -> None: ...

def _block_greedy_ipython_completer() -> None: ...
def _get_stdlib_modules() -> set[str]: ...
