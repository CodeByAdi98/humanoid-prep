if [ -z "$1" ]; then
    echo "usage: ./run.sh <output-file>"
    exit 1
fi
python3 week-02/day01.py > $1
