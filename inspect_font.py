from fontTools.ttLib import TTFont

font_path = input("Enter font path: ")

font = TTFont(font_path)

print("\n=== FONT INFO ===")

if "fvar" not in font:
    print("This is not a variable font.")
    exit()

fvar = font["fvar"]

print("\nAxes:")
for axis in fvar.axes:
    print(
        f"{axis.axisTag}: "
        f"{axis.minValue} → {axis.maxValue} "
        f"(default {axis.defaultValue})"
    )

print("\nInstances:")
for instance in fvar.instances:
    coords = instance.coordinates
    print(coords)
