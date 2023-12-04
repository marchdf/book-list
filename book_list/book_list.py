"""Alphabetize a list of books

A simple script to parse lists of books and alphabetize based on the
author last name.

"""

import argparse
import os
import time
from datetime import timedelta

import pandas as pd


def main():
    """Alphabetize a list of books"""
    start = time.time()

    # Parse arguments
    parser = argparse.ArgumentParser(description="Alphabetize the list of books")
    args = parser.parse_args()

    # Setup
    tmpfile = "tmp.md"
    basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    ifile = basedir + "/data/read_books.md"
    ofile = basedir + "/data/read_books_alpha.md"

    # Parse the list of books
    df = pd.read_csv(
        ifile,
        sep="|",
        skiprows=3,  # skip markdown header
        header=None,
        usecols=[0, 1, 2, 3, 4],  # dont take extra columns
        names=["name", "title", "status", "date", "own"],
    )

    # Get the first and last names
    names = df["name"].str.split()
    df["first_name"] = [" ".join(n[:-1]) for n in names]
    df["last_name"] = [n[-1] for n in names]

    # sort based on last name
    df = df.sort_values(
        by=["last_name", "first_name", "title", "date", "status", "own"]
    )

    # Save to file
    df.to_csv(
        tmpfile,
        sep="|",
        index=False,
        columns=["name", "title", "status", "date", "own"],
        header=False,
    )

    # Add header lines from original table
    with open(ifile) as f:
        h1 = f.readline()
        h2 = f.readline()
        h3 = f.readline()

    ftmp = open(tmpfile, "r")
    with open(tmpfile, "r") as ftmp, open(ofile, "w") as of:
        of.write(h1.rstrip() + " (alphabetized)\n")
        of.write(h2)
        of.write(h3)
        for line in ftmp.readlines():
            of.write(line)

    # Remove temporary file
    os.remove(tmpfile)

    # output timer
    end = time.time() - start
    print(
        "Elapsed time "
        + str(timedelta(seconds=end))
        + " (or {0:f} seconds)".format(end)
    )


if __name__ == "__main__":
    main()
