from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from pathlib import Path
from zipfile import ZipFile

font_path = input("Enter variable font path: ").strip()

font = TTFont(font_path)

if "fvar" not in font:
    print("This is not a variable font.")
    exit()

output_dir = Path.home() / "storage" / "downloads" / "FreezeFont"
output_dir.mkdir(parents=True, exist_ok=True)

family_name = "Font"

try:
    for record in font["name"].names:
        if record.nameID == 1:
            family_name = record.toUnicode()
            break
except:
    pass

instances = font["fvar"].instances

generated_files = []

print(f"\nFound {len(instances)} instances\n")

for instance in instances:

    coords = instance.coordinates

    static_font = TTFont(font_path)

    static_font = instantiateVariableFont(
        static_font,
        coords,
        inplace=False
    )

    # Convert from WOFF2 to real TTF
    static_font.flavor = None

    # Remove variable font tables
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

    weight = list(coords.values())[0]

    filename = f"{family_name}-{weight}.ttf"

    output_file = output_dir / filename

    static_font.save(str(output_file))

    generated_files.append(output_file)

    print(f"Generated: {filename}")

# Create ZIP file
zip_path = output_dir / f"{family_name}.zip"

with ZipFile(zip_path, "w") as zip_file:
    for file in generated_files:
        zip_file.write(
            file,
            arcname=file.name
        )

print("\nDone!")
print(f"ZIP created: {zip_path}")
print(f"Saved to: {output_dir}")
