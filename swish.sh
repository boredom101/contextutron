#!/bin/bash

SPLASH="OFF"
while getopts "t:s:xh" opt; do
  case ${opt} in
    h ) echo "Usage: swish -t <theme> [-s <icon size>] [-x]"
        exit 0
      ;;
    t ) THEME="$OPTARG"
      ;;
    s )
        SIZE="$OPTARG"
      ;;
    x )
        SPLASH="ON"
      ;;
  esac
done

if (( $OPTIND == 1 )); then
   echo "Usage: swish -t <theme> [-s <icon size>] [-x]"
   exit 0
fi

./pid.sh | python3 main.py $THEME $SIZE $SPLASH
