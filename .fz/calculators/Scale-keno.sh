#!/bin/bash

# Scale-keno calculator script
# Compatible with fz framework

# Check for SCALE installation
if [ -z "$SCALE_HOME" ]; then
    export SCALE_HOME="/SCALE/scale6.2"
fi
export CMDS=${SCALE_HOME}/bin

# if directory as input, cd into it
if [ -d "$1" ]; then
  cd "$1"
  # Find the first input file (not .out or .msg)
  input=$(ls | grep -v '\.out$' | grep -v '\.msg$' | grep -v '\.sh$' | head -n 1)
  if [ -z "$input" ]; then
    echo "No input file found in directory. Exiting."
    exit 1
  fi
  shift
# if $1 is a file, use it
elif [ -f "$1" ]; then
  input="$1"
  shift
else
  echo "Usage: $0 <input_file or input_directory>"
  exit 2
fi

PID_FILE=$PWD/PID
echo $$ >> $PID_FILE

output="$(basename $input).out"
msgs="$(basename $input).msg"

${CMDS}/scalerte $input $output > $msgs 2>&1 &

PID_SCALE=$!
echo $PID_SCALE >> $PID_FILE
wait $PID_SCALE

# test for "congratulations" message in output for csas5/csas6
if [[ (`grep "=csas[56]" $input 2>/dev/null | wc -l` == "1" ) ]]
then
    echo "Testing congratulations..."
    if [ `grep "Congratulations" *.out 2>/dev/null | wc -l` == "0" ]
    then
        echo "Error: no congratulations !"
        if [ -f $PID_FILE ]; then
            rm -f $PID_FILE
        fi
        exit 1
    else
        echo "OK: Congratulations returned."
    fi
fi

if [ -f $PID_FILE ]; then
    rm -f $PID_FILE
fi
