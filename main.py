from app import *
from mysqlHelper import *
import sys

createSchemaAndTable()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Run tests
        import unittest
        import test

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test)
        # unittest.TextTestRunner(verbosity=2).run(suite)
        # Add your test import statements here
        unittest.main()
    else:
        # Run the Flask app
        app.run(debug=True)