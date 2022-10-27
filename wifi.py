from cProfile import Profile
import profile
import subprocess
import os
import re
from collections import namedtuple
import configparser
from tabnanny import verbose



def get_windows_saved_ssids():
    """tra ve danh sach ssid da luu trong may bang lenh netsh"""
    #nhan tat ca cac cau hinh da luu trong may
    output= subprocess.check_output("netsh wlan show profile").decode()
    ssids=[]
    profiles= re.findall(r"All user profile\s(.*)",output)
    for profile in profiles:
        #doi vs moi ssid hay xoa dau cach va dau hai cham
        ssid= profile.strip().strip(":").strip()
        #them vao list
        ssid.append(ssid)
    return ssids
def get_windows_saved_wifi_passwords(verbose=1):
    #trich xuat mk da luu trong may
    ssids = get_windows_saved_ssids()
    Profile = namedtuple("Profile",["ciphers","keys","ssid"])
    profiles=[]
    for ssid in ssids:
        ssid_details = subprocess.check_output(f"""netsh wlan show profile"{ssid}"key = clear""")
        #get the ciphers
        ciphers ="/".join([c.strip().strip(":").strip() for c in ciphers])
        #get the wifi
        ciphers = re.findall(r"Cipher\s(.*)",ssid_details)
        #clear space and colon
        try:
            key = key[0].strip().strip(":").strip()
        except IndexError:
            key = "none"
        profile= Profile(ssid=ssid,ciphers=ciphers,key=key)
        if verbose >=1:
            print_windows_profile(profile)
        profile.append(profile)
    return profiles
def print_windows_profile(profile):
    #print a single profile on window
    print(f"{profile.ssid:25}{profile.ciphers:15}{profile.key:50}")
def print_windows_profiles(verbose):
    #prints all extracted ssids along with key on window 
    print("SSID                    CIPHER(S)       KEY")
    print("_"*50)
    get_windows_saved_wifi_passwords(verbose)
def get_linux_saved_wifi_passwords(verbose):
    

    network_connections_path = "/etc/NetworkManager/system-connections/"
    fields = ["ssid", "auth-alg", "key-mgmt", "psk"]
    Profile = namedtuple("Profile", [f.replace("-", "_") for f in fields])
    profiles = []
    for file in os.listdir(network_connections_path):
        data = { k.replace("-", "_"): None for k in fields }
        config = configparser.ConfigParser()
        config.read(os.path.join(network_connections_path, file))
        for _, section in config.items():
            for k, v in section.items():
                if k in fields:
                    data[k.replace("-", "_")] = v
        profile = Profile(**data)
        if verbose >= 1:
            print_linux_profile(profile)
        profiles.append(profile)
    return profiles


def print_linux_profile(profile):
        """Prints a single profile on Linux"""
        print(f"{str(profile.ssid):25}{str(profile.auth_alg):5}{str(profile.key_mgmt):10}{str(profile.psk):50}")
        
def print_linux_profiles(verbose):
    """Prints all extracted SSIDs along with Key (PSK) on Linux"""
    print("SSID                     AUTH KEY-MGMT  PSK")
    print("-"*50)
    get_linux_saved_wifi_passwords(verbose)
def print_profiles(verbose=1):
    if os.name == "nt":
        print_windows_profiles(verbose)
    elif os.name == "posix":
        print_linux_profiles(verbose)
    else:
        raise NotImplemented("Code only works for either Linux or Windows")
    
    
if __name__ == "_main_":
    print_profiles()        
