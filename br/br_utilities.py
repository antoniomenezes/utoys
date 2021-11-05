#!/usr/bin/python
# coding=utf-8

# The CPF number is the Brazilian individual taxpayer registry identification.
# It is an 11-digit number in the format 000.000.000-00.
# There is a two digit verification value (DV) used for CPF.
# The following code was based on http://ghiorzi.org/DVnew.htm

# Returns the first 9 CPF digits concatenated to DV digits
def get_cpf_and_dv(value):
  primary_val = str(value).rjust(9,'0')
  sum1 = 0
  sum2 = 0
  for i in range(len(primary_val)):
    sum1 += int(primary_val[i]) * (i+1)
  digit1 = sum1 % 11
  if digit1 == 10:
    digit1 = 0

  for j in range(len(primary_val+str(digit1))):
    sum2 += int((primary_val+str(digit1))[j]) * (j)
  digit2 = sum2 % 11
  if digit2 == 10:
    digit2 = 0

  return primary_val + str(digit1) + str(digit2)

