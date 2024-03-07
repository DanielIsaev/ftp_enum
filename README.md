## Description

ftp_enum is a Python script that allows you to automatically map an FTP server's contents, and check the permissions on all directories recursivly. 


### Features

- Retrieves and displays directory listings from an FTP server.
- Displays read and write access permissions for directories.
- Checks for both file and directory write permissions. 
- Recursion depth of the scan can be controlled by a command-line option (Default is no limit).
- Attempts to handle FTP errors gracefully.
- Automatically switches between passive and active mode if necessary.

### Disclaimer

Although I have tested this script againts a dozen different FTP servers and my results were stable and consistent, I can't promise it will be the same for you. There are endless amounts of server configurations, environment deployments, and various other variables this script does not account for.

Therefore, I would exercise extreme caution, and start with a recursion depth set to 1 in order to test the server's response to this script. If the server responds nicely, I might consider scanning deeper down it's filesystem. 

I should also say that, by no means I'm I an expert developer, I don't claim my approach is the best and most efficient solultion to the general problem it attempts to solve. There could very well be other, more efficiant and "pythonic" ways of enumerating FTP servers for permissions but this is my solution. 

Finally, DO NOT use this script againts any FTP server you are not explicitly authorized to. This could very well lead to legal consequences, which I, the author of the script, will not be held accountable for. You are the one pressing the Enter key, not me, so think carefully about your actions. 

Other then that have fun:)

### Prerequisites

- Python 3.6 and higher. Otherwise you'll get a syntax error. 
- The rest of the modules are a part of the standard Python library. 

### Installation

You can either clone the repository:

```bash
git clone https://github.com/DanielIsaev/ftp_enum.git; cd ftp_enum
python3 ftp_enum.py --help
```

Or simply download the script itself:

```bash
wget https://github.com/DanielIsaev/ftp_enum/ftp_num.py
python3 ftp_enum.py --help
```

## Usage

pretty straightforward:

```bash
python ftp_enum.py <host> [-u <username>] [-p <password>] [-r <recursion_depth>]
```

### Example

Here is an example againts the Access machine from HTB:

![example](https://github.com/DanielIsaev/ftp_enum/blob/main/img/an4q789tqv.png) 

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit) so feel free to customize it further to fit your specific project details.
