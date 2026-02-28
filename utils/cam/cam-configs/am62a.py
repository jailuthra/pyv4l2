import v4l2
from pixutils import formats

imx219_w = 2592
imx219_h = 1944
#imx219_w = 1312
#imx219_h = 972
imx219_bus_fmt = v4l2.BusFormat.SRGGB8_1X8
imx219_pix_fmt = v4l2.PixelFormats.SRGGB8
imx219_bus_fmt = v4l2.BusFormat.SRGGB12_1X12
imx219_pix_fmt = v4l2.PixelFormats.SRGGB12
imx219_bus_fmt = v4l2.BusFormat.SRGGB10_1X10
imx219_pix_fmt = v4l2.PixelFormats.SRGGB10

mbus_fmt_imx219 = (imx219_w, imx219_h, imx219_bus_fmt)
fmt_pix_imx219 = (imx219_w, imx219_h, imx219_pix_fmt)

imx219_meta_w = imx219_w
imx219_meta_h = 2
#imx219_meta_bus_fmt = v4l2.BusFormat.META_8
#imx219_meta_pix_fmt = v4l2.MetaFormat.GENERIC_8
imx219_meta_bus_fmt = v4l2.BusFormat.META_10
imx219_meta_pix_fmt = v4l2.MetaFormats.GENERIC_CSI2_10

meta_mbus_fmt_imx219 = (imx219_meta_w, imx219_meta_h, imx219_meta_bus_fmt)
meta_fmt_pix_imx219 = (imx219_meta_w, imx219_meta_h, imx219_meta_pix_fmt)

configurations = {}

sensor_ent = 'imx335 4-001a'
#sensor_ent = 'imx219 4-0010'

configurations['cam0'] = {
    'media': ('TI-CSI2RX', 'model'),

    'subdevs': [
        # Camera
        {
            'entity': sensor_ent,
            'pads': [
                { 'pad': (0, 0), 'fmt': mbus_fmt_imx219 },
            ],
#            "routing": [
#               { "src": (1, 0), "dst": (0, 0) },
#            ],
            'controls': [
                (v4l2.uapi.V4L2_CID_EXPOSURE, 5300),
                (v4l2.uapi.V4L2_CID_VBLANK, 2556),
                (v4l2.uapi.V4L2_CID_ANALOGUE_GAIN, 40),
                (v4l2.uapi.V4L2_CID_VFLIP, 0),
                # (v4l2.uapi.V4L2_CID_DIGITAL_GAIN, 0),
            ],
        },
        # CSI-2 RX
        {
            'entity': 'cdns_csi2rx.30101000.csi-bridge',
#            "routing": [
#                { "src": (0, 0), "dst": (1, 0) },
#            ],
            'pads': [
                { 'pad': (0, 0), 'fmt': mbus_fmt_imx219 },
                { 'pad': (1, 0), 'fmt': mbus_fmt_imx219 },
            ],
        },
    ],

    'devices': [
        {
            'entity': 'j721e-csi2rx',
            'fmt': fmt_pix_imx219,
        },
    ],

    'links': [
        { 'src': (sensor_ent, 0), 'dst': ('cdns_csi2rx.30101000.csi-bridge', 0) },
        { 'src': ('cdns_csi2rx.30101000.csi-bridge', 1), 'dst': ('j721e-csi2rx', 0) },
    ],
}

configurations['cam0-new'] = {
    'media': ('TI-CSI2RX', 'model'),

    'kms_format': formats.pixelformats.PixelFormats.NV12,
    'subdevs': [
        # Camera
        {
            'entity': sensor_ent,
            'pads': [
                { 'pad': (0, 0), 'fmt': mbus_fmt_imx219 },
            ],
#            "routing": [
#               { "src": (1, 0), "dst": (0, 0) },
#            ],
        },
        # CSI-2 RX
        {
            'entity': 'cdns_csi2rx.30101000.csi-bridge',
#            "routing": [
#                { "src": (0, 0), "dst": (1, 0) },
#            ],
            'pads': [
                { 'pad': (0, 0), 'fmt': mbus_fmt_imx219 },
                { 'pad': (1, 0), 'fmt': mbus_fmt_imx219 },
            ],
        },
        {
            'entity': '30102000.ticsi2rx',
#            "routing": [
#                { "src": (0, 0), "dst": (1, 0) },
#            ],
            'pads': [
                { 'pad': (0, 0), 'fmt': mbus_fmt_imx219 },
                { 'pad': (1, 0), 'fmt': mbus_fmt_imx219 },
            ],
        },

    ],

    'devices': [
        {
            'entity': '30102000.ticsi2rx context 0',
            'fmt': fmt_pix_imx219,
        },
    ],

    'links': [
        { 'src': (sensor_ent, 0), 'dst': ('cdns_csi2rx.30101000.csi-bridge', 0) },
        { 'src': ('cdns_csi2rx.30101000.csi-bridge', 1), 'dst': ('30102000.ticsi2rx', 0) },
        { 'src': ('30102000.ticsi2rx', 1), 'dst': ('30102000.ticsi2rx context 0', 0) },
    ],
}

def get_configs():
    return (configurations, ['cam0'])
