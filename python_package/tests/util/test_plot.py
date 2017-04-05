import unittest
import unittest.mock as mock


class PlotTest(unittest.TestCase):
    def setUp(self):
        modules = {
            'matplotlib': mock.Mock(),
            'matplotlib.pyplot':  mock.Mock(),
            'cartopy': mock.Mock(),
            'cartopy.crs': mock.Mock(),
            'cartopy.io': mock.Mock(),
            'cartopy.io.img_tiles': mock.Mock()
        }

        self.module_patcher = mock.patch.dict('sys.modules', modules)
        self.module_patcher.start()

        from pytraffic.collectors.util import plot
        self.plot = plot

    def test_generate(self):
        mock_plt = mock.Mock()
        self.plot.plt = mock_plt
        pom = self.plot.PlotOnMap([1, 2], [3, 4], 'title')
        pom.generate((10, 10), 100, 15, 5)

        mock_plt.figure.assert_called_with(figsize=(10, 10), dpi=100)
        args, kwargs = mock_plt.plot.call_args
        self.assertEqual(args[0], [1, 2])
        self.assertEqual(args[1], [3, 4])
        self.assertEqual(kwargs['markersize'], 5)
        mock_plt.title.assert_called_with('title')

    def test_label(self):
        mock_plt = mock.Mock()
        self.plot.plt = mock_plt
        pom = self.plot.PlotOnMap([1, 2], [3, 4], 'title')
        pom.label(['a', 'b'], (0.1, 0.2), 10)

        self.assertEqual(mock_plt.text.call_count, 2)

        args1, kwargs1 = mock_plt.text.call_args_list[0]
        self.assertEqual(args1[0], 1.1)
        self.assertEqual(args1[1], 3.2)
        self.assertEqual(args1[2], 'a')
        self.assertEqual(kwargs1['fontsize'], 10)

        args2, kwargs2 = mock_plt.text.call_args_list[1]
        self.assertEqual(args2[0], 2.1)
        self.assertEqual(args2[1], 4.2)
        self.assertEqual(args2[2], 'b')
        self.assertEqual(kwargs2['fontsize'], 10)

    @mock.patch('pytraffic.collectors.util.plot.files')
    def test_save(self, mock_files):
        mock_plt = mock.Mock()
        self.plot.plt = mock_plt
        pom = self.plot.PlotOnMap([1, 2], [3, 4], 'title')
        pom.save('/test1/', 'file_name')
        mock_plt.savefig.assert_called_with('/test1/file_name',
                                            bbox_inches='tight')

if __name__ == '__main__':
    unittest.main()
