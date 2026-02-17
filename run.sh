#!/usr/bin/env bash
# Run circular_plate_cone.py, suppressing pyparsing deprecation warnings from cadquery
DIR="$(cd "$(dirname "$0")" && pwd)"
python "$DIR/circular_plate_cone.py" "$@" 2> >(grep -v -E 'PyparsingDeprecation|oneOf|setParseAction|infixNotation|delimitedList|setResultsName' >&2)
