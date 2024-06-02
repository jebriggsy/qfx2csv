import pytest
import ofxtools
import csv
import os
from src.qfx2csv.qfx2csv import to_csv, ArgList, CSVConfig

TESTDATA = os.getcwd() + "/data/"


# Doesn't have OFX headers
def test_wrong_source_file_type():
    arglist = ArgList()
    arglist.source_file = TESTDATA + "notofx.gif"
    arglist.trntype = True
    arglist.dtposted = True
    arglist.trnamt = True

    with pytest.raises(ofxtools.header.OFXHeaderError):
        to_csv(arglist)


# Doesn't have transactions, what we are actually converting
def test_wrong_ofx_file():
    arglist = ArgList()
    arglist.source_file = TESTDATA + "notrans.ofx"

    with pytest.raises((IndexError, TypeError)):
        to_csv(arglist)


def test_convert():
    arglist = ArgList()
    arglist.source_file = TESTDATA + "stmtrs-160.ofx"
    arglist.trntype = True
    arglist.trnamt = True
    arglist.dtposted = True

    to_csv(arglist)

    with open(TESTDATA + "stmtrs-160.ofx.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile, dialect=CSVConfig)
        for row in reader:
            assert row["dtposted"] == "2024-04-29 07:00:00+00:00"
            break
