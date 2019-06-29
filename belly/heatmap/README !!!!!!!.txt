The file "FinalFixed.json" should be either accessed via a local web server ( with the command: python -m http.server 8888 & )
or be uploaded to a remote host which supports direct download.
After that, you could disable Chrome or Firefox's security measure called "Same Origin Policy". Then it works.

**** NOTE : this solution is indeed dirty. I wanted to do this quickly, so i did not look for a clean solution. You could always search for a better one.
 
Firefox Extension which disables Same Origin Policy: 
https://addons.mozilla.org/en-US/firefox/addon/cors-everywhere/

Remote hosting for tiny files, keeps files for 24 hours:
https://uguu.se/