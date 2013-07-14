#!flask/bin/python
import argparse
import os.path

from app import flask_application
from install import dbUtil

def main():

    fontus = "A stripper well management tool based on Miguel Grinberg's Flask tutorial."
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser(description=fontus)
    parser.add_argument("-s", "--server", dest="nameHost", default="localhost",
                      help="host domain name or IP if you do not want 'localhost'")
    parser.add_argument("-p", "--port", dest="numPort", default=8080,
                      help="port to serve out of if you do not want '8088'")
    parser.add_argument("-l", "--live", help="turn off debug mode",
                      action="store_false", dest="debug")
    parser.add_argument("-k", "--kill", help="scrap and remake the database",
                      action="store_false", dest="debug")
    parser.add_argument("-d", "--debug", help="turn on debug mode",
                      action="store_true", dest="debug")
    parser.add_argument("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_argument("-q", "--quiet",
                      action="store_false", dest="verbose")
                      
    base_dir = os.path.abspath(os.path.dirname(__file__))

    args = parser.parse_args()
    
    if args.verbose:
        print "Kill"
        engine = dbUtil.start_engine()
        dbUtil.drop(base_dir, engine)
        dbUtil.create()
        dbUtil.load(engine)
        
    if args.verbose:
        print "Will use Host -- {} and port -- {}.".format(args.nameHost, args.numPort)


    flask_application.run(args.nameHost, int(args.numPort), debug = args.debug)


if __name__ == "__main__":
    main()
	

# Example :    ./run.py -s www.matrixoflife.net -p 8088 -d &

