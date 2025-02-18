import shutil
from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError
import dns.resolver
from colorama import Fore, Style

def validate(email):

    try:
        # If the Email is valid then it will run this function
        valid = validate_email(email)
        normalized_email = valid.email
        print(Fore.GREEN + f"The Email Address {normalized_email} is a valid email address.")


    # Email is not valid it will run this function
    except EmailNotValidError as e:
        print(Fore.RED + f"The Email Address {email} is not a valid email address {e}.")

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
        valid = validate_email(email)
        normalized_email = valid.email
        domain = normalized_email.split("@")[1]

        blacklist = "zen.spamhaus.org"
        query = f"{domain}.{blacklist}"

        try:
            dns.resolver.resolve(query, "A")
            print(Fore.RED + f"The Domain |{domain}| is Blacklisted on Spamhaus")

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            print(Fore.GREEN + f"The Domain |{domain}| is not Blacklisted on Spamhaus")
    except EmailNotValidError as e:
        print(Fore.RED + f"Email Is in a invalid form {e}")

if __name__ == '__main__':

    # Take The terminal Size to center the text
    terminal_width = shutil.get_terminal_size().columns
    print("Aurum".center(terminal_width, '-'))
    print("")
    print("|1.Check Email Validity|".center(terminal_width, ' '))
    print("|2.Check if Email Can Receive|".center(terminal_width, ' '))
    print("|3.Check if the Email is blacklisted|".center(terminal_width, ' '))
    print("|4.Run All checks|\n".center(terminal_width, ' '))
    print("Developed By Qais M.Alqaissi\n".center(terminal_width, ' '))
    print("Aurum Terminal".center(terminal_width, '-'))




    while True:

        option = input(Style.RESET_ALL + "\nEnter your choice (1-4) or 'exit' to quit: ")
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

            print(Style.RESET_ALL + "[Validating Email Address]".center(terminal_width, ' '))
            validate(email)

            print(Style.RESET_ALL + "[Checking MX records]".center(terminal_width, ' '))
            mx_records(email)

            print(Style.RESET_ALL + "[Checking if the domain is black listed]".center(terminal_width, ' '))
            blacklistcheck(email)

        elif option == "exit":
            print("Shutting down...")
            break
