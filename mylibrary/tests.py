from django.test import TestCase

# Create your tests here.


class SyskTests(TestCase):
    def test_connect_pocast(self):
        ''''''
        from sysk import fetchRss
        feeds = fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
        self.assertIs(len(feeds) > 0, True)

    def test_send_new_mail(self):
        from mytoolkit import findAllDownloadFile
        from foo.Mail import sendNewFile
        for _, info in findAllDownloadFile().items():
            self.assertIs(sendNewFile(info.FullPath), True)
