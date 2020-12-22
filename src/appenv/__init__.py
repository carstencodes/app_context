#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of appenv
# (see https://github.com/carstencodes/appenv).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

""" Module providing information about the current application and
the run-time packages that are currently used in the python environment.

The data is provided as python dataclass.
"""

from dataclasses import dataclass, field
from typing import Iterable, Dict, FrozenSet, MappingView
import sys
import os
import platform

import pkg_resources

__all__ = [
    "create_application_environment",
    "ApplicationEnvironment",
    "PackageInformation",
    "RunTimeInformation",
    "SystemInformation",
    "LanguageInformation",
]


# Abstraction for built-ins: abstract to make it testable.
__my_platform = platform


def __working_set() -> pkg_resources.WorkingSet:
    """Gets the working set of the current application.

    Returns:
        pkg_resources.WorkingSet: All loaded packages.
    """
    return pkg_resources.working_set


def __get_cur_dir() -> str:
    """Gets the current directory for the application.

    Returns:
        str: The current directory.
    """
    return os.curdir


def __get_entry_point() -> str:
    """Gets the application entry point starting the app.

    Returns:
        str: The application entry point.
    """
    return sys.argv[0]


@dataclass(frozen=True)
class SystemInformation:
    """Provides information about the current system.
    """
    name: str = field()
    """The name of the operating system.
    """
    version: str = field()
    """The version of the operating system.
    """
    architecture: str = field()
    """The system architecture.
    """
    processor: str = field()
    """The name of the processor.
    """
    host_name: str = field()
    """The name of the current host.
    """
    instruction_set: str = field()
    """The name of the instruction set.
    """


@dataclass(frozen=True)
class BuildInformation:
    """Provides information about the python build.
    """
    compiler: str = field()
    """The name of the compiler used.
    """
    built_on: str = field()
    """The date the build was performed.
    """
    build_number: str = field()
    """The incremental number of the build.
    """


@dataclass(frozen=True)
class SourceInformation:
    """Provides information about the source
       code python has been build from.
    """
    revision: str = field()
    """The source code revision, i.e. the git commit.
    """
    branch: str = field()
    """The git branch the executable was build from.
    """


@dataclass(frozen=True)
class LanguageInformation:
    """Provides information about the language interpreter.
    """
    name: str = field()
    """The name of the interpreter.
    """
    version: str = field()
    """The version of the interpreter.
    """
    implementation: str = field()
    """The implementation of the interpreter.
    """
    revision: SourceInformation = field()
    """The revision the interpreter was build from.
    """
    build: BuildInformation = field()
    """The information about the build that produced the interpreter.
    """


@dataclass(frozen=True)
class RunTimeInformation:
    """Provides information about the run-time of the current script.
    """
    system: SystemInformation = field()
    """Provides information about the system.
    """
    language: LanguageInformation = field()
    """Provides information about the programming language interpreter.
    """
    system_properties: MappingView[str, str] = field()
    """Provides additional information about the system.
       Varies from operating system to operating system.
    """


@dataclass(frozen=True)
class PackageInformation:
    """Provides information about a certain package that
       can be consumed at run-time.
    """
    name: str = field()
    """The name of the package.
    """
    version: str = field()
    """The version of the package.
    """
    location: str = field()
    """The installation location of the package.
    """
    extras: FrozenSet[str] = field()
    """The extras installed for the package.
    """


@dataclass(frozen=True)
class ApplicationEnvironment:
    """The environment of the current application.
    """
    name: str = field()
    """The name of the current application, i.e. name of the entry file.
    """
    entry_point: str = field()
    """The entry point of the current application, i.e. the start package.
    """
    working_dir: str = field()
    """The working directory of the application.
    """
    run_time: RunTimeInformation = field()
    """Information about the script run-time.
    """
    packages: FrozenSet[PackageInformation] = field()
    """Packages that can be consumed at run-time.
    """


def create_application_environment() -> ApplicationEnvironment:
    """Creates a stateful object that contains information
       about the current application environment.

    Returns:
        ApplicationEnvironment: The application environment information.
    """
    runtime_information: RunTimeInformation = _get_run_time_info()
    package_information: Iterable[PackageInformation] = list(
        _get_package_info()
    )
    entry_point = __get_entry_point()
    name, _ = os.path.splitext(os.path.basename(entry_point))
    working_dir = os.path.realpath(__get_cur_dir())

    return ApplicationEnvironment(
        name,
        entry_point,
        working_dir,
        runtime_information,
        frozenset(package_information),
    )


