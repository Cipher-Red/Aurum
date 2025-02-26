import shutil
from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError
import dns.resolver
from colorama import Fore, Style
import csv
from fpdf import FPDF
from dns.resolver import LifetimeTimeout
import re
from datetime import datetime
import smtplib
import socket


def validate(email):

    try:
        # If the Email is valid then it will run this function
        valid = validate_email(email)
        normalized_email = valid.email
        return Fore.GREEN + f"The Email Address {normalized_email} is a valid email address."


    # Email is not valid it will run this function
    except EmailNotValidError as e:
        return Fore.RED + f"The Email Address {email} is not a valid email address {e}."

def mx_records(email):
    try:
        # Validate email syntax
        valid = validate_email(email)
        normalized_email = valid.email
        domain = normalized_email.split("@")[1]
        records = ["MX", "A", "AAAA", "CNAME", "NS", "PTR", "SOA", "TXT", "SRV", "TLSA", "CAA", "DNAME"]

        # Check if the domain has any of the required records
        for record in records:
            try:
                answers = dns.resolver.resolve(domain, record, lifetime=15)  # Timeout in 3 seconds
                if answers:
                    return Fore.GREEN + f"Domain {domain} has a Valid {record} record. This email might receive emails."
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout, dns.resolver.NoNameservers):
                continue

        return Fore.RED + f"Domain {domain} does not have a valid DNS records."

    except EmailNotValidError as e:
        return Fore.RED + f"Invalid email: {email} ({e})"
    except EmailUndeliverableError:
        return Fore.RED + f"The domain {domain} does not accept email."

def blacklistcheck(email):
    try:
        # Validate email
        valid = validate_email(email)
        normalized_email = valid.email
        domain = normalized_email.split("@")[1]

        # Blacklist database to check against
        blacklists = ["zen.spamhaus.org","psbl.surriel.com","dnsbl.sorbs.net","bl.spamcop.net","b.barracudacentral.org",
                      "all.spamrats.com","bl.spameatingmonkey.net","ubl.unsubscore.com","truncate.gbudb.net","dnsbl.info",
                      "ubl.lashback.com","rbl.interserver.net","xbl.spamhaus.org","cbl.abuseat.org","dnsbl-1.uceprotect.net",
                      "dnsbl-2.uceprotect.net","dnsbl-3.uceprotect.net","relays.mail-abuse.org","dnsbl.spfbl.net",
                      "rbl.efnetrbl.org","multi.surbl.org","dbl.spamhaus.org","uribl.spameatingmonkey.net"]

        # Check if the domain is blacklisted on multiple lists
        for blacklist in blacklists:
            query = f"{domain}.{blacklist}"
            try:
                dns.resolver.resolve(query, "A")
                return Fore.RED + f"The Domain {domain} is Blacklisted on {blacklist}"
                return
            except LifetimeTimeout:
                return f"DNS query for {domain} timed out."
                continue
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                continue
        return Fore.GREEN + f"The domain {domain} is not blacklisted on any of the checked blacklists."

    except EmailNotValidError as e:
        return Fore.RED + f"Email is in an invalid form: {e}"

# A Custom internal blacklist you can add to it what you find or discover
def cblacklist(email):

    try:
        valid = validate_email(email)
        normalized_email = valid.email
        domain = normalized_email.split("@")[1]

        emailbl = ["example@spam.spam","test@test.com"]
        blacklist = ["0SPAM","Abuse.ro","example.domain"]

        if domain in blacklist or normalized_email in emailbl:
            return Fore.RED + f"This Email address {email} is blacklisted."

        else:
            return Fore.GREEN + f"The Email address {email} isn't blacklisted internally"

    except EmailNotValidError as e:
        return Fore.RED + f"Email is in an invalid form {e}"

def fullscan(email):

    print(Style.RESET_ALL + "[Validating Email Address]".center(terminal_width, ' '))
    print(validate(email))

    print(Style.RESET_ALL + "[Checking DNS records]".center(terminal_width, ' '))
    print(mx_records(email))

    print(Style.RESET_ALL + "[Checking if the domain is blacklisted]".center(terminal_width, ' '))
    print(blacklistcheck(email))

    print(Style.RESET_ALL + "[Checking if the domain is blacklisted using the custom list]".center(terminal_width, ' '))
    print(cblacklist(email))

    print(Style.RESET_ALL + "[Checking if the Email is Valid by sending packets]".center(terminal_width, ' '))
    print(vc(email))

def rct(text):
    # Remove color codes from the text
    return re.sub(r'\033\[[0-9;]*m', '', text)

