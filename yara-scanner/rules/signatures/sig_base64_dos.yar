/*
  With Yara v4.0, we can now test for Base64 strings, these are some specific
  for Windows systems (DOS, PowerShell, VBScript, etc.)
*/
rule dos_rule_1 {
   strings:
      $s1 = "This program cannot" base64

   condition:
      any of them
}
