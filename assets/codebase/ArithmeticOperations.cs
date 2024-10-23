using System;

public class ArithmeticOperations
{
    // Function to add two numbers
    public static float Add(float a, float b)
    {
        return a + b;
    }

    // Function to subtract the second number from the first
    public static float Subtract(float a, float b)
    {
        return a - b;
    }

    // Function to multiply two numbers
    public static float Multiply(float a, float b)
    {
        return a * b;
    }

    // Function to divide the first number by the second
    // Returns NaN if division by zero is attempted
    public static float Divide(float a, float b)
    {
        if (b == 0)
        {
            Console.WriteLine("Error: Division by zero");
            return float.NaN;
        }
        return a / b;
    }
}