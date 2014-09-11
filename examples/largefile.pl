#!/usr/bin/perl

$| = 1;

print "Begin\n";

open OUT, ">", 'out.txt';
print OUT "x" x (1000*10);
close OUT;

print "End\n";

