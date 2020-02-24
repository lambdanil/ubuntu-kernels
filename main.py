import subprocess
import os
import sys

# Get commandline arguments
argv = list(sys.argv)

# Clear screen
def clear():
    os.system('clear')
    
# Main()
def main(argv):
    if len(argv) > 2:
        if argv[1] == '-i' or argv[1] == '--install':
            # Set version
            version = str(argv[2])
            # Fetch URL info
            os.system("wget -q https://kernel.ubuntu.com/~kernel-ppa/mainline -O /tmp/ubuntu-kernels >> /dev/null")
            install(version)
        if argv[1] == '-r' or argv[1] == '--remove':
            # Fetch URL info
            os.system("wget -q https://kernel.ubuntu.com/~kernel-ppa/mainline -O /tmp/ubuntu-kernels >> /dev/null")
            # Set version
            version = str(argv[2])
            remove(version)
    else:
        if argv[1] == '-l' or argv[1] == '--list':
            # Fetch URL info
            os.system("wget -q https://kernel.ubuntu.com/~kernel-ppa/mainline -O /tmp/ubuntu-kernels >> /dev/null")
            show()
        if argv[1] == '-c' or argv[1] == '--clean-cache':
            clean()
        else:
            print("Not enough arguments!")
    
# Clean file
def clean():
    os.system('rm -f /tmp/ubuntu-kernels;rm -rf /tmp/ubuntu-kernels.d/')

# List kernels
def show():
    kernelfile = open("/tmp/ubuntu-kernels","r")
    line = ''
    lines = []
    filel = int(subprocess.check_output('cat /tmp/ubuntu-kernels | wc -l',shell=True))
    curr = 0
    while '[DIR]' not in line:
        line = kernelfile.readline()
    while curr != filel:
        line = kernelfile.readline()
        curr += 1
        if 'href="v' in line:
            lines.append(line)
    newlines = []
    for item in lines:
        item = item.replace('<tr><td valign="top"><img src="/icons/folder.gif" alt="[DIR]"></td><td><a href="v','')
        newlines.append(item)
    lines = []
    for item in newlines:
        letter = ''
        newitem = []
        c = 0
        while letter != '/':
            letter = item[c]
            if letter != '/':
                newitem.append(letter)
            c += 1
        lines.append(''.join(newitem))
    print("\n".join(lines))
        
# Remove
def remove(version):
    os.system(f"apt remove --purge linux-headers-{version} linux-image-unsigned-{version} linux-modules-{version}")

# Install()
def install(version):
    # Open URL info
    kernelfile = open("/tmp/ubuntu-kernels","r")
    # Check if selected kernel verion is available
    line = kernelfile.readline()
    while str(version) not in line and (line != ''):
        line = kernelfile.readline()
    kernelfile.close()
    # If selected version is available
    if str(version) in line:
        os.system(f"wget -q https://kernel.ubuntu.com/~kernel-ppa/mainline/v{version} -O /tmp/ubuntu-kernels >> /dev/null")
        # Get kernel version website info
        kernelfile = open("/tmp/ubuntu-kernels","r")
        line = kernelfile.readline()
        links = []
        link = ''
        # Get files
        for i in range (0,4,+1):
            if len(links) != 0:
                for item in links:
                    while '.deb' not in line or ('lowlatency' in line) or (item in line):
                        line = kernelfile.readline()
            else:
                while '.deb' not in line or ('lowlatency' in line):
                    line = kernelfile.readline()
            line = line.replace('&nbsp;   <a href="','')
            link = []
            index = 0
            letter=str("")
            while '.deb' not in str(link):
                letter = str(letter)+str(line[index])
                link.append(str(letter))
                index += 1
            link = str(link[len(link)-1])
            links.append(link)
        newlinks = []
        for item in links:
            newlinks.append(f'https://kernel.ubuntu.com/~kernel-ppa/mainline/v{version}/{item}')
        os.system("mkdir -p /tmp/ubuntu-kernels.d")
        index = 0
        print("Fetching kernel files...")
        for item in newlinks:
            os.system(f'wget -q {item} -O /tmp/ubuntu-kernels.d/{links[index]}')
            index += 1
        os.system("dpkg -i /tmp/ubuntu-kernels.d/*.deb")
        
            
    # If selected version is not available
    else:
        print('Selected kernel version not found!')

main(argv)
