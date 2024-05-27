from malmoext.malmo_bootstrap import MalmoBootstrap
import argparse

# Parse arguments
parser = argparse.ArgumentParser(
    prog='malmoext',
    description='Launches one or more Malmo Minecraft instances that can be used to run scenarios')
parser.add_argument(
        '--ports',
        nargs='+',
        default=['10000'],
        help='(Optional) List of ports that determine the number of Malmo Minecraft instances to spawn,'
                + 'and where they should run. Defaults to 10000, implying one instance running on port 10000.')
args = parser.parse_args()

# Run Malmo Minecraft instances
ports = list(map(int, args.ports))
MalmoBootstrap.start(ports)