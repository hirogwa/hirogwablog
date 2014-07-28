# coding: utf-8
import cmd
import getopt
import getpass
import urlparse
import urllib
import urllib2


class BlogCli(cmd.Cmd):

    URL_PUSH = '/blog/api/entry/'
    URL_ENTRY = '/blog/api/entry/'
    URL_TEMPLATE = '/blog/api/entry/new/'
    URL_ENTRY_LIST = '/blog/api/entry/list/'
    FILE_NEW_ENTRY = 'newentry.html'

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.host = ''

    def do_entrylist(self, line):
        if self.host == '':
            print 'host empty. call host command to set the target host'
            return False

        opts, args = getopt.getopt(line.split(), 'k:')

        keyword = ''
        for o, a in opts:
            if o == '-k':
                keyword = a

        if self.host == '':
            print 'host empty. call host command to set the target host'
            return False
        if keyword == '':
            url = urlparse.urljoin(self.host, BlogCli.URL_ENTRY_LIST)
            print 'recent post list with no filter'
        else:
            url = urlparse.urljoin(self.host, BlogCli.URL_ENTRY_LIST + keyword)
            print 'recent post list with filter: %s' % keyword

        print urllib2.urlopen(url).read()

    def do_host(self, line):
        self.host = line
        print 'host set to %s' % line

    def do_template(self, line):
        if self.host == '':
            print 'host empty. call host command to set the target host'
            return False

        url = urlparse.urljoin(self.host, BlogCli.URL_TEMPLATE)
        resp_body = urllib2.urlopen(url).read()
        f = open(BlogCli.FILE_NEW_ENTRY, 'w')
        f.write(resp_body)
        f.close()

    def do_entry(self, line):
        if self.host == '':
            print 'host empty. call host command to set the target host'
            return False

        url = urlparse.urljoin(self.host, BlogCli.URL_ENTRY + line)
        resp_body = urllib2.urlopen(url).read()
        f = open(line + '.html', 'w')
        f.write(resp_body)
        f.close()

    def do_push(self, line):
        filename = line

        if self.host == '':
            print 'host empty. call host command to set the target host'
            return False
        if filename == '':
            print 'filename unspecified'
            return False

        username = raw_input('Username: ')
        password = getpass.getpass('Password: ')

        url = urlparse.urljoin(self.host, BlogCli.URL_PUSH)

        with open(filename, 'r') as file_obj:
            data = file_obj.read()

        print 'publishing an entry for %s to %s from %s...' % (username, self.host, filename)

        postdata = dict(body=data, username=username, password=password)
        postdata_encoded = urllib.urlencode(postdata)
        req = urllib2.Request(url, postdata_encoded)
        resp = urllib2.urlopen(req)

        print resp

        return False

    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return self.do_exit(line)

    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt as e:
            print 'Exiting with keyboard interrupt'

if __name__ == '__main__':
    BlogCli().cmdloop()
