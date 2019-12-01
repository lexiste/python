rule pdf_v17_contains_link
{
  meta:
    author = "todd fencl"
    last_update = "27-Nov-2018"
    description = "PDFv1.7 with HTML link(s)"
  strings:
    $pdf_fingerprint = {25 50 44 46}
    $s_anchor_tag = "<a " ascii wide nocase
    $s_url_tab = /\(http.+\)/ ascii wide nocase
  condition:
    $pdf_fingerprint at 0 and any of ($s*)
}
