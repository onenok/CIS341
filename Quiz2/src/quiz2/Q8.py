from math import gcd


def main() -> None:
	n = 2026

	gcd_values = [gcd(i, n) for i in range(1, n + 1)]
	s = sum(gcd_values)
	c = sum(value == 1 for value in gcd_values)

	print(f"S = {s}")
	print(f"C = {c}")

	assert s == 6075
	assert c == 1012


if __name__ == "__main__":
	main()
