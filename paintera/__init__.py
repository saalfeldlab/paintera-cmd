import jgo.util
import os
import pathlib
import sys

from . import version

_paintera                = '@Paintera'
_paintera_show_container = '@PainteraShowContainer'
_picocli_autocomplete    = 'picocli.AutoComplete'
_paintera_cli_args       = 'org.janelia.saalfeldlab.paintera.PainteraCommandLineArgs'
_groupId                 = 'org.janelia.saalfeldlab'
_artifactId              = 'paintera'
_slf4j_endpoint          = os.getenv('PAINTERA_SLF4J_BINDING', f'org.slf4j:slf4j-simple:{version._slf4j_version}')

def launch_paintera():
    return jgo.util.main_from_endpoint(
        primary_endpoint            = f'{_groupId}:{_artifactId}',
        primary_endpoint_version    = version._paintera_version.maven_version(),
        primary_endpoint_main_class = _paintera,
        secondary_endpoints         = (_slf4j_endpoint,))

def generate_paintera_bash_completion():
    relative_path = os.path.join(
        'share',
        'bash-completion',
        'completions',
        'paintera')
    default_path = os.path.join('$PREFIX', relative_path)
    description=f'''Generate bash completion file for Paintera. This script uses picocli[1] to create a script file for bash-completion[2]. The default output location is {default_path} and can be modified with the --prefix option or overwritten entirely with the --output option.

[1] https://picocli.info
[2] https://github.com/scop/bash-completion
'''
    import argparse
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    default_prefix = os.getenv('PREFIX', os.path.abspath(os.path.join(os.sep, 'usr')))
    parser.add_argument('--prefix', required=False, default=default_prefix, help='Sets the PREFIX for the output location. Is ignored if --output is set.')
    parser.add_argument('--output', required=False, default=None, help='Specifies the output location explicitly (PREFIX and --prefix are ignored)')

    argv = sys.argv[1:]

    try:
        double_dash_index = argv.index('--')
    except ValueError:
        double_dash_index = -1

    if double_dash_index > 0 and double_dash_index < len(argv):
        jgo_argv = argv[:double_dash_index + 1]
        argv     = argv[double_dash_index + 1:]
    else:
        jgo_argv = []

    args = parser.parse_args(args=argv)

    output = os.path.join(args.prefix, relative_path) if args.output is None else output

    argv = [
        '-n', 'paintera',
        'org.janelia.saalfeldlab.paintera.PainteraCommandLineArgs',
        '-o', output]

    pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)

    return jgo.util.main_from_endpoint(
        primary_endpoint            = f'{_groupId}:{_artifactId}',
        argv                        = jgo_argv + argv,
        primary_endpoint_version    = version._paintera_version.maven_version(),
        primary_endpoint_main_class = _picocli_autocomplete,
        secondary_endpoints         = (_slf4j_endpoint,))

