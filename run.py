#!flask/bin/python
import argparse
import os.path

from frmwk import flask_framework
from install import dbUtil

def main():

    warehouseman = "A generic 'blank' website structure based on Miguel Grinberg's Flask 'mega'-tutorial."
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser(description=warehouseman)
    parser.add_argument("-s", "--server", dest="nameHost", default="localhost",
                      help="host domain name or IP if you do not want 'localhost'")
    parser.add_argument("-p", "--port", dest="numPort", default=80,
                      help="port to serve out of if you do not want '80'")

    parser.add_argument("-g", "--regenerate", help="scrap and remake the database",
                      action="store_true", dest="regenerate", default=False)

    parser.add_argument("-l", "--live", help="turn off debug mode",
                      action="store_false", dest="debug", default=False)
    parser.add_argument("-d", "--debug", help="turn on debug mode",
                      action="store_true", dest="debug", default=False)

    parser.add_argument("-v", "--verbose",
                      action="store_true", dest="verbose", default=False)
    parser.add_argument("-q", "--quiet",
                      action="store_false", dest="verbose", default=False)
                      
    base_dir = os.path.abspath(os.path.dirname(__file__))

    args = parser.parse_args()
    
    if args.regenerate:
        print "Regenerate"
        engine = dbUtil.start_engine()
        dbUtil.drop(base_dir, engine)
        dbUtil.create()
        dbUtil.load(engine)
        
    if args.verbose:
        print "Will use Host -- {} and port -- {}.".format(args.nameHost, args.numPort)


    flask_framework.config['MINE'] = 'XXXX'
    flask_framework.run(args.nameHost, int(args.numPort), debug = args.debug)


if __name__ == "__main__":
    main()
	

# Example :    ./run.py -vdg -s www.matrixoflife.net -p 8088 &

# find . -name "*.py~" -print0 | xargs -0 rm -rf  && find . -name "*.pyc" -print0 | xargs -0 rm -rf
# grep -R --exclude=\*.*~ --exclude=\*.pyc --exclude-dir={flask,tmp,.git} "url_for" .  2>/dev/null

