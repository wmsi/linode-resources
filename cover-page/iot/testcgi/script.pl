#!/usr/bin/perl
use CGI;	#CGI.pm module that handles taking form input and turning them into perl variables

my $q= new CGI;	#$query now has the submitted form details (if any)

print "Content-type: text/html\n\n";	#2 newlines are needed to tell Apaache that the header is done.  Data will follow.
#print $q->header('text/html');	#same as above

print "hi<p>\n";

#we know what the variables used in the form are, so we could access them directly by using $q->param('button1');
#we'll pretend otherwise and get a list of all submitted variables.  If you tweak the url, you can add new key/value
#pairs like this: script.pl?textVar=hjola&radioVar=bravo&button1=Jump&button99=foobar&lastName=Lincoln 
my @submittedParams = $q->param();

#The data from $q->param is really just unpacked from an environmental variable:
#print $ENV{QUERY_STRING}, "<br>\n";


#spit back out whatever submitted.
foreach $paramName (@submittedParams) {
	print "$paramName -- ", $q->param($paramName), "<br>\n";
}

$action = $q->param('button1');
#hash of commands we may be given.
%COMMANDS = ('Jump' => 'move up 3',
		'Walk' => 'move forward 3');

	# the backticks '`' perform a shell operation.  
	# the "right" way to do this would be to do an open(FILE, ">>outfile.txt") and print FILE, etc.
	# this is simpiler for now.
	# it does not need to begin with 'print'., but if there is any output it will be shown to the screen/browser.
	# that may happen if there is an error executing the command, like if the write permissions on outfile.txt
	# were wrong.
print `echo $COMMANDS{$action} >> outfile.txt`;
print "<p>\n";
print "<a href=page.html>Back</a> || <a href=outfile.txt>Outfile.txt</a>\n";

exit;






