import malmo.minecraftbootstrap
import os

def start(ports=[10000]):
    '''Starts 1 or more instances of Malmo Minecraft on the given ports.
    Defaults to one instance running on port 10000.'''

    cwd = os.getcwd()

    # Determine install directory for Malmo
    malmo_parent_dir = os.getenv('MALMO_INSTALL_DIR')
    if malmo_parent_dir is None:
        print('To control the install location of Malmo, set the MALMO_INSTALL_DIR environment variable')
        malmo_parent_dir = cwd
    
    # Install Malmo (if it is not already installed)
    os.chdir(malmo_parent_dir)
    malmo_dir = os.path.join(malmo_parent_dir, 'MalmoPlatform')
    if not os.path.exists(malmo_dir):
        print('Installing Malmo to ' + malmo_dir)
        malmo.minecraftbootstrap.download()
    malmo.minecraftbootstrap.set_malmo_xsd_path()

    # Launch Minecraft instances
    malmo.minecraftbootstrap.launch_minecraft(ports)
    
    os.chdir(cwd)