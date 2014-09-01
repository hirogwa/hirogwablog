plain-blog
===========
A simple Django application to host a blog.

## Installation
* Project settings
  * add the blog app
  * define `STATIC_URL`, `STATIC_ROOT` for css/js/images storage
  * define `MEDIA_URL`, `MEDIA_ROOT` for image storage
* Nginx
  * define locations `/static/`, `/media/`, accordingly in the nginx.conf
