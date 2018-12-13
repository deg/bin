# Restart gvfs, for when Samba connections fail
# See https://askubuntu.com/questions/996949/how-to-restart-gvfs
# (Used at least once in Ubuntu 16.04)

killall gvfsd
nautilus -q  # Close all Nautilus windows/instances
nautilus
