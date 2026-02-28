import v4l2

width=1920
height=1080
sensor_fmt = (width, height, v4l2.BusFormat.SRGGB10_1X10)
#isp_out_fmt = (1920, 1080, v4l2.BusFormat.YUYV8_2X8)
#resizer_out_fmt = (1920, 1080, v4l2.BusFormat.YUYV8_1_5X8)
vid_fmt = (width, height, v4l2.PixelFormats.SRGGB10)

configurations = {}

configurations['cam0'] = {
    'media': ('renesas,vin-r8a779g0', 'model'),

    'subdevs': [
        # Camera
        {
            'entity': 'imx219 1-0010',
            'pads': [
                { 'pad': (0, 0), 'fmt': sensor_fmt },
            ],
            'controls': [
                (v4l2.uapi.V4L2_CID_EXPOSURE, 1759),
                (v4l2.uapi.V4L2_CID_ANALOGUE_GAIN, 100),
                (v4l2.uapi.V4L2_CID_DIGITAL_GAIN, 0),
            ],
        },
        # CSI-2 RX
        {
            'entity': 'rcar_csi2 fe500000.csi2',
            'pads': [
                { 'pad': (0, 0), 'fmt': sensor_fmt },
                { 'pad': (1, 0), 'fmt': sensor_fmt },
            ],
        },

        {
            'entity': 'rcar_isp fed00000.isp',
            'pads': [
                { 'pad': (0, 0), 'fmt': sensor_fmt },
                { 'pad': (1, 0), 'fmt': sensor_fmt },
            ],
        },


    ],

    'devices': [
        {
            'entity': 'VIN0 output',
            'fmt': vid_fmt,
        },
    ],

    'links': [
        { 'src': ('imx219 1-0010', 0), 'dst': ('rcar_csi2 fe500000.csi2', 0) },
        { 'src': ('rcar_csi2 fe500000.csi2', 1), 'dst': ('rcar_isp fed00000.isp', 0) },
        { 'src': ('rcar_isp fed00000.isp', 1), 'dst': ('VIN0 output', 0) },
    ],
}

def get_configs():
    return (configurations, ['cam0'])
