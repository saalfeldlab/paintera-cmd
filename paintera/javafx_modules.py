import sys

_javafx_platform_map = {
    "linux": "linux",
    "linux2": "linux",
    "win32": "win",
    "darwin": "mac"
}

_javafx_version = "13.0.1"
_javafx_group = "org.openjfx"

_modules_and_opens = {
    "javafx.base": [
        'javafx.util',
        'javafx.event',
        'javafx.beans.property',
        'com.sun.javafx.binding',
        'com.sun.javafx.event',
    ],
    "javafx.controls": [],
    "javafx.fxml": [],
    "javafx.media": [],
    "javafx.swing": [],
    "javafx.web": [],
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


def javafx_module_deps():
    """
    jgo expects --module-dependencies to be a list of the form: "group:artifact:version[:classifier].
        We construct that here.

    :return: list[str] of "group:artifact:version[:classifier]" to be placed on the module-path
    """
    module_dependencies = []
    for module in _modules_and_opens.keys():
        module_path_name = module.replace(".", "-")
        classifier = _javafx_platform_map[sys.platform]
        common_artifact = f"{_javafx_group}:{module_path_name}:{_javafx_version}"
        platform_artifact = f"{_javafx_group}:{module_path_name}:{_javafx_version}:{classifier}"
        module_dependencies.append(common_artifact)
        module_dependencies.append(platform_artifact)
    return module_dependencies


def javafx_modules():
    """
    :return: comma separate list of the javafx modules we with to add to the jvm runtime
    """
    return ",".join(_modules_and_opens.keys());


# Specify for jgo the dependencies which should be treated as modules
javafx_args = ["--module-dependencies"]
javafx_args.extend(javafx_module_deps())

# Allow access to classes that are not exported by their modules (currently needed).
javafx_args += ["--illegal-access=permit"]
# for each class we use, open it to ALL-UNNAMED, which contains Paintera since it isn't utilizing the module system currently
for module_name, packages_to_open in _modules_and_opens.items():
    for package in packages_to_open:
        javafx_args.append(f"--add-opens={module_name}/{package}=ALL-UNNAMED")

javafx_args += ["--add-modules"]
javafx_args += [javafx_modules()]
