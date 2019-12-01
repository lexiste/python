/*
  Version: 0.0.1 2019-08-26

*/

rule js_src {
  meta:
    description = "locate the .src attribute"
    author = "tfencl"
    date = "2019-08-26"
  strings:
    $str01 = ".src" fullword nocase wide ascii
  condition:
    $str01
}

rule js_href {
  meta:
    description = "locate the <a href= string"
    author = "tfencl"
    date = "2019-08-26"
  strings:
    $str01 = "<a href=" fullword nocase wide ascii
  condition:
    $str01
}

rule  js_download {
meta:
  description = "locate the .download attribute"
  author = "tfencl"
  date = "2019-08-26"
strings:
  $str01 = ".download" fullword nocase wide ascii
condition:
  $str01
}
