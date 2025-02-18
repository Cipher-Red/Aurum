# Aurum

<div align="center">
<img src="Heading.png" alt="Banner">
</div>

## Overview
Aurum is a Python-based terminal tool that provides email validation, domain MX record checks, and blacklist checks using multiple DNS-based blacklists (DNSBLs). This tool helps users verify email validity, check if an email can receive messages, and determine whether a domain is blacklisted.


## Features
- **Email Validation:** Checks if an email address is syntactically valid.
- **MX Record Check:** Determines if the email domain has MX records, indicating its ability to receive emails.
- **Blacklist Check:** Checks if the email domain is blacklisted on multiple DNSBLs, including Spamhaus, SORBS, and Barracuda.
- **Custom Blacklist Check:** Allows adding a custom internal blacklist for manually flagged domains or specific email addresses.
- **All-in-One Check:** Runs all four checks in sequence for comprehensive analysis.
- **Bulk Email Check:** Performs bulk email validation from a CSV file, running a full scan for each email.
- **Cross-Platform:** Works on both Windows and Linux systems.

## Installation
### Prerequisites
Ensure you have Python installed on your system (Python 3.x recommended).

### Clone the Repository
To clone this repository, run the following command:
```sh
git clone https://github.com/Cipher-Red/Aurum.git
cd Aurum
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
4. Check if an email address or domain is internally blacklisted using a custom list.
5. Perform all checks at once.

### Windows Users
Windows users can use a compiled version of the code to run the tool without needing Python installed. A precompiled executable version will be available in the releases section.

## Example Output
```
-------------------------------------Aurum--------------------------------------

                            |1.Check Email Validity|                            
                         |2.Check if Email Can Receive|                         
                     |3.Check if the Email is blacklisted|                      
      |4.Check if the Email is internally blacklisted using a custom list|      
       |5. Perform Bulk Email Checks using a .CSV file with a full scan|        
                              |6.Run All checks|
                               
                         Developed By Qais M.Alqaissi
                          
---------------------------------Aurum Terminal---------------------------------

Enter your choice (1-5) or 'exit' to quit: 1
Enter the Email Address you want to Check: example@gmail.com
The Email Address |example@gmail.com| is a valid email address.
```

## Blacklists Checked
Aurum queries multiple DNSBLs, including:
- Spamhaus (zen.spamhaus.org, dbl.spamhaus.org, xbl.spamhaus.org)
- SpamCop (bl.spamcop.net)
- Barracuda (b.barracudacentral.org)
- SORBS (dnsbl.sorbs.net)
- SURBL (multi.surbl.org, phishing.rhsbl.surbl.org)
- And many more...

## License
This project is licensed under the Apache 2.0 License. 

The **Apache 2.0 License** allows you to freely use, modify, and distribute the software, even for commercial purposes, under the following conditions:
- You must include the original copyright notice and license in any distribution.
- Any modifications must be clearly documented.
- The software is provided "as is," without warranty of any kind.
- You are not allowed to use the project’s trademarks, branding, or logo without permission.

For full details, refer to the official [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

## Legal Disclaimer
Aurum is designed as a tool for security professionals, researchers, and ethical users. 

- **Intended Use:** This tool should only be used for lawful and ethical security research, email security assessments, and administrative monitoring.
- **Unauthorized Use:** Using Aurum to check third-party emails or domains without proper authorization may violate privacy laws and terms of service agreements.
- **No Warranty:** The software is provided "as is" without any warranties or guarantees. The developers are not responsible for any misuse, legal consequences, or damage resulting from its use.
- **Compliance:** Ensure compliance with local laws and regulations when using this tool.

By using Aurum, you agree to these terms and acknowledge that misuse of the tool is solely your responsibility.

## Author
Developed by **Qais M. Alqaissi**.

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests.

## Contact
For any inquiries, reach out via [LinkedIn](https://www.linkedin.com/in/qais-alqaissi-1b9295238/) or Email: Qipher09@proton.me.

