using System;

public class TaylorExpansion
{
    // This function calculates the Taylor series expansion for cos(x)
    // up to n terms. The series is: cos(x) = 1 - x^2/2! + x^4/4! - x^6/6! + ...
    public static double TaylorSeriesExpansion(double x, int n)
    {
        double sum = 0;
        for (int i = 0; i < n; i++)
        {
            // Calculate each term of the series
            sum += Math.Pow(-1, i) * Math.Pow(x, 2 * i) / Factorial(2 * i);
        }
        return sum;
    }

    // Helper function to calculate factorial of a number
    private static double Factorial(int n)
    {
        double result = 1;
        for (int i = 1; i <= n; i++)
        {
            result *= i;
        }
        return result;
    }
}