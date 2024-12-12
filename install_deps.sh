#!/bin/bash

# Function to display the logo
display_  logo() {
echo "  ██      ██  ██  ████████    ████    ██     ██    ██       ██    ██████   ███████████    "         
echo "  ██      ██          ██    ██ ██    ██          ██            ██    ██     ██      "
echo "   ██    ██   ██     ██     ██  ██   ██      ██   ██       ██     ██         ██  "
echo "   ██    ██   ██    ██      ██████   ██      ██   ██       ██        ██      ██    "  
echo "    ██  ██    ██   ██      ██   ██   ██      ██   ██       ██   ██     ██    ██    "  
echo "     ████     ██  ████████ ██     ██  ███████  ██  ████████  ██     ██████      ██    "
}

# Function to display the welcome message
display_welcome_message() {
    echo "Welcome to the Vizualist automated installation process!"
    echo "This script will install all the necessary tools and dependencies for the Vizualist setup."
    echo ""
    echo "Please ensure you have sudo privileges to install the required packages."
    echo ""
}

# Function to prompt the user for confirmation
prompt_confirmation() {
    while true; do
        read -p "Do you want to continue and install these tools? (Y/n): " response
        case "$response" in
            [Yy]|[Yy][Ee][Ss])
                echo "Continuing with the installation..."
                break
                ;;
            [Nn]|[Nn][Oo])
                echo "Installation cancelled."
                exit 1
                ;;
            *)
                echo "Invalid response. Please enter Y or n."
                ;;
        esac
    done
}

# Function to prompt the user for their shell
prompt_shell() {
    echo "Please select your shell:"
    echo "1. bash"
    echo "2. zsh"
    echo "3. fish"
    echo "4. tcsh"
    echo "5. ksh"
    echo "6. csh"
    echo "7. Other (Please specify the path to your shell configuration file)"
    while true; do
        read -p "Enter the number corresponding to your shell or specify the path: " shell_choice
        case "$shell_choice" in
            1)
                shell_config="$HOME/.bashrc"
                break
                ;;
            2)
                shell_config="$HOME/.zshrc"
                break
                ;;
            3)
                shell_config="$HOME/.config/fish/config.fish"
                break
                ;;
            4)
                shell_config="$HOME/.tcshrc"
                break
                ;;
            5)
                shell_config="$HOME/.profile"
                break
                ;;
            6)
                shell_config="$HOME/.cshrc"
                break
                ;;
            *)
                read -p "Please enter the path to your shell configuration file: " shell_config
                if [[ -f "$shell_config" ]]; then
                    break
                else
                    echo "File not found. Please try again."
                fi
                ;;
        esac
    done
}

# Function to install dependencies
install_dependencies() {
    # Update package lists
    echo "Updating package lists..."
    sudo apt-get update

    # Install Python 3 and pip
    echo "Installing Python 3 and pip..."
    sudo apt-get install -y python3 python3-pip

    # Install Go
    echo "Installing Go..."
    if ! command -v go &> /dev/null; then
        wget https://golang.org/dl/go1.19.4.linux-amd64.tar.gz
        sudo tar -C /usr/local -xzf go1.19.4.linux-amd64.tar.gz
        rm go1.19.4.linux-amd64.tar.gz
        echo 'export PATH=$PATH:/usr/local/go/bin' >> "$shell_config"
        source "$shell_config"
    fi

    # Install Tkinter
    echo "Installing Tkinter..."
    sudo apt-get install -y python3-tk

    # Install Pmw
    echo "Installing Pmw..."
    pip3 install Pmw
}

# Function to install security tools
install_security_tools() {
    echo "Installing security tools..."

    # Assetfinder
    echo "Installing Assetfinder..."
    go install -v github.com/tomnomnom/assetfinder@latest

    # Subfinder
    echo "Installing Subfinder..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

    # Sublist3r
    echo "Installing Sublist3r..."
    sudo apt-get install -y sublist3r

    # Amass
    echo "Installing Amass..."
    sudo snap install amass

    # MassDNS
    echo "Installing MassDNS..."
    git clone https://github.com/blechschmidt/massdns.git
    cd massdns
    make
    sudo cp bin/massdns /usr/local/bin/
    cd ..

    # Shuffledns
    echo "Installing Shuffledns..."
    go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest

    # Dnsx
    echo "Installing Dnsx..."
    go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest

    # HTTProbe
    echo "Installing HTTProbe..."
    go install -v github.com/tomnomnom/httprobe@latest

    # Waybackpy
    echo "Installing Waybackpy..."
    pip3 install waybackpy

    # Gau
    echo "Installing Gau..."
    go install -v github.com/lc/gau/v2/cmd/gau@latest

    # Nuclei
    echo "Installing Nuclei..."
    go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

    # GF
    echo "Installing GF..."
    go install -v github.com/tomnomnom/gf@latest
    echo 'source $HOME/go/src/github.com/tomnomnom/gf/gf-completion.bash' >> "$shell_config"
    echo 'export PATH="$PATH:$HOME/.gf"' >> "$shell_config"
    source "$shell_config"

    # Sn1per
    echo "Installing Sn1per..."
    git clone https://github.com/1N3/Sn1per.git
    cd Sn1per
    sudo ./install.sh
    cd ..

    # Autorecon
    echo "Installing Autorecon..."
    git clone https://github.com/Tib3rius/AutoRecon.git
    cd AutoRecon
    sudo ./install.sh
    cd ..

    # LinkFinder
    echo "Installing LinkFinder..."
    git clone https://github.com/GerbenJavado/LinkFinder.git
    cd LinkFinder
    sudo python3 setup.py install
    cd ..

    # Meg
    echo "Installing Meg..."
    go install -v github.com/tomnomnom/meg@latest

    # FFUF
    echo "Installing FFUF..."
    go install -v github.com/ffuf/ffuf@latest

    # SQLmap
    echo "Installing SQLmap..."
    sudo apt-get install -y sqlmap

    # XSStrike
    echo "Installing XSStrike..."
    git clone https://github.com/s0md3v/XSStrike.git
    cd XSStrike
    sudo python3 setup.py install
    cd ..

    # Dirsearch
    echo "Installing Dirsearch..."
    git clone https://github.com/maurosoria/dirsearch.git

    # Subjack
    echo "Installing Subjack..."
    go install -v github.com/haccer/subjack@latest

    # CSP Evaluator
    echo "Installing CSP Evaluator..."
    git clone https://github.com/nVisium/content-security-policy-evaluator.git
    cd content-security-policy-evaluator
    sudo python3 setup.py install
    cd ..

    # GitHound
    echo "Installing GitHound..."
    git clone https://github.com/tillson/gitHound.git
    cd gitHound
    sudo python3 setup.py install
    cd ..
}

# Main script execution
display_logo
display_welcome_message
prompt_confirmation
prompt_shell
install_dependencies
install_security_tools

echo "All dependencies and tools have been installed successfully."
