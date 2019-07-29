import jgo.util
import os
import sys

from . import version

_paintera                = '@Paintera'
_paintera_show_container = '@PainteraShowContainer'
_groupId                 = 'org.janelia.saalfeldlab'
_artifactId              = 'paintera'
_slf4j_endpoint          = os.getenv('PAINTERA_SLF4J_BINDING', f'org.slf4j:slf4j-simple:{version._slf4j_version}')

def launch_paintera():
    return jgo.util.main_from_endpoint(
        primary_endpoint            = f'{_groupId}:{_artifactId}',
        primary_endpoint_version    = version._paintera_version.maven_version(),
        primary_endpoint_main_class = _paintera,
        secondary_endpoints         = (_slf4j_endpoint,))

def launch_paintera_show_container():
    return jgo.util.main_from_endpoint(
        primary_endpoint            = f'{_groupId}:{_artifactId}',
        primary_endpoint_version    = version._paintera_version.maven_version(),
        primary_endpoint_main_class = _paintera_show_container,
        secondary_endpoints         = (_slf4j_endpoint,))

