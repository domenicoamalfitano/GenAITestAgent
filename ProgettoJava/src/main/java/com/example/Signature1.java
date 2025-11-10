package com.example;

public class Signature1 {
    public float divide(int num, int den) {
        if (den == 0) {
            return Float.NaN; // Handle division by zero
        }
        return (float) num / den;
    }
}