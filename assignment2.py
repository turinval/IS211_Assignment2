import argparse
import csv
import datetime
import logging
import sys
import urllib.error
import urllib.request

# -------------------------------------------------------------------
# Function 1: Setup Logger
# -------------------------------------------------------------------
def setupLogger():
    """Configures the 'assignment2' logger to write log messages to errors.log."""
    logger = logging.getLogger("assignment2")
    logger.setLevel(logging.ERROR)

    # File handler to output logs to errors.log
    file_handler = logging.FileHandler("errors.log", mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Avoid adding multiple handlers if setupLogger is called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger


# -------------------------------------------------------------------
# Function 2: downloadData
# -------------------------------------------------------------------
def downloadData(url):
    """Downloads content from the provided URL."""
    with urllib.request.urlopen(url) as response:
        return response.read()


# -------------------------------------------------------------------
# Function 3: processData
# -------------------------------------------------------------------
def processData(file_contents):
    """Parses CSV contents line-by-line into a dictionary mapping ID -> (Name, Birthday)."""
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
# Function 4: displayPerson
# -------------------------------------------------------------------
def displayPerson(id, personData):
    """Prints the person's name and birthday if found in personData."""
    if id in personData:
        name, birthday = personData[id]
        formatted_date = birthday.strftime("%Y-%m-%d")
        print(f"Person #{id} is {name} with a birthday of {formatted_date}")
    else:
        print("No user found with that id")


# -------------------------------------------------------------------
# Function 5: main
# -------------------------------------------------------------------
def main():
    # 1. Parse CLI arguments
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

    # Configure logger
    setupLogger()

    # 2. Download Data with Exception Handling
    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(
            f"ERROR: Failed to download data from the provided URL. Details: {e}"
        )
        sys.exit(1)

    # 4. Process Data
    personData = processData(csvData)

    # 5. Interactive Prompt Loop
    while True:
        try:
            user_input = int(
                input(
                    "\nEnter a person ID to lookup (enter 0 or negative number to exit): "
                )
            )
            if user_input <= 0:
                print("Exiting program.")
                sys.exit(0)

            displayPerson(user_input, personData)

        except ValueError:
            print("Please enter a valid integer for the ID.")


if __name__ == "__main__":
    main()
