import json
import os
import random
import argparse

# Define the materials, shapes, and default configuration ranges
MATERIALS = ["copper", "FR4", "vacuum"]
SHAPE_TYPES = ["rectangle", "circle"]
CELL_WIDTH = 2.5  # mm
SUBSTRATE_HEIGHT = 0.25  # mm
RAD_LENGTH = 2.51  # mm
RAD_WIDTH = 2.51  # mm
RAD_HEIGHT = 2.51  # mm
PATCH_THICKNESS = 0.017  # mm
POSITION_RANGE = (-CELL_WIDTH / 2, CELL_WIDTH / 2)  # mm
SIZE_RANGE = (0.1, CELL_WIDTH / 2)  # mm
RADIUS_RANGE = (0.1, CELL_WIDTH / 2)  # mm
FREQUENCY_START = 5  # GHz
FREQUENCY_STOP = 15  # GHz
SOLUTION_FREQUENCY = 10  # GHz

def round_value(value, decimals=3):
    """Round the value to the specified number of decimal places."""
    return round(value, decimals)

def generate_random_dimensions(shape_type):
    """Generate random dimensions based on the shape type."""
    if shape_type == "rectangle":
        return {
            "position": [f"{round_value(random.uniform(-CELL_WIDTH / 2, CELL_WIDTH / 2))}mm" for _ in range(2)] + ["0mm"],
            "size": [f"{round_value(random.uniform(0.1, CELL_WIDTH / 2))}mm" for _ in range(2)],
        }
    elif shape_type == "circle":
        return {
            "position": [f"{round_value(random.uniform(-CELL_WIDTH / 2, CELL_WIDTH / 2))}mm" for _ in range(2)] + ["0mm"],
            "radius": f"{round_value(random.uniform(0.1, CELL_WIDTH / 2))}mm",
        }
    else:
        raise ValueError(f"Unsupported shape type: {shape_type}")

def generate_random_shape():
    """Generate a single random shape."""
    shape_type = random.choice(SHAPE_TYPES)
    dimensions = generate_random_dimensions(shape_type)
    return {
        "type": shape_type,
        "dimensions": dimensions,
        "material": "copper",  # Ensure the material is copper
        "name": f"{shape_type}_{random.randint(1, 1000)}"
    }

def generate_random_operation(shapes):
    """Generate a random operation (merge or subtract) based on the shapes."""
    operation_type = random.choice(["merge", "subtract"])
    if operation_type == "merge":
        selected_shapes = random.sample(shapes, 2)
        return {
            "type": "merge",
            "objects": [shape["name"] for shape in selected_shapes],
            "new_name": f"merged_{random.randint(1, 1000)}"
        }
    elif operation_type == "subtract":
        blank_shape = random.choice(shapes)
        tool_shape = random.choice([shape for shape in shapes if shape != blank_shape])
        return {
            "type": "subtract",
            "blank": blank_shape["name"],
            "tool": tool_shape["name"],
            "new_name": f"subtracted_{random.randint(1, 1000)}"
        }

def generate_random_json(file_path, num_shapes):
    """Generate a random JSON file with the specified number of shapes."""
    shapes = [generate_random_shape() for _ in range(num_shapes)]
    operations = [generate_random_operation(shapes) for _ in range(random.randint(1, 3))]

    data = {
        "geometry": {
            "cell_width": f"{CELL_WIDTH}mm",
            "substrate_height": f"{SUBSTRATE_HEIGHT}mm",
            "rad_length": f"{RAD_LENGTH}mm",
            "rad_width": f"{RAD_WIDTH}mm",
            "rad_height": f"{RAD_HEIGHT}mm",
            "patch_thickness": f"{PATCH_THICKNESS}mm"
        },
        "shapes": shapes,
        "operations": operations,
        "analysis": {
            "frequency_start": f"{FREQUENCY_START}GHz",
            "frequency_stop": f"{FREQUENCY_STOP}GHz",
            "solution_frequency": f"{SOLUTION_FREQUENCY}GHz"
        }
    }

    # Write the JSON data to the specified file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Generated JSON file: {file_path}")

def generate_multiple_json_files(output_dir, num_files, shapes_per_file):
    """Generate multiple JSON files with randomized content."""
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_files):
        file_path = os.path.join(output_dir, f"template_{i + 1}.json")
        generate_random_json(file_path, shapes_per_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random JSON files for design templates.")
    parser.add_argument("--output_dir", type=str, default="./design_generator/templates/", help="Output directory for JSON files")
    parser.add_argument("--num_files", type=int, default=5, help="Number of JSON files to generate")
    parser.add_argument("--shapes_per_file", type=int, default=3, help="Number of shapes per JSON file")

    args = parser.parse_args()

    generate_multiple_json_files(args.output_dir, args.num_files, args.shapes_per_file)

# Usage: python json_generator.py --output_dir ./design_generator/templates/ --num_files 5 --shapes_per_file 3