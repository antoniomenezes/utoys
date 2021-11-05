#!/usr/bin/python
# coding=utf-8

# Cálculo do DV do CPF de acordo com http://ghiorzi.org/DVnew.htm
def get_cpf_and_dv(value):
  primary_val = str(value)
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

