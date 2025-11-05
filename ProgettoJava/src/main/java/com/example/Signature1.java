package com.example;

import java.util.Arrays;

public class Signature1 {
    
    public float divide(int num, int den) {
        if (den == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return (float) num / den;
    }

    public int[] bubbleSort(int[] myArray) {
        int[] arr = Arrays.copyOf(myArray, myArray.length);
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        return arr;
    }
    
    public boolean isValidEmail(String email) {
        if (email == null) {
            return false;
        }
        String regex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
        return email.matches(regex);
    }
}