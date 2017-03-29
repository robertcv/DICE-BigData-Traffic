import unittest
import unittest.mock as mock

from pytraffic.collectors.util import files


@mock.patch('pytraffic.collectors.util.files.os')
class FilesTest(unittest.TestCase):
    @mock.patch('pytraffic.collectors.util.files.time')
    def test_old_or_not_exists(self, mock_time, mock_os):
        mock_os.path.isfile.return_value = False

        self.assertTrue(files.old_or_not_exists('any path', 0))

        mock_os.path.isfile.return_value = True
        mock_os.path.getmtime.return_value = 1490354200
        mock_time.time.return_value = 1490354300

        self.assertFalse(files.old_or_not_exists('any path', 150))

        self.assertTrue(files.old_or_not_exists('any path', 50))

    def test_file_path(self, mock_os):
        mock_os.path.realpath.return_value = '/test1/test2.txt'
        mock_os.path.dirname.return_value = '/test1'

        files.file_path('/test1/test2.txt', 'image1/image2.png')

        mock_os.path.realpath.assert_called_once_with('/test1/test2.txt')
        mock_os.path.dirname.assert_called_once_with('/test1/test2.txt')
        mock_os.path.join.assert_called_once_with('/test1', 'image1/image2.png')

    def test_directory_exists_or_make(self, mock_os):
        mock_os.path.exists.return_value = True
        files.directory_exists_or_make("any path")

        self.assertFalse(mock_os.makedirs.called)

        mock_os.path.exists.return_value = False
        files.directory_exists_or_make("any path")

        mock_os.makedirs.assert_called_once_with("any path")


if __name__ == '__main__':
    unittest.main()
