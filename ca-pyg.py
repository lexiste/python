""" a pig latin word converter in python, takes a single input"""

pyg = 'ay'

original = raw_input("Enter a word: ")

if len(original) > 0 and original.isalpha():
  print "org} " + original
  word = original.lower()
  first = word[0]
  new_word = word + first + pyg
  new_word = new_word[1:len(new_word)]
  print "new} " + new_word
else:
  print 'empty'
