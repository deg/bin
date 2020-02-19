sudo service smbd stop && sudo service nmbd stop

docker run -it -p 139:139 -p 445:445 -d dperson/samba \
       -s "centralpirk;/centralPark"


#            -u "example1;badpass" \
#            -u "example2;badpass" \
#            -s "public;/share" \
#            -s "users;/srv;no;no;no;example1,example2" \
#            -s "example1 private share;/example1;no;no;no;example1" \
#            -s "example2 private share;/example2;no;no;no;example2"
