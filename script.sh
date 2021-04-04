#! /bin/sh
find / -mount -type f -print0 | xargs -0 du -h | sort -rh | head -n 10
