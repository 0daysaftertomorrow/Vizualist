# Vizualist
The Program Launcher and Console is a Python-based GUI application designed for bug bounty hunters. It allows users to dynamically select, configure, and execute a series of security tools against specified targets. The application provides an intuitive interface for managing toolsets, adjusting targets, and viewing real-time command outputs, streamlining the process of running multiple reconnaissance and vulnerability assessment tools.

# Program Launcher and Console

This project is a Python-based GUI application that allows users to select, configure, and run a series of bug bounty hunting tools. The application is built using Tkinter and supports dynamic management of target domains and commands.

## Features

- **Program Selection**: Choose from a list of predefined bug bounty tools.
- **Launch List Management**: Add, remove, and clear programs to be executed.
- **Dynamic Target Management**: Change the target domain or file dynamically.
- **Console Output**: View the output and errors of the executed commands in a console window.
- **Tooltip Support**: Hover over programs to see the actual command that will be executed.
- **File Browsing**: Browse and select files for target input.

## Requirements

- Python 3.x
- Tkinter
- Pmw (Python MegaWidgets)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/program-launcher.git
    cd program-launcher
    ```

2. Install the required Python packages:

    ```bash
    pip install Pmw
    ```

## Usage

1. Run the main script:

    ```bash
    python main.py
    ```

2. **Start Investigation**: A pop-up window will prompt you to enter a domain or select a file for investigation.

3. **Add Programs**: Select programs from the list and add them to the launch list using the "Add to Launch List" button.

4. **Change Target**: Use the text field and "Change!" button to update the target dynamically.

5. **Manage Launch List**: Remove individual programs or clear the entire list using the "Remove" and "Clear" buttons.

6. **Run Programs**: Click "Run Code List" to execute the selected programs. The output and errors will be displayed in the console.

## File Structure

- `main.py`: Main script to launch the GUI application.
- `programs.json`: Configuration file containing the list of bug bounty tools and their commands.

## Example `programs.json`

```json
[
    {"name": "assetfinder", "cmd": "assetfinder $TARGET | tee $TARGET_assetfinder.txt"},
    {"name": "Subfinder -d", "cmd": "subfinder -d $TARGET | tee $TARGET_subfinder.txt"},
    {"name": "Subfinder -list", "cmd": "subfinder -l $TARGET_FILE | tee $domain_subfinder_list.txt"},
    {"name": "Sublist3r", "cmd": "sublist3r -d $TARGET -b -p 21,22,25,80,443,445,8080 -v -t 100 -e google.com | tee $TARGET_sublist3r.txt"},
    {"name": "Sort and Unique", "cmd": "cat *.txt | sort | uniq | anew $TARGET_unique_doms.txt"},
    {"name": "Resolver", "cmd": "shuffledns -list $TARGET_unique_doms -r ~/tools/multiviz/resolve.txt -mode resolve | tee $TARGET_resolved.txt"},
    {"name": "Dnsx recon", "cmd": "dnsx -d $TARGET -cdn -recon -re -w /usr/share/seclists/Discovery/DNS/bug-bounty-program-subdomains-trickest-inventory.txt -r ~/tools/multiviz/resolve.txt"},
    {"name": "HTTprobe", "cmd": "cat $TARGET_resolved.txt | httprobe | tee $TARGET_httprobed.txt"},
    {"name": "403-checker", "cmd": "sudo ~/tools/multiviz/curly.sh $TARGET_unique_doms.txt ~/tools/multiviz/403.txt | tee $TARGET_403.txt"}
]
```
Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    Tkinter - Python's de-facto standard GUI package.
    Pmw - Python MegaWidgets.

javascript


This `README.md` file includes sections for features, requirements, installation, usage, file structure, an example `programs.json`, contributing guidelines, license information, and acknowledgments. Adjust the URLs and specific details as needed for your project.

