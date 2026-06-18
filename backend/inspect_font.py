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

    instances = []

    for instance in font["fvar"].instances:

        instance_name = "Unknown"

        try:

            name_record = font["name"].getName(
                instance.subfamilyNameID,
                3,
                1,
                1033
            )

            if name_record:
                instance_name = str(name_record)

        except:
            pass

        instances.append({
            "name": instance_name
        })

    return {
        "is_variable": True,
        "family_name": family_name,
        "instance_count": len(instances),
        "axes": axes,
        "instances": instances
    }