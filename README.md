# Measurements

[![Build Status](https://travis-ci.org/BennettRand/Measurements.svg?branch=master)](https://travis-ci.org/BennettRand/Measurements)

A library to keep track of magnitude and unit-aware measurements.

## SI
The foundation of all measurements. The objects will keep track of their magnitude, SI scale factor, and unit of measurement across math operations.

```python
one_kilometer = Measure(1, 'k', BaseUnits.m)
one_k_meters = Measure(1000, unit=BaseUnits.m)

assert(one_kilometer == one_k_meters)

assert(one_kilometer + one_kilometer == one_k_meters * 2)
```

Units can change if the math operation calls for it. Additionally, there are protections against doing invalid math operations across multiple incompatible units.

```python
one_hour = Measure(60*60, unit=BaseUnits.s)
G = Measure(9.81, unit=(BaseUnits.m / (BaseUnits.s * BaseUnits.s)))

one_kilometer_per_hour = one_kilometer / one_hour
speed_after_hour_of_falling = G * one_hour

assert(one_kilometer_per_hour.unit == BaseUnits.m / BaseUnits.s)
assert(one_kilometer_per_hour.unit == speed_after_hour_of_falling.unit)
```

The following works:
```python
final_speed = speed_after_hour_of_falling - one_kilometer_per_hour
```
However the following,
```python
should_error = speed_after_hour_of_falling + G
```
raises:
> UnitError: Incompatible units
