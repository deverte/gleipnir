# Gleipnir

## Description

Gleipnir is a program with graphical user interface for visualizing the results
of modeling the absorption of radiation by stellar and planetary matter.

![screenshot](assets/screenshot.png)

Compatible file format for parsing (commonly named as "AbsorpPlot.dat"):

```
nR <int>
nZ <int>
dr <float>
dz <float>
r0 <float>
z0 <float>
V1 <float>
V2 <float>
dV <float>
Incl <float>
ENA <float>
Coeff <float>
arrays
AbsPlot
<float values from 0.0 to 1.0 with size (nR + 1) x (nZ + 1), each value separated by space>
<empty string>
```

## Installation

### Method 1: Scoop

To install Gleipnir with [Scoop](https://scoop.sh/), you can add repo and install this program.

```sh
scoop bucket add shell https://github.com/deverte/scoop-shell
```

```sh
scoop install gleipnir
```

### Method 2: Download

Also you can [download](https://github.com/deverte/gleipnir/releases) a single executable file (`gleipnir.exe`) and use it like portable program.

## Dependencies

- [Matplotlib](https://matplotlib.org/)

## License

[MIT](LICENSE)