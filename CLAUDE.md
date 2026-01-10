# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CirclePrints is a repository for generating parametric, 3D-printable items using Python and the build123d library.

## Technical Requirements

### Core Library
- **build123d**: Primary CAD library for generating 3D models
  - Prefer **Algebra mode** for all designs
  - Use `ocp_vscode` for visualization

### 3D Printing Constraints
- **Build Plate**: 256x256mm
  - Target total assembly length: <250mm to ensure fit
- **Printer Type**: FDM (Fused Deposition Modeling)
  - Design for printing **without supports**
  - Add chamfers on overhangs to prevent support requirements
  - Place text on top faces only (avoid underside text)

## Design Principles

When creating parametric models:
1. Use build123d Algebra mode syntax
2. Design all parts to be support-free for FDM printing
3. Apply chamfers/fillets to eliminate overhangs >45°
4. Ensure final assembly fits within 250mm length constraint
5. Position embossed text on upward-facing surfaces

## Current Design: Circular Plate with Cylinder

The initial design is a circular plate with a concentric cylinder:

**Base Plate:**
- Shape: Circular
- Default diameter: 11mm (variable parameter)
- Thickness: 1mm

**Cylinder:**
- Positioned concentrically on top of the plate
- Default diameter: 4mm (variable parameter)
- Height: 10mm (variable parameter)
- Through-hole: 1mm diameter (variable, set to 0 for solid)
- Embossed diameter text on top face (0.8mm height)
- Total assembly height: 11.8mm (plate + cylinder + text)

**Parameters:**
- `plate_diameter`: Default 11mm
- `cylinder_diameter`: Default 4mm
- `cylinder_height`: Default 10mm
- `plate_thickness`: 1mm (fixed)
- `hole_diameter`: Default 1mm (0 for solid cylinder)
- Embossed text height: 0.8mm (fixed)

**CLI Usage:**
```bash
python circular_plate_cone.py -p 11 -c 4                    # defaults (with 1mm hole)
python circular_plate_cone.py --hole-diameter 0             # solid cylinder, no hole
python circular_plate_cone.py -p 20 -c 8 --hole-diameter 3  # custom sizes with 3mm hole
python circular_plate_cone.py --help                        # show all options
```

**Features:**
- Automatic embossed plate diameter labeling on cylinder top
- Configurable through-hole (default 1mm, set to 0 for solid)
- Font size scales with cylinder diameter to fit properly (40% of cylinder diameter)
- Deeper embossed text (0.8mm) for better visibility during printing
- Support-free FDM printing (text on top face, hole runs straight through)

## Role

Act as a Senior Mechanical Design Engineer when creating designs in this repository.
