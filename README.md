# Aurum

<img src="Banner.jpeg" alt="Banner">

## Overview
Aurum is a Python-based terminal tool that provides email validation, domain MX record checks, and blacklist checks using the Spamhaus database. This tool helps users verify email validity, check if an email can receive messages, and determine whether a domain is blacklisted.

## Features
- **Email Validation:** Checks if an email address is syntactically valid.
- **MX Record Check:** Determines if the email domain has MX records, indicating its ability to receive emails.
- **Blacklist Check:** Checks if the email domain is blacklisted on Spamhaus.
- **All-in-One Check:** Runs all three checks in sequence for comprehensive analysis.
- **Cross-Platform:** Works on both Windows and Linux systems.

## Installation
### Prerequisites
Ensure you have Python installed on your system (Python 3.x recommended).

### Clone the Repository
To clone this repository, run the following command:
```sh
git clone https://github.com/your-username/aurum.git
cd aurum
```

### Install Required Dependencies
Run the following command to install dependencies:
```sh
pip install email-validator dnspython colorama
```

## Usage
Run the script from the terminal using:
```sh
python main.py
```
Then, follow the on-screen prompts to:
1. Validate an email address.
2. Check if an email domain can receive messages.
3. Check if an email domain is blacklisted.
4. Perform all checks at once.

### Windows Users
Windows users can use a compiled version of the code to run the tool without needing Python installed. A precompiled executable version will be available in the releases section.

## Example Output
```
------------------------Aurum-------------------------

|1.Check Email Validity|
|2.Check if Email Can Receive|
|3.Check if the Email is blacklisted|
|4.Run All checks|

Developed By Qais M. Alqaissi

---------------------Aurum Terminal--------------------

Enter your choice (1-4) or 'exit' to quit: 1
Enter the Email Address you want to Check: example@gmail.com
The Email Address example@gmail.com is a valid email address.
```

## License
This project is licensed under the Apache 2.0 License.

## Author
Developed by **Qais M. Alqaissi**.

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests.

## Contact
For any inquiries, reach out via [LinkedIn](www.linkedin.com/in/qais-alqaissi-1b9295238) or Email: Qipher09@proton.me.

