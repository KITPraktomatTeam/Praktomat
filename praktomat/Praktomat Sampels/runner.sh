(sleep 10;
 echo 
 echo
 echo ABBRUCH DURCH ZEITUEBERSCHREITUNG; 
 echo
 kill -9 $$) < /dev/null &

java \
 -Djava.security.manager \
 -Djava.security.policy=/dev/null \
 HelloWorld 2>&1 

status=$?
kill $!
exit $status