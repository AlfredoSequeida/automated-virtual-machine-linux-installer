import requests
import sys
from os import popen, system, path, remove
from bs4 import BeautifulSoup
from shutil import copyfile

VB_REPO = "https://download.virtualbox.org/virtualbox"


def print_header():
    """print program ascii art header"""

    header = """
 __       _______  __       
|  \     |       \|  \      
| ▓▓     | ▓▓▓▓▓▓▓\ ▓▓      
| ▓▓     | ▓▓__/ ▓▓ ▓▓      
| ▓▓     | ▓▓    ▓▓ ▓▓      
| ▓▓     | ▓▓▓▓▓▓▓\ ▓▓      
| ▓▓_____| ▓▓__/ ▓▓ ▓▓_____ 
| ▓▓     \ ▓▓    ▓▓ ▓▓     \\
 \▓▓▓▓▓▓▓▓\▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓▓
                            
    Long Beach Lunabotics
    """
    print(header)


def get_current_path() -> str:
    """Get current path of script/executable"""

    application_path = ""

    if getattr(sys, "frozen", False):
        application_path = path.dirname(sys.executable)
    elif __file__:
        application_path = path.dirname(__file__)

    return application_path


def menu_handler() -> int:
    """Handle menu for program and return user integer option"""
    option = int(
        input(
            """
1) Install/reinstall virtual machine image (includes VirtualBox)
2) Uninstall virtual machine image
3) Create desktop shortcut
4) Exit

"""
        )
    )
    return option


def proceed_with_installation(manager: str):
    """Check for previously installed lunabotics vms and prompt user for overrides
    of the vm is previous installation is found

    manager -- path of VirtualBox manager
    """
    proceed = True
    vms = popen(f"{manager} list vms").read()

    for vm in vms.splitlines():
        name = vm.split('" {')[0].replace('"', "")
        if name == "lunabotics":
            ask = True
            while ask:
                user_input = input(
                    "Previous installation found. "
                    "Installing again will delete previous installation "
                    "and all work done in that virtual machine. "
                    "Do you want to proceed(Y/N)? "
                ).lower()

                if user_input == "y" or user_input == "yes":
                    proceed = True
                    ask = False
                elif user_input == "n" or user_input == "no":
                    proceed = False
                    ask = False
                else:
                    print("Invalid option. Use Y or N")

            break

    return proceed


def get_latest_vbox_version() -> str:
    """Get the latest version of virtual box from https://download.virtualbox.org/virtualbox/"""

    download_page = BeautifulSoup(requests.get(VB_REPO).text, features="lxml")
    versions = download_page.find("pre").find_all("a")

    latest = (0, "")

    for version in versions:
        original_version = version.text.replace("/", "")
        stripped_version = original_version.replace(".", "")

        if stripped_version.isdigit():
            simple_version = int(stripped_version)

            if simple_version > latest[0]:
                latest = (simple_version, original_version)

    return latest[1]


def download_vbox(version: str, platform: str, destination: str) -> str:
    """Dowload the specified version of virtual box for the specified platform

    version -- the verision to download
    platform -- the platform to download virtualbox for
    file_path -- the location to save the file
    """
    download_page = BeautifulSoup(
        requests.get(f"{VB_REPO}/{version}").text, features="lxml"
    )
    downloads = download_page.find("pre").find_all("a")

    file_name = ""

    # get file for platform
    for download in downloads:
        name = download.text
        if platform in name:
            file_name = name
            break

    # download
    download_file(
        requests.get(f"{VB_REPO}/{version}/{file_name}", stream=True), destination
    )


def download_vm_image(destination: str):
    """Download virtual machine image from google drive. The id for the file is kept in
    the github repo to always download the latest image.

    destination -- the file path to save the file
    """

    image_id = requests.get(
        "https://raw.githubusercontent.com/AlfredoSequeida/automated-virtual-machine-linux-installer/main/image.txt"
    ).text.strip()
    download_file_from_google_drive(image_id, destination)


def download_file_from_google_drive(id: str, destination: str):
    """Download file from google drive
    id -- the id of the download
    destination -- the path to save the file to
    """

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    download_file(response, destination)


def get_confirm_token(response: requests):
    """Get session token from page request for use with google drive tokens
    response -- requests session
    """
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value


def download_file(response: requests, destination: str, chunk_size: int = 32768):
    """Download a file given a requests object
    response -- a requests get reponse
    destination -- the destination path to save the file to
    chunk_size -- the chunk size to use for donwloading
    """

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)


def install_vbox(file_path):
    """Install VirtualBox
    file_path -- the path of the VirtualBox installer
    """
    system(f"{file_path} --silent --ignore-reboot")


def uninstall_vbox_image(manager):
    """
    kill headless instances, power off lunabotics vm, and delete previously installed lunabotics images
    manager -- VirtualBox manager path
    """

    # kill vbox headless instances
    system("Taskkill /IM VBoxHeadless.exe /F")

    # power off vm
    system(f"{manager} controlvm lunabotics acpipowerbutton")

    # delete old images
    system(f"{manager} unregistervm --delete lunabotics")


def setup_vbox_image(manager, image):
    """Setup image by issuing commands to stoping all headless instances, kill lunabotics vm sessions,
    and deleting any previous lunabotics vms

    manager -- VirtualBox manager path
    image -- VirtualBox image to setup
    """

    uninstall_vbox_image(manager)

    # setup image
    system(f"{manager} import {image}")


def copy_launcher_to_desktop():
    """Copy the launcher (bat file) to desktop"""
    launcher_path = path.join(sys._MEIPASS, "lunabotics.bat")
    copyfile(launcher_path, f"C:\\Users\\{os.getlogin()}\\Desktop\\lunabotics.bat")


def clean_up(files: list):
    """delete unnecessary files
    files -- the file paths to remove
    """

    for f in files:
        remove(f)


if __name__ == "__main__":

    vbox_manager_path = '"C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"'
    current_path = get_current_path()
    vbox_version = get_latest_vbox_version()
    vbox_installer_path = path.join(current_path, "vbox.exe")
    vbox_image_path = path.join(current_path, "lunabotics.ova")

    run = True
    valid = True

    while run:

        print_header()

        if not valid:
            print("Invalid option")

        option = menu_handler()

        if option == 1:
            if proceed_with_installation(vbox_manager_path):

                print(f"Downloading VirtualBox v{vbox_version} . . .")

                download_vbox(vbox_version, "Win", vbox_installer_path)

                print("Installing VirtualBox . . .")
                install_vbox(vbox_installer_path)

                print("Downloading VirtualBox Image . . .")
                download_vm_image(vbox_image_path)

                print("Setting up VirtualBox Image . . .")
                setup_vbox_image(vbox_manager_path, vbox_image_path)

                print("Creating desktop shortcut . . .")
                copy_launcher_to_desktop()

                print("Cleaning up . . .")
                clean_up([vbox_installer_path, vbox_image_path])

                print("Done, double-click lunabotics.bat on your desktop to start")
                valid = True

        elif option == 2:
            print("Uninstalling virtual machine")
            uninstall_vbox_image(vbox_manager_path)
            print("Done")
            valid = True

        elif option == 3:
            copy_launcher_to_desktop()
            print("Done, double-click lunabotics.bat on your desktop to start")
            valid = True

        elif option == 4:
            run = False
            valid = False

        else:
            valid = False

        if valid:
            input("Press ENTER to continue . . .")

        system("cls")
