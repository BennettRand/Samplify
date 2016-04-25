# Samplify

[![Build Status](https://travis-ci.org/BennettRand/Samplify.svg?branch=master)](https://travis-ci.org/BennettRand/Samplify)

A library to keep track of magnitude and unit-aware measurements.

## Measure
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

## BaseUnits and DerivedUnits
Every single SI base unit is assigned a [Fraction](https://docs.python.org/2/library/fractions.html) object with the value of a prime number. This way, every single derived unit can be traced back to a combination of prime numbers.

For example,
> m = 2

and 
> s = 5

This means that
> speed = 2 / 5

and
> Hz = 1 / 5

The Fraction object is used because floating-point precision issues could lead to losing the uniqueness of prime numbers in an integer.

### BaseUnits

Unit | Abbreviation | Prime
---- | ------------ | -----
*No Unit* | | 1
Meter | m | 2
Gram | g | 3
Second | s | 5
Ampere | A | 7
Kelvin | K | 11
Mole | mol | 13
Candela | cd | 17
Power Factor | PF | 19

### DerivedUnits

Unit | Abbreviation | Fraction
---- | ------------ | -----
Hertz | Hz | 1 / s
Newton | N | m * g * s * s
Joule | J | N * m
Watt | W | J / s
Volt | V | W / A * PF
Voltampere | VA | W / PF

Power Factor is considered a base unit so that power computation models AC electricity. This can be switched by calling model_dc_power() and model_ac_power() at the start of an application.
