##############################################################################
#             Makefile for Python scripts for Adeli                             #
#----------------------------------------------------------------------------#

##############################################################################
# Define exec name and obj directory:
#-----------------------------------------------------------------------------

PS2P := creeepy2p.ps
PDF2P := creeepy2p.pdf

PS := creeepy.ps
PDF := creeepy.pdf

##############################################################################
# Source and object files:
#-----------------------------------------------------------------------------

SRCS := `find ~/RhEoVOLUTION/CODES/SCRIPTS/creeepy -type f -name "*.py"`

##############################################################################
# Make a pdf : 

SRCS += makefile

write:
	enscript -2r --line-numbers --highlight=fortran --toc --fancy-header=header $(SRCS) -o $(PS2P)
	gs -sDEVICE=pdfwrite -o $(PDF2P) $(PS2P)

print:
	enscript -MA4 --line-numbers --highlight=fortran --toc --fancy-header=headerB5 -fCourier8.5 $(SRCS) -o $(PS)
	gs -sDEVICE=pdfwrite -o $(PDF) $(PS)
	#gs -q -sDEVICE=pdfwrite -dBATCH -dNOPAUSE -sOutputFile=print.pdf \
	-dDEVICEWIDTHPOINTS=595 -dDEVICEHEIGHTPOINTS=842 -dFIXEDMEDIA \ -c "<< /CurrPageNum 1 def /Install { /CurrPageNum CurrPageNum 1 add def CurrPageNum 2 mod 1 eq {} {96 0 translate} ifelse } bind  >> setpagedevice " -f "out.pdf"
	#rm out.pdf
	

##############################################################################
# Delete objects:
#-----------------------------------------------------------------------------

clean:
	/bin/rm $(DIROBJ)/*.o

cleanmod:
	/bin/rm $(DIROBJ)/*.mod

all:
	@echo $(OBJS)  
