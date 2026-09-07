#!/bin/sh
# Macro Assembler AS (Alfred Arnold), installed under ~/opt/asl. Needed only to
# rebuild the CP/M 2.2 CCP/BDOS binaries in ~/Documents/degel/CPeMulator
# (`make cpm-binaries`); normal builds there use the committed binaries.
# AS_MSGPATH points the assembler at its message catalog, which is not on the
# default search path when the binary lives outside /usr/local.
AS_MSGPATH=/Users/deg/opt/asl exec /Users/deg/opt/asl/asl "$@"
