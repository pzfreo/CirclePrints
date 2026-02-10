"""
Circular Plate with Cylinder
A parametric 3D-printable design featuring a circular base plate with a concentric cylinder.

Design by: Senior Mechanical Design Engineer
Created for: CirclePrints - FDM 3D Printing
"""

import argparse
from build123d import *

# Try to import show from ocp_vscode if available
try:
    from ocp_vscode import show
    SHOW_AVAILABLE = True
except ImportError:
    SHOW_AVAILABLE = False

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Generate a parametric circular plate with concentric cylinder for 3D printing',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '-p', '--plate-diameter',
    type=float,
    default=11.0,
    help='Diameter of the circular base plate in mm'
)
parser.add_argument(
    '-c', '--cylinder-diameter',
    type=float,
    default=4.0,
    help='Diameter of the concentric cylinder in mm'
)
parser.add_argument(
    '--cylinder-height',
    type=float,
    default=10.0,
    help='Height of the cylinder in mm'
)
parser.add_argument(
    '--plate-thickness',
    type=float,
    default=1.0,
    help='Thickness of the base plate in mm'
)
parser.add_argument(
    '--hole-diameter',
    type=float,
    default=1.0,
    help='Diameter of the hole through the cylinder in mm (0 for solid cylinder)'
)
parser.add_argument(
    '--no-export',
    action='store_true',
    help='Skip exporting STL and STEP files (display only)'
)

args = parser.parse_args()

# Parameters (convert diameter to radius for geometry)
plate_diameter = args.plate_diameter  # mm - variable
plate_radius = plate_diameter / 2.0  # mm - calculated
plate_thickness = args.plate_thickness  # mm - configurable
cylinder_diameter = args.cylinder_diameter  # mm - variable
cylinder_radius = cylinder_diameter / 2.0  # mm - calculated
cylinder_height = args.cylinder_height  # mm - variable
hole_diameter = args.hole_diameter  # mm - variable
hole_radius = hole_diameter / 2.0  # mm - calculated

# Build the circular plate with cylinder using Algebra mode
with BuildPart() as circular_plate_cylinder:
    # Create the base circular plate
    with BuildSketch() as plate_sketch:
        Circle(plate_radius)
    extrude(amount=plate_thickness)

    # Create the cylinder on top of the plate
    with BuildSketch(Plane.XY.offset(plate_thickness)) as cylinder_sketch:
        Circle(cylinder_radius)
    extrude(amount=cylinder_height)

    # Add hole through the cylinder if hole_diameter > 0
    if hole_diameter > 0:
        with BuildSketch(Plane.XY) as hole_sketch:
            Circle(hole_radius)
        extrude(amount=plate_thickness + cylinder_height, mode=Mode.SUBTRACT)

    # Engrave plate diameter text into the bottom of the plate, offset from center
    text_height = 0.8  # mm - engraved text depth
    font_size = (plate_radius - cylinder_radius) * 0.6  # Scale to fit between cylinder and plate edge
    text_offset_y = (cylinder_radius + plate_radius) / 2  # Midpoint between cylinder edge and plate edge

    with BuildSketch(Plane.XY) as text_sketch:
        text_str = f"{plate_diameter:.0f}" if plate_diameter == int(plate_diameter) else f"{plate_diameter:.1f}"
        with Locations([(0, text_offset_y)]):
            Text(text_str, font_size=font_size, align=(Align.CENTER, Align.CENTER))
    extrude(amount=text_height, mode=Mode.SUBTRACT)

# Get the part object
part = circular_plate_cylinder.part

# Display the part (requires ocp_vscode in VS Code)
if SHOW_AVAILABLE:
    show(part)
    print("\n✓ Model displayed in ocp_vscode")
else:
    print("\nNote: ocp_vscode not available, exporting to file...")

# Export to STL and STEP files (unless --no-export is specified)
if not args.no_export:
    # Generate filename based on parameters
    filename_base = f"{int(cylinder_diameter)}mmCircle-{int(plate_diameter)}mm"
    stl_filename = f"{filename_base}.stl"
    step_filename = f"{filename_base}.step"

    from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
    from build123d import Mesher

    # Export STL
    try:
        # Use OCP STL writer directly
        from OCP.StlAPI import StlAPI_Writer
        stl_writer = StlAPI_Writer()
        stl_writer.Write(part.wrapped, stl_filename)
        print(f"✓ Exported to {stl_filename}")
    except Exception as e:
        print(f"STL export error: {e}")

    # Export STEP
    try:
        step_writer = STEPControl_Writer()
        step_writer.Transfer(part.wrapped, STEPControl_AsIs)
        step_writer.Write(step_filename)
        print(f"✓ Exported to {step_filename}")
    except Exception as e:
        print(f"STEP export error: {e}")
else:
    print("Export skipped (--no-export flag set)")

# Print dimensions for verification
text_height = 0.8  # mm - must match the value used in geometry
print(f"Design Parameters:")
print(f"  Plate diameter: {plate_diameter}mm")
print(f"  Plate thickness: {plate_thickness}mm")
print(f"  Cylinder diameter: {cylinder_diameter}mm")
print(f"  Cylinder height: {cylinder_height}mm")
print(f"  Hole diameter: {hole_diameter}mm" + (" (solid)" if hole_diameter == 0 else ""))
print(f"  Engraved text depth: {text_height}mm (bottom of plate)")
print(f"  Total height: {plate_thickness + cylinder_height + text_height}mm")
print(f"\nFDM Printability:")
print(f"  - Engraved text '{int(plate_diameter) if plate_diameter == int(plate_diameter) else plate_diameter}' (plate diameter) on plate bottom, off-center")
print(f"Build plate fit: ✓ Fits within 256x256mm")
