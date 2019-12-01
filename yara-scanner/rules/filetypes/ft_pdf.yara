rule fileType_PDF
{
   meta:
      author = "Todd Fencl"
      company = ""
      lastmod = "2019-10-18"
      desc = "Signature to detect PDF files"

   strings:
      $pdfOff = { 25 50 44 46 2D}

   condition:
      $pdfOff at 0
}
