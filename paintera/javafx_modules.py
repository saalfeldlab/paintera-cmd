import sys
from jgo.jgo import default_config

_javafx_platform_map = {
    "linux": "linux",
    "linux2": "linux",
    "win32": "win",
    "darwin": "mac"
}

_javafx_version = "13.0.1"
_javafx_group = "org/openjfx"
_modules_and_opens = {
    "javafx.base": [
        'javafx.util',
        'javafx.event',
        'javafx.beans.property',
        'com.sun.javafx.binding',
        'com.sun.javafx.event',
    ],
    "javafx.controls": [],
    "javafx.graphics": [
        "javafx.scene",
        "javafx.stage",
        "javafx.geometry",
        "javafx.animation",
        "javafx.scene.input",
        "javafx.scene.image",
        "com.sun.prism",
        "com.sun.javafx.geom",
        "com.sun.javafx.image",
        "com.sun.javafx.scene",
        "com.sun.javafx.stage",
        "com.sun.javafx.perf",
        "com.sun.javafx.cursor",
        "com.sun.javafx.tk",
        "com.sun.javafx.scene.traversal",
        "com.sun.javafx.geom.transform",
        "com.sun.scenario.animation",
        "com.sun.scenario.animation.shared",
        "com.sun.scenario.effect",
        "com.sun.javafx.sg.prism",
    ]
}


def _javafx_module_path():
    m2_repository = default_config()['settings'].get('m2Repo')
    relative_module_paths = []
    for module in _modules_and_opens.keys():
        module_path_name = module.replace(".", "-")
        shared_prefix = f"{_javafx_group}/{module_path_name}/{_javafx_version}/{module_path_name}-{_javafx_version}"
        common_module = f"{shared_prefix}.jar"
        platform_specific_module = f"{shared_prefix}-{_javafx_platform_map[sys.platform]}.jar"
        relative_module_paths.append(platform_specific_module),
        relative_module_paths.append(common_module)
    absolute_module_paths = (f"{m2_repository}/{x}" for x in relative_module_paths)
    module_path = ":".join(absolute_module_paths)
    return module_path


# Allow access to classes that are not exported (currently needed)
javafx_args = ["--illegal-access=permit"]

# for each class we use, open it to ALL-UNNAMED, which contains Paintera,
#   since it isn't utilizing the module system currently
for module_name, packages_to_open in _modules_and_opens.items():
    for package in packages_to_open:
        javafx_args.append(f"--add-opens={module_name}/{package}=ALL-UNNAMED")

# add the module path for the javafx modules
javafx_args.extend(["--module-path", _javafx_module_path()])
# specify which modules we actually use.
javafx_args.extend(["--add-modules", ",".join(_modules_and_opens.keys())])
