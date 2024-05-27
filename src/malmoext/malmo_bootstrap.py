import malmo.minecraftbootstrap
import os
    
class MalmoBootstrap:
    '''Class containing purely static utility methods for installing and starting the Malmo Minecraft Platform.'''

    def init_env():
        '''Initializes environment variables needed for Malmo Platform to successfully run.
        This method assumes that the Malmo Platform has already been installed'''

        working_dir = os.getcwd()
        install_dir = MalmoBootstrap.__get_malmo_install_dir()
        os.chdir(install_dir)
        malmo.minecraftbootstrap.set_malmo_xsd_path()
        os.chdir(working_dir)


    def start(ports=[10000]):
        '''Starts 1 or more instances of Malmo Minecraft on the given ports.
        Defaults to one instance running on port 10000.'''

        working_dir = os.getcwd()
        install_dir = MalmoBootstrap.__get_malmo_install_dir()
        
        # Install Malmo (if it is not already installed)
        os.chdir(install_dir)
        malmo_dir = os.path.join(install_dir, 'MalmoPlatform')
        if not os.path.exists(malmo_dir):
            print('Installing Malmo to ' + malmo_dir)
            malmo.minecraftbootstrap.download()
        malmo.minecraftbootstrap.set_malmo_xsd_path()

        # Launch Minecraft instances
        malmo.minecraftbootstrap.launch_minecraft(ports)
        
        os.chdir(working_dir)


    def __get_malmo_install_dir():
        '''Returns the parent directory that the Malmo Platform should be installed to'''
        
        target = os.getenv('MALMO_INSTALL_DIR')
        if target is None:
            target = os.getcwd()
        return target