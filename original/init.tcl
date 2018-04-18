##########
## JACK493 INIT SCRIPT
## 18-1 PSYC493
## JACK 'jryzkns' ZHOU 2018
##########

### SETTING VARIABLES

## DECLARATIONS

# as Per Bert Tradition, collect all variables
SimSelectDataCollectionElements ALL  

# Boolean variable to determine whether if subject is in Curved Trial
# USAGE: When subject vehicle enters curved trial, inCurv is negated
# Curved trials begin when in contact with triggers of the form: direction-number-direction
# ex. RT4OUT is the exit to the 4th right turn trial
# in triggers, the command issued is:
# SimSetUserData inCurv 0 (or 1)
SimCreateDataCollectionElement inCurv  

# Integral variable in the natural numbers to denote how many laps has been completed.
# an internal TCL variable is specified and incremented, the external outfile variable will be updated right after. 
# USAGE: When $lap (the amount of laps completed) is 5, experiment exits
SimCreateDataCollectionElement lap

# collect all specified variables at 60 Hz
SimCollectData On 60 NONE  

## SPECIFYING VALUES

set lapCount 0
SimSetUserData lap $lapCount 
SimSetUserData inCurv 0 


########## TOP ##########

#Virtual Trigger for Checking if the experiment is done
VTriggerCreate CheckForEnd {
	# If participant has completed 5 laps, then exit the experiment
	if  {$lapCount == 5} {
		SimExit
	}
}

VTriggerAdd CheckForEnd 1 Hz 

#space for more calls but we are now done!