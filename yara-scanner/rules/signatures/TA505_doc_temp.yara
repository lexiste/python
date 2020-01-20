/*
  Version 0.0.1 2020-01-20
  Source code put in public domain by Todd Fencl, no Copyright
  Use at your own risk

  These are YARA rules to detect VBA code that might be malware.

  Shortcomings, or todo's ;-) :

  History:
    2020-01-20: start
*/

rule doc_temp01
{
  strings:
    $a1 = { D0 CD 11 E0 A1 B1 1A E1 }
    $a2 = { E1 2E 60 13 5F D5 01 40 }
  condition:
    $a1 at 0 and $a2
}
