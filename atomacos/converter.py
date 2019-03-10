from collections import namedtuple

from CoreFoundation import CFGetTypeID, CFArrayGetTypeID
from ApplicationServices import (
    AXUIElementGetTypeID,
    AXValueGetType,
    kAXValueCGSizeType,
    kAXValueCGPointType,
    kAXValueCFRangeType,
    NSSizeFromString,
    NSPointFromString,
    NSRangeFromString,
)
import re


class Converter:
    def __init__(self, axuielementclass=None):
        self.app_ref_class = axuielementclass

    def convert_value(self, value):
        if CFGetTypeID(value) == AXUIElementGetTypeID():
            return self.convert_app_ref(value)
        if CFGetTypeID(value) == CFArrayGetTypeID():
            return self.convert_list(value)
        if AXValueGetType(value) == kAXValueCGSizeType:
            return self.convert_size(value)
        if AXValueGetType(value) == kAXValueCGPointType:
            return self.convert_point(value)
        if AXValueGetType(value) == kAXValueCFRangeType:
            return self.convert_range(value)
        else:
            return value

    def convert_list(self, value):
        return [self.convert_value(item) for item in value]

    def convert_app_ref(self, value):
        return self.app_ref_class(value)

    def convert_size(self, value):
        repr_searched = re.search("{.*}", str(value)).group()
        CGSize = namedtuple("CGSize", ["width", "height"])
        size = NSSizeFromString(repr_searched)

        return CGSize(size.width, size.height)

    def convert_point(self, value):
        repr_searched = re.search("{.*}", str(value)).group()
        CGPoint = namedtuple("CGPoint", ["x", "y"])
        point = NSPointFromString(repr_searched)

        return CGPoint(point.x, point.y)

    def convert_range(self, value):
        repr_searched = re.search("{.*}", str(value)).group()
        CFRange = namedtuple("CFRange", ["location", "length"])
        range = NSRangeFromString(repr_searched)

        return CFRange(range.location, range.length)