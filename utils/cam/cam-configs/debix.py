import v4l2

sensor_fmt = (1920, 1080, v4l2.BusFormat.SRGGB10_1X10)
isp_out_fmt = (1920, 1080, v4l2.BusFormat.YUYV8_2X8)
resizer_out_fmt = (1920, 1080, v4l2.BusFormat.YUYV8_1_5X8)
vid_fmt = (1920, 1080, v4l2.PixelFormats.NV21)

isp_crop = (0, 0, 1920, 1080)
resizer_crop = (0, 0, 1920, 1080)

configurations = {}

configurations['cam0'] = {
    'media': ('rkisp1', 'model'),

    'subdevs': [
        # Camera
        {
            'entity': 'imx219 1-0010',
            'pads': [
                { 'pad': (0, 0), 'fmt': sensor_fmt },
            ],
        },
        # CSI-2 RX
        {
            'entity': 'csis-32e40000.csi',
            'pads': [
                { 'pad': (0, 0), 'fmt': sensor_fmt },
                { 'pad': (1, 0), 'fmt': sensor_fmt },
            ],
        },

        {
            'entity': 'rkisp1_isp',
            'pads': [
                { 'pad': (0, 0), 'fmt': sensor_fmt,
                    'crop': isp_crop,
                },
                { 'pad': (2, 0), 'fmt': isp_out_fmt,
                    'crop': isp_crop,
                },
            ],
        },

        {
            'entity': 'rkisp1_resizer_mainpath',
            'pads': [
                { 'pad': (0, 0), 'fmt': isp_out_fmt,
                    'crop': resizer_crop,
                },
                { 'pad': (1, 0), 'fmt': resizer_out_fmt },
            ],
        },

    ],

    'devices': [
        {
            'entity': 'rkisp1_mainpath',
            'fmt': vid_fmt,
        },
    ],

    'links': [
        { 'src': ('imx219 1-0010', 0), 'dst': ('csis-32e40000.csi', 0) },
        { 'src': ('csis-32e40000.csi', 1), 'dst': ('rkisp1_isp', 0) },
        { 'src': ('rkisp1_isp', 2), 'dst': ('rkisp1_resizer_mainpath', 0) },
        { 'src': ('rkisp1_resizer_mainpath', 1), 'dst': ('rkisp1_mainpath', 0) },
    ],
}

def get_configs():
    return (configurations, ['cam0'])
