# CS 6120

Working through the [Cornell CS 6120 Advanced Compilers course][course].

To see some pretty control-flow graphs:
```bash
dot lesson2/test/asm$(shuf -en1 0 1 2).out -Tpng -o cfg.png
```
Or to run some probably-boring checks:
```bash
./checks.sh
```

[course]: https://www.cs.cornell.edu/courses/cs6120/2020fa/self-guided/