def _get_package_info() -> Iterable[PackageInformation]:
    """Collects information about available packages.

    Returns:
        Iterable[PackageInformation]: The packages available at run-time.

    Yields:
        Iterator[Iterable[PackageInformation]]: A current package.
    """
    for package in __working_set().entries():
        yield PackageInformation(
            package.key,
            package.version,
            package.location,
            frozenset(package.extras),
        )


def _get_build_info() -> BuildInformation:
    """Collects information about the build of the operating system.

    Returns:
        BuildInformation: The information object.
    """
    compiler: str = __my_platform.python_compiler()
    build_number, build_date = __my_platform.python_build()

    return BuildInformation(compiler, build_date, build_number)


def _get_source_info() -> SourceInformation:
    """Collects information about the source code of the interpreter.

    Returns:
        SourceInformation: The information about the interpreter source.
    """
    return SourceInformation(
        __my_platform.python_revision(), __my_platform.python_branch()
    )


def _get_system_info() -> SystemInformation:
    """Collects information about the current system.

    Returns:
        SystemInformation: The system information object.
    """
    name: str = __my_platform.platform()
    version: str = __my_platform.version()
    architecture: str = __my_platform.processor()
    processor: str = __my_platform.machine()
    host_name: str = __my_platform.node()
    instruction_set, _ = __my_platform.architecture()

    return SystemInformation(
        name, version, architecture, processor, host_name, instruction_set
    )


def _get_lang_info() -> LanguageInformation:
    """Collects information about the language interpreter.

    Returns:
        LanguageInformation: The language information object.
    """
    build_information: BuildInformation = _get_build_info()
    source_information: SourceInformation = _get_source_info()
    name: str = __my_platform.system()
    version: str = __my_platform.version()
    implementation = __my_platform.python_implementation()

    return LanguageInformation(
        name, version, implementation, source_information, build_information
    )


def _get_run_time_info() -> RunTimeInformation:
    """Collects information about the run-time.

    Returns:
        RunTimeInformation: The run-time information object.
    """
    system_information: SystemInformation = _get_system_info()
    language_information: LanguageInformation = _get_lang_info()
    system_extras: Dict[str, str] = _get_system_extras()

    return RunTimeInformation(
        system_information, language_information, system_extras
    )


def _get_system_extras() -> Dict[str, str]:
    """Gets information about the run-time that is not covered
       by a generic interface.

    Returns:
        Dict[str, str]: A key-value list of OS related information.
    """
    result: dict = dict(system_info_for=__my_platform.system())
    if __my_platform.system() == "Linux":
        dict.update(_get_linux_info())
    elif __my_platform.system() == "Darwin":
        result.update(_get_mac_info())
    elif __my_platform.system() == "Windows":
        result.update(_get_windows_info())
    elif __my_platform.system() == "Java":
        result.update(_get_java_info())

    return result


def _get_linux_info() -> Dict[str, str]:
    """Gets information about a Linux run-time that is not covered
       by a generic interface.

    Returns:
        Dict[str, str]: A key-value list of Linux related information.
    """
    libc_file, libc_version = __my_platform.libc_ver()
    return dict(libc_file=libc_file, libc_version=libc_version)


def _get_java_info() -> Dict[str, str]:
    """Gets information about a JAVA VM run-time that is not covered
       by a generic interface.

    Returns:
        Dict[str, str]: A key-value list of JAVA VM related information.
    """
    release, vendor, vm_info, os_info = __my_platform.java_ver()
    vm_name, vm_release, vm_vendor = vm_info
    os_name, os_version, os_arch = os_info
    return dict(
        release=release,
        vendor=vendor,
        vm_name=vm_name,
        vm_release=vm_release,
        vm_vendor=vm_vendor,
        os_name=os_name,
        os_version=os_version,
        os_arch=os_arch,
    )


def _get_windows_info() -> Dict[str, str]:
    """Gets information about a Windows run-time that is not covered
       by a generic interface.

    Returns:
        Dict[str, str]: A key-value list of Windows related information.
    """
    release, version, service_pack, ms_proc = __my_platform.win32_edition()
    is_iot = str(__my_platform.win32_is_iot())
    edition = __my_platform.win32_ver()
    return dict(
        release=release,
        version=version,
        service_pack=service_pack,
        processor=ms_proc,
        is_win_iot=is_iot,
        edition=edition,
    )


def _get_mac_info() -> Dict[str, str]:
    """Gets information about a MacOS X run-time that is not covered
       by a generic interface.

    Returns:
        Dict[str, str]: A key-value list of MacOS X related information.
    """
    release, version_info, machine = __my_platform.mac_ver()
    version, dev_stage, non_release_version = version_info
    return dict(
        release=release,
        machine=machine,
        version=version,
        dev_stage=dev_stage,
        non_release_version=non_release_version,
    )