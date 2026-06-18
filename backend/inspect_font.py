from fontTools.ttLib import TTFont


def inspect_font(font_path):

    font = TTFont(font_path)

    if "fvar" not in font:
        return {
            "is_variable": False
        }

    family_name = "Unknown"

    try:
        for record in font["name"].names:
            if record.nameID == 1:
                family_name = record.toUnicode()
                break
    except:
        pass

    axes = []

    for axis in font["fvar"].axes:

        axes.append({
            "tag": axis.axisTag,
            "min": axis.minValue,
            "max": axis.maxValue,
            "default": axis.defaultValue
        })

    instance_count = len(
        font["fvar"].instances
    )

    return {
        "is_variable": True,
        "family_name": family_name,
        "instance_count": instance_count,
        "axes": axes
    }