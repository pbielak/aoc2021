def make_f(s1: int, div: int, s2: int):
    def f(w: int, z: int) -> int:
        cond = (z % 26 + s1) == w
        z = z // div

        if cond:
            return z
        else:
            return z * 26 + (w + s2)

    return f


def main():
    f0 = make_f(s1=14, div=1, s2=1)
    f1 = make_f(s1=15, div=1, s2=7)
    f2 = make_f(s1=15, div=1, s2=13)
    f3 = make_f(s1=-6, div=26, s2=10)
    f4 = make_f(s1=14, div=1, s2=0)
    f5 = make_f(s1=-4, div=26, s2=13)
    f6 = make_f(s1=15, div=1, s2=11)
    f7 = make_f(s1=15, div=1, s2=6)
    f8 = make_f(s1=11, div=1, s2=1)
    f9 = make_f(s1=0, div=26, s2=7)
    f10 = make_f(s1=0, div=26, s2=11)
    f11 = make_f(s1=-3, div=26, s2=14)
    f12 = make_f(s1=-9, div=26, s2=4)
    f13 = make_f(s1=-9, div=26, s2=10)


if __name__ == "__main__":
    main()
