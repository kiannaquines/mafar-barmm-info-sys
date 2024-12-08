from PyPDFForm import PdfWrapper


filled = PdfWrapper("RSBSA_Enrollment-Form_Digital_Copy.pdf").fill(
    {
        "Text1": "NAQUINES",
        "Text2": "GERALDEZ",
        "Text3": "KIAN JEARARD",
        "Text4": "Jr.",
    },
)

with open("output.pdf", "wb+") as output:
    output.write(filled.read())