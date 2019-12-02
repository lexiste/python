#!/usr/bin/env python3

import yara
import os
from termcolor import colored, cprint

def isMatch(rule, target_path):
    a = rule.match(target_path)
    if a:
        return True
    else:
        return False


def compileYaraRules(rule_path):
    ruleSet = []
    for (root, dir, files) in os.walk(rule_path):
        for file in files:
            if file.endswith('.yara'): # make sure we only load files that "appear" to be yara files
                print(colored('  [+]', 'green') + os.path.join(root, file))
                rule = yara.compile(os.path.join(root, file))
                ruleSet.append(rule)
            else:
                print (colored('  [-]' + os.path.join(root, file), 'red')) ##+ os.path.join(root, file)
    return ruleSet


def scanTargetDirectory(target_path, ruleSet):
    for (root, dir, files) in os.walk(target_path):
        for file in files:
            print(' ' + os.path.join(root, file))
            for rule in ruleSet:
                if (isMatch(rule, os.path.join(root, file))):
                    matches = rule.match(os.path.join(root, file))
                    if(matches):
                        print('\tYARA MATCH: '+os.path.join(root, file)+'\t'+matches[0].rule)

if __name__ == '__main__':
    compiled_ruleset = []
    target_path = 'files/'
    rule_path = 'rules/'

    print('Loading YARA rules ...') # let the user know that we are compiling the rules in our path
    compiled_ruleset = compileYaraRules(rule_path)

    print('Recursive scan of target files ...') # let the user know that we are getting ready to scan files in path for violations ...
    scanTargetDirectory(target_path, compiled_ruleset)