def bulfullscan(email):
    output_data = []

    output_data.append("\n~~~~Validation Result~~~~\n")
    result = validate(email) or "No result"  # Ensure something is returned
    result = rct(result)
    output_data.append(result)

    output_data.append("\n~~~~DNS records Result~~~~\n")
    result = mx_records(email) or "No result"
    result = rct(result)
    output_data.append(result)

    output_data.append("\n~~~~Blacklist Result~~~~\n")
    result = blacklistcheck(email) or "No result"
    result = rct(result)
    output_data.append(result)

    output_data.append("\n~~~~Custom blacklist Result~~~~\n")
    result = cblacklist(email) or "No result"
    result = rct(result)
    output_data.append(result)

    output_data.append("\n~~~~Reachability Result~~~~\n")
    result = vc(email) or "No result"
    result = rct(result)
    output_data.append(result)

    return output_data


def report(output_data, filename="Aurum_Report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.image('Report_Header.png', x=0, y=0, w=pdf.w)
    pdf.ln(50)

    for line in output_data:

        if "Email:" in line:
            pdf.set_font("Arial", style='B', size=15)
        else:
            pdf.set_font("Arial", size=13)  # Set normal font

        pdf.multi_cell(0, 10, line)

    pdf.ln(20)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(200, 10, txt=f"Report generated on: {timestamp}", ln=True, align="C")

    pdf.output(filename)

def bulkscan(file_path):

    output_data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            email = row[0]
            result = bulfullscan(email)
            output_data.append(f"\nEmail: {email}")
            output_data.append(f"{' '.join(result)}\n")
            report(output_data)



def vc(email):
    domain = email.split("@")[-1]

    # Known email providers smtp servers / mail servers
    # You can add your own smtp server to check for custom mail servers
    # Example { "Domain.com": "mail.Domain.com", } you can use this to add to the list to check
    mail_servers = {
        "gmail.com": "gmail-smtp-in.l.google.com",
        "yahoo.com": "mta5.am0.yahoodns.net",
        "outlook.com": "outlook-com.olc.protection.outlook.com",
        "protonmail.com": "mail.protonmail.ch",
        "proton.me": "mail.protonmail.ch",
        "fibertechjo.com": "fibertechjo-com.mail.protection.outlook.com",
    }

    mail_server = mail_servers.get(domain)

    if not mail_server:
        return Fore.RED + "Mail server not found for this domain. - add the SMTP/mail server address to the list"

    ports = [587, 25, 465]
    for port in ports:

        try:

            if port == 465:
                server = smtplib.SMTP_SSL(mail_server, port, timeout=10)
            else:
                server = smtplib.SMTP(mail_server, port, timeout=10)

            server.set_debuglevel(0)
            server.ehlo()

            if port == 587:
                server.starttls()
                server.ehlo()

            sender_email = "test@example.com"
            server.mail(sender_email)
            code, message = server.rcpt(email)

            server.quit()

            if code == 250:
                return Fore.GREEN + "This Email can Receive messages"
            elif code == 550:
                return Fore.RED + "This Email cannot Receive messages"
            else:
                return Fore.RED + f"Unknown response: {code} {message}"

        except Exception as e:
            return Fore.RED + f"Error: {e} - Could be a security measure for spam if there was a time out error"


if __name__ == '__main__':

    # Take The terminal Size to center the text
    terminal_width = shutil.get_terminal_size().columns
    print("Aurum".center(terminal_width, '-'))
    print("")
    print("|1.Check Email Validity|".center(terminal_width, ' '))
    print("|2.Check if Email Can Receive|".center(terminal_width, ' '))
    print("|3.Check if the Email is blacklisted|".center(terminal_width, ' '))
    print("|4.Check if the Email is internally blacklisted using a custom list|".center(terminal_width, ' '))
    print("|5.Check if the Email can Receive emails/Validation check|".center(terminal_width, ' '))
    print("|6.Perform Bulk Email Checks using a .CSV file with a full scan|".center(terminal_width, ' '))
    print("|7.Run All checks|\n".center(terminal_width, ' '))
    print("Developed By Qais M.Alqaissi\n".center(terminal_width, ' '))
    print("Aurum Terminal".center(terminal_width, '-'))

    while True:

        option = input(Style.RESET_ALL + "\nEnter your choice (1-6) or 'exit' to quit: ")
        option = option.lower()

        if option == "1":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")

            print(validate(email))

        elif option == "2":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")

            print(mx_records(email))

        elif option == "3":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")

            print(blacklistcheck(email))

        elif option == "4":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")
            print(cblacklist(email))

        elif option == "5":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")
            print(vc(email))

        elif option == "6":
            file_path = input(Style.RESET_ALL + "Enter the File path to the .CSV file: ")
            bulkscan(file_path)
            print(f"Report of the scan is done ")

        elif option == "7":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")
            fullscan(email)

        elif option == "exit":
            print(Fore.RED + "Shutting down...")
            break
