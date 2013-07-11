#!flask/bin/python
from app import flask_application
from optparse import OptionParser

def main():

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-s", "--server", dest="nameHost", default="localhost",
                      help="host domain name or IP if you do not want 'localhost'")
    parser.add_option("-p", "--port", dest="numPort", default=8080,
                      help="port to serve out of if you do not want '8088'")
    parser.add_option("-l", "--live", help="turn off debug mode",
                      action="store_false", dest="debug")
    parser.add_option("-d", "--debug", help="turn on debug mode",
                      action="store_true", dest="debug")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")

    (options, args) = parser.parse_args()
    
    if options.verbose:
        print "Will use Host -- {} and port -- {}.".format(options.nameHost, options.numPort)


    flask_application.run(options.nameHost, int(options.numPort), debug = options.debug)


if __name__ == "__main__":
    main()
	

# Example :    ./run.py -s www.matrixoflife.net -p 8088 -d &

