#!/bin/csh

set exp=nameExp
set exe=../versionAdeli/bin/adeli

set run=1
set export=1

if ( $run ) then
  $exe <<fin 
$exp
1
fin
endif
