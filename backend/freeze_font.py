from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from pathlib import Path
from zipfile import ZipFile


def freeze_font(
    font_path,
    output_dir,
    mode="all",
    selected_styles=None
):

    if selected_styles is None:
        selected_styles = []

    font = TTFont(font_path)

    if "fvar" not in font:
        raise Exception("This is not a variable font")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    family_name = "Font"

    try:
        for record in font["name"].names:
            if record.nameID == 1:
                family_name = record.toUnicode()
                break
    except:
        pass

    generated_files = []

    instances = font["fvar"].instances

    if len(selected_styles) > 0:

        filtered_instances = []

        for instance in instances:

            instance_name = ""

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

            if instance_name in selected_styles:
                filtered_instances.append(
                    instance
                )

        instances = filtered_instances

    elif mode == "basic":

        filtered_instances = []

        allowed_keywords = [
            "Thin",
            "Light",
            "Regular",
            "SemiBold",
            "Bold",
            "Black",
            "Oblique"
        ]

        for instance in instances:

            instance_name = ""

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

            blocked_words = [
                "Condensed",
                "Expanded",
                "Contrast"
            ]

            blocked = False

            for word in blocked_words:
                if word in instance_name:
                    blocked = True

            if blocked:
                continue

            for keyword in allowed_keywords:
                if keyword in instance_name:
                    filtered_instances.append(
                        instance
                    )
                    break

        instances = filtered_instances

    for instance in instances:

        coords = instance.coordinates

        static_font = TTFont(font_path)

        static_font = instantiateVariableFont(
            static_font,
            coords,
            inplace=False
        )

        static_font.flavor = None

        for table in [
            "fvar",
            "gvar",
            "avar",
            "cvar",
            "HVAR",
            "MVAR",
            "VVAR",
            "STAT"
        ]:
            if table in static_font:
                del static_font[table]

        instance_name = "Font"

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

        safe_name = (
            instance_name
            .replace(" ", "-")
            .replace("/", "-")
        )

        filename = (
            f"{family_name}-{safe_name}.ttf"
        )

        output_file = (
            output_dir / filename
        )

        static_font.save(
            str(output_file)
        )

        generated_files.append(
            output_file
        )

    zip_name = (
        f"{family_name}-{mode}.zip"
    )

    zip_path = output_dir / zip_name

    with ZipFile(
        zip_path,
        "w"
    ) as zip_file:

        for file in generated_files:

            zip_file.write(
                file,
                arcname=file.name
            )

    return str(zip_path)