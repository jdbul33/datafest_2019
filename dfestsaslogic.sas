/* Generated Code (IMPORT) */
/* Source File: fuckthissasshit.csv */
/* Source Path: /home/craiggarzella0/sasuser.v94 */
/* Code generated on: 3/30/19, 11:07 PM */

%web_drop_table(WORK.IMPORT);


FILENAME REFFILE '/home/craiggarzella0/sasuser.v94/d_fest_IV.csv';

PROC IMPORT DATAFILE=REFFILE
	DBMS=CSV
	OUT=WORK.IMPORT;
	GETNAMES=YES;
RUN;

PROC CONTENTS DATA=WORK.IMPORT; RUN;


%web_open_table(WORK.IMPORT);

data rugby;
set work.import;
run;


proc syslin data = rugby 2sls first; 
endogenous tacklingindexsecondz;
instruments AcuteLoad ChronicLoad;
model Victory = Soreness tacklingindexsecondz;
run;
