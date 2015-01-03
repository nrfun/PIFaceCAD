# PiFaceCAD.sh
# slightly  iffy work around to get our python 'driver' to be running (exec worked without this, spawn maybe not)

BASEDIR=$(dirname $0)
sudo python -u $BASEDIR/PIFaceCAD.py $@

