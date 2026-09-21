from Q9 import build_image


def main() -> None:
    image = build_image()

    g_mean = image[:, :, 1].mean()
    equal_pixels = (image[:, :, 0] == image[:, :, 1]).sum()

    print(f"(a) G channel mean: {g_mean:.2f}")
    print(f"(b) Number of pixels where R == G: {equal_pixels}")


if __name__ == "__main__":
    main()
