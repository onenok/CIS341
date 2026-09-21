from pathlib import Path

import numpy as np
from PIL import Image


def build_image() -> np.ndarray:
	"""Build the requested 1080-by-1920 RGB image."""
	rows, columns = 1080, 1920

	y = np.arange(rows, dtype=np.int32)[:, np.newaxis]
	x = np.arange(columns, dtype=np.int32)[np.newaxis, :]

	red = (x + y) % 256
	green = (x * y) % 256
	blue = 255 - red

	return np.stack((red, green, blue), axis=2).astype(np.uint8)


def main() -> None:
	image_array = build_image()
	output_path = Path(__file__).with_name("Q9.png")
	Image.fromarray(image_array, mode="RGB").save(output_path)

	print(f"Saved {output_path}")
	print(f"Shape: {image_array.shape}")


if __name__ == "__main__":
	main()
