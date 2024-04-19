import math
import pathlib
import typing

from ipyniivue._constants import (
    _SNAKE_TO_CAMEL_OVERRIDES,
    DragMode,
    MuliplanarType,
    SliceType,
)

RENAME_OVERRIDES = {v: k for k, v in _SNAKE_TO_CAMEL_OVERRIDES.items()}


def camel_to_snake(name: str):
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")


def type_hint(value: typing.Any):
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, tuple):
        return "tuple"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    elif isinstance(value, SliceType):
        return "SliceType"
    elif isinstance(value, MuliplanarType):
        return "MuliplanarType"
    elif isinstance(value, DragMode):
        return "DragMode"
    else:
        return "typing.Any"


def get_value(value: typing.Any):
    if isinstance(value, float) and math.isnan(value):
        return 'float("nan")'
    if value == float("inf"):
        return 'float("inf")'
    if isinstance(value, SliceType):
        return f"SliceType.{value.name}"
    if isinstance(value, MuliplanarType):
        return f"MuliplanarType.{value.name}"
    if isinstance(value, DragMode):
        return f"DragMode.{value.name}"
    if isinstance(value, str):
        # double quote
        return f'"{value}"'
    return repr(value)


def generate_mixin(options: typing.Dict[str, typing.Any]):
    lines = [
        "# This file is automatically generated by scripts/generate_options_mixin.py",
        "# Do not edit this file directly",
        "from __future__ import annotations",
        "",
        "import typing",
        "",
        "from ._constants import SliceType, MuliplanarType, DragMode",
        "",
        '__all__ = ["OptionsMixin"]',
        "",
        "class OptionsMixin:",
    ]
    for option, value in options.items():
        snake_name = RENAME_OVERRIDES.get(option, camel_to_snake(option))
        hint = type_hint(value)
        lines.append("    @property")
        lines.append(f"    def {snake_name}(self) -> {hint}:")
        lines.append(f'        return self._opts.get("{option}", {get_value(value)})')
        lines.append("")
        lines.append(f"    @{snake_name}.setter")
        lines.append(f"    def {snake_name}(self, value: {hint}):")
        lines.append(f'        self._opts = {{**self._opts, "{option}": value}}')
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    # Copied from niivue (should be able to automatically generate this)
    DEFAULT_OPTIONS = {
        "textHeight": 0.06,
        "colorbarHeight": 0.05,
        "crosshairWidth": 1,
        "rulerWidth": 4,
        "show3Dcrosshair": False,
        "backColor": (0, 0, 0, 1),
        "crosshairColor": (1, 0, 0, 1),
        "fontColor": (0.5, 0.5, 0.5, 1),
        "selectionBoxColor": (1, 1, 1, 0.5),
        "clipPlaneColor": (0.7, 0, 0.7, 0.5),
        "rulerColor": (1, 0, 0, 0.8),
        "colorbarMargin": 0.05,
        "trustCalMinMax": True,
        "clipPlaneHotKey": "KeyC",
        "viewModeHotKey": "KeyV",
        "doubleTouchTimeout": 500,
        "longTouchTimeout": 1000,
        "keyDebounceTime": 50,
        "isNearestInterpolation": False,
        "isResizeCanvas": True,
        "isAtlasOutline": False,
        "isRuler": False,
        "isColorbar": False,
        "isOrientCube": False,
        "multiplanarPadPixels": 0,
        "multiplanarForceRender": False,
        "isRadiologicalConvention": False,
        "meshThicknessOn2D": float("inf"),
        "dragMode": DragMode.CONTRAST,
        "yoke3Dto2DZoom": False,
        "isDepthPickMesh": False,
        "isCornerOrientationText": False,
        "sagittalNoseLeft": False,
        "isSliceMM": False,
        "isV1SliceShader": False,
        "isHighResolutionCapable": True,
        "logLevel": "info",
        "loadingText": "waiting for images...",
        "isForceMouseClickToVoxelCenters": False,
        "dragAndDropEnabled": True,
        "drawingEnabled": False,
        "penValue": 1,
        "floodFillNeighbors": 6,
        "isFilledPen": False,
        "thumbnail": "",
        "maxDrawUndoBitmaps": 8,
        "sliceType": SliceType.MULTIPLANAR,
        "meshXRay": 0.0,
        "isAntiAlias": None,
        "limitFrames4D": float("nan"),
        "isAdditiveBlend": False,
        "showLegend": True,
        "legendBackgroundColor": (0.3, 0.3, 0.3, 0.5),
        "legendTextColor": (1.0, 1.0, 1.0, 1.0),
        "multiplanarLayout": MuliplanarType.AUTO,
        "renderOverlayBlend": 1.0,
    }
    code = generate_mixin(DEFAULT_OPTIONS)
    loc = pathlib.Path(__file__).parent / "../src/ipyniivue/_options_mixin.py"
    loc.write_text(code)
