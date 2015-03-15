def test(expected, actual):
   if expected != actual:
      import sys, traceback
      (filename, lineno, container, code) = traceback.extract_stack()[-2]
      print("Test: %r failed on line %d in file %r.\nExpected %r but got %r\n" %
         (code, lineno, filename, expected, actual))

      sys.exit(1)
