import argparse
import csv
import datetime
import logging
import sys
import urllib.error
import urllib.request


# -------------------------------------------------------------------
# 1. Logger Setup
# Requirement 2 & 3: Logs errors to 'errors.log' in the required format
# -------------------------------------------------------------------
def setupLogger():
    logger = logging.getLogger("assignment2")
    logger.setLevel(logging.ERROR)

    file_handler = logging.FileHandler("errors.log", mode="w")
    formatter = logging.Formatter("%(message)s")
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger


# -------------------------------------------------------------------
# 2. Download Data Function
# Requirement 1: Downloads content from any given URL without catching exceptions internally
# -------------------------------------------------------------------
def downloadData(url):
    with urllib.request.urlopen(url) as response:
        return response.read()


# -------------------------------------------------------------------
# 3. Process Data Function
# Requirement 3: Processes lines and logs malformed/invalid dates to assignment2 logger
# -------------------------------------------------------------------
def processData(file_contents):
    logger = logging.getLogger("assignment2")
    person_dict = {}

    if isinstance(file_contents, bytes):
        file_contents = file_contents.decode("utf-8")

    lines = file_contents.strip().splitlines()
    reader = csv.reader(lines)

    for line_num, row in enumerate(reader, start=1):
        if not row:
            continue

        person_id, name, birthday_str = row[0], row[1], row[2]

        try:
            birthday_date = datetime.datetime.strptime(
                birthday_str, "%d/%m/%Y"
            )
            person_dict[int(person_id)] = (name, birthday_date)
        except (ValueError, IndexError):
            logger.error(
                f"Error processing line #{line_num} for ID #{person_id}"
            )

    return person_dict


# -------------------------------------------------------------------
# 4. Display Person Function
# Requirement 4: Displays users with exact required formatting
# -------------------------------------------------------------------
def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        formatted_date = birthday.strftime("%Y-%m-%d")
        print(f"Person #{id} is {name} with a birthday of {formatted_date}")
    else:
        print("No user found with that id")


# -------------------------------------------------------------------
# 5. Main Execution Function
# Requirement 1 & 5: Handles CLI argument, catches download errors, and loops until ID <= 0
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Download and process CSV birthday data."
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL pointing to the CSV dataset.",
    )
    args = parser.parse_args()

    setupLogger()

    # Step 2: Download data with main-level exception handling
    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"ERROR: Unable to download data from provided URL. Details: {e}")
        sys.exit(1)

    # Step 4: Process CSV data into dictionary
    personData = processData(csvData)

    # Step 5: Interactive lookup loop
    while True:
        try:
            user_input = int(
                input(
                    "Enter a person ID to lookup (enter 0 or negative number to exit): "
                )
            )

            # Requirement 5: Exit if ID <= 0
            if user_input <= 0:
                sys.exit(0)

            # Requirement 4: Print person details or 'No user found' message
            displayPerson(user_input, personData)

        except ValueError:
            print("Please enter a valid integer for the ID.")


if __name__ == "__main__":
    main()
