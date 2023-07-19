# pylint: disable=consider-using-with
from PyPDF4 import (
    PdfFileReader,
    PdfFileWriter,
)
from aioextensions import (
    in_process,
)
from context import (
    STARTDIR,
)
from dataloaders import (
    Dataloaders,
)
from fpdf import (
    FPDF,
)
from groups import (
    domain as groups_domain,
)
import os


class PDF(FPDF):
    user = ""

    def set_user(self, user: str) -> None:
        self.user = user

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Times", "", 12)
        self.cell(0, 10, f"Only for {self.user}", 0, 0, align="L")
        self.cell(0, 10, f"Page {self.page_no() - 1}", 0, 0, align="R")


class SecurePDF:
    """Add basic security to PDF."""

    footer_tpl = ""
    passphrase = ""  # nosec
    result_dir = ""
    secure_pdf_filename = ""
    secure_pdf_usermail = ""
    secure_pdf_username = ""
    watermark_tpl = ""

    def __init__(self) -> None:
        """Class constructor."""
        self.base = f"{STARTDIR}/integrates/back/src/reports"
        self.footer_tpl = os.path.join(
            self.base, "resources/themes/overlay_footer.pdf"
        )
        self.result_dir = os.path.join(self.base, "results/results_pdf/")
        self.watermark_tpl = os.path.join(
            self.base, "resources/themes/watermark_integrates_en.pdf"
        )

    async def create_full(
        self,
        loaders: Dataloaders,
        usermail: str,
        basic_pdf_name: str,
        group_name: str,
    ) -> str:
        """Execute the security process in a PDF."""
        self.secure_pdf_usermail = usermail
        self.secure_pdf_username = usermail.split("@")[0]
        if await groups_domain.exists(loaders, group_name.lower()):
            return os.path.join(self.result_dir, basic_pdf_name)

        water_pdf_name = await in_process(self.overlays, basic_pdf_name)
        return os.path.join(self.result_dir, water_pdf_name)

    def lock(self, in_filename: str) -> str:
        """Add a passphrase to a PDF."""
        pdf_foutname = f"{self.secure_pdf_username}_{in_filename}"
        output = PdfFileWriter()
        input_file = PdfFileReader(  # noqa
            open(
                os.path.join(self.result_dir, in_filename),
                "rb",
            )
        )
        for i in range(0, input_file.getNumPages()):
            output.addPage(input_file.getPage(i))
        output_stream = open(os.path.join(self.result_dir, pdf_foutname), "wb")
        output.encrypt(self.passphrase, use_128bit=True)
        output.write(output_stream)
        output_stream.close()
        return pdf_foutname

    def overlays(self, in_filename: str) -> str:
        """Add watermark and footer to all pages of a PDF."""
        pdf_foutname = f"water_{in_filename}"

        footer_pdf = PDF()
        footer_pdf.set_user(self.secure_pdf_usermail)
        footer_pdf.alias_nb_pages()
        input_file = PdfFileReader(  # noqa
            open(self.result_dir + in_filename, "rb")
        )
        for i in range(1, input_file.getNumPages()):
            footer_pdf.add_page()
        footer_pdf.add_page()
        footer_pdf.output(self.footer_tpl)
        footer_pdf.close()

        output = PdfFileWriter()
        overlay_watermark = PdfFileReader(open(self.watermark_tpl, "rb"))
        overlay_footer = PdfFileReader(open(self.footer_tpl, "rb"))
        for i in range(0, input_file.getNumPages()):
            page = input_file.getPage(i)
            page.mergePage(overlay_watermark.getPage(0))
            if i != 0:
                page.mergePage(overlay_footer.getPage(i))
            output.addPage(page)
        output_stream = open(os.path.join(self.result_dir, pdf_foutname), "wb")
        output.write(output_stream)
        output_stream.close()
        return pdf_foutname
