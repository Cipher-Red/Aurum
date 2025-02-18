import shutil
from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError
import dns.resolver
from colorama import Fore, Style
import csv


def validate(email):

    try:
        # If the Email is valid then it will run this function
        valid = validate_email(email)
        normalized_email = valid.email
        print(Fore.GREEN + f"The Email Address |{normalized_email}| is a valid email address.")


    # Email is not valid it will run this function
    except EmailNotValidError as e:
        print(Fore.RED + f"The Email Address |{email}| is not a valid email address {e}.")

def mx_records(email):

    try:
        # Validate email syntax
        valid = validate_email(email)
        normalized_email = valid.email
        domain = normalized_email.split("@")[1]

        try:
            # Check if the domain has MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            print(Fore.GREEN + f"Domain |{domain}| has MX records. This email can receive emails.")
            return
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout):
            print(Fore.RED + f"Domain |{domain}| does not have MX records.")

        # No MX then check A
        try:
            dns.resolver.resolve(domain, 'A')
            print(f"No MX records, but |{domain}| has an A record. It might accept emails.")
            return
        except dns.resolver.NoAnswer:
            pass

        # No A check for AAAA
        try:
            dns.resolver.resolve(domain, 'AAAA')
            print(f"No MX records, but |{domain}| has an AAAA record. It might accept emails.")
            return
        except dns.resolver.NoAnswer:
            pass

        # If none have the domain then its invalid
        print(Fore.RED + f"Domain |{domain}| does not accept email.")

    except EmailNotValidError as e:
        print(Fore.RED + f"Invalid email: {email} {e}")
    except EmailUndeliverableError:
        print(Fore.RED + f"The domain |{domain}| does not accept email.")

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
                print(Fore.RED + f"The Domain |{domain}| is Blacklisted on {blacklist}")
                return
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                continue
        print(Fore.GREEN + f"The domain |{domain}| is not blacklisted on any of the checked blacklists.")

    except EmailNotValidError as e:
        print(Fore.RED + f"Email is in an invalid form: {e}")

# A Custom internal blacklist you can add to it what you find or discover
def cblacklist(email):

    try:
        valid = validate_email(email)
        normalized_email = valid.email
        domain = normalized_email.split("@")[1]

        emailbl = ["example@spam.spam","test@test.com"]
        blacklist = ["0SPAM","Abuse.ro","example.domain"]

        if domain in blacklist or normalized_email in emailbl:
            print(Fore.RED + f"This Email address |{email}| is blacklisted.")

        else:
            print(Fore.GREEN + f"The Email address |{email}| isn't blacklisted internally")

    except EmailNotValidError as e:
        print(Fore.RED + f"Email is in an invalid form {e}")

def fullscan(email):

    print(Style.RESET_ALL + "[Validating Email Address]".center(terminal_width, ' '))
    validate(email)

    print(Style.RESET_ALL + "[Checking MX records]".center(terminal_width, ' '))
    mx_records(email)

    print(Style.RESET_ALL + "[Checking if the domain is blacklisted]".center(terminal_width, ' '))
    blacklistcheck(email)

    print(Style.RESET_ALL + "[Checking if the domain is blacklisted using the custom list]".center(terminal_width, ' '))
    cblacklist(email)

def bulkscan(file_path):

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            email = row[0]
            fullscan(email)

if __name__ == '__main__':

    # Take The terminal Size to center the text
    terminal_width = shutil.get_terminal_size().columns
    print("Aurum".center(terminal_width, '-'))
    print("")
    print("|1.Check Email Validity|".center(terminal_width, ' '))
    print("|2.Check if Email Can Receive|".center(terminal_width, ' '))
    print("|3.Check if the Email is blacklisted|".center(terminal_width, ' '))
    print("|4.Check if the Email is internally blacklisted using a custom list|".center(terminal_width, ' '))
    print("|5. Perform Bulk Email Checks using a .CSV file with a full scan|".center(terminal_width, ' '))
    print("|6.Run All checks|\n".center(terminal_width, ' '))
    print("Developed By Qais M.Alqaissi\n".center(terminal_width, ' '))
    print("Aurum Terminal".center(terminal_width, '-'))




    while True:

        option = input(Style.RESET_ALL + "\nEnter your choice (1-6) or 'exit' to quit: ")
        option = option.lower()

        if option == "1":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")

            validate(email)

        elif option == "2":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")

            mx_records(email)

        elif option == "3":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")

            blacklistcheck(email)

        elif option == "4":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")
            cblacklist(email)

        elif option == "5":
            file_path = input(Style.RESET_ALL + "Enter the File path to the .CSV file: ")
            bulkscan(file_path)

        elif option == "6":
            email = input(Style.RESET_ALL + "Enter the Email Address you want to Check: ")
            fullscan(email)

        elif option == "exit":
            print(Fore.RED + "Shutting down...")
            break
