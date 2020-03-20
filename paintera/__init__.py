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

def _get_paintera_version(argv=None):
    import argparse
    argv = sys.argv[1:] if argv is None else argv
    if ('--' in argv):

        def version_from_string(string):
            split = string.split('.')
            try:
                major, minor, patch = [int(s) for s in split[:3]]
                tag = ''
            except:
                major, minor = [int(s) for s in split[:2]]
                patch = int(split[2].split('-')[0])
                tag = 'SNAPSHOT'
            return version._Version(major, minor, patch, tag)

        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
        parser.add_argument('--use-version', type=version_from_string)
        args, unknown = parser.parse_known_args(argv)
        return version._paintera_version if args.use_version is None else args.use_version, unknown

    else:
        return version._paintera_version, argv

def launch_paintera():
    paintera_version, argv = _get_paintera_version(argv=sys.argv[1:])
    return jgo.util.main_from_endpoint(
        argv                        = argv,
        primary_endpoint            = f'{_groupId}:{_artifactId}',
        primary_endpoint_version    = paintera_version.maven_version(),
        primary_endpoint_main_class = _paintera)

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

    output = os.path.join(args.prefix, relative_path) if args.output is None else args.output

    argv = [
        '-n', 'paintera',
        'org.janelia.saalfeldlab.paintera.PainteraCommandLineArgs',
        '-o', output]

    pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)

    return jgo.util.main_from_endpoint(
        primary_endpoint            = f'{_groupId}:{_artifactId}',
        argv                        = jgo_argv + argv,
        primary_endpoint_version    = version._paintera_version.maven_version(),
        primary_endpoint_main_class = _picocli_autocomplete)

