package com.example; public class Signature1 { public float divide(int num, int den) { return (float) num / den; }

public float divide(int num, int den) { return (float) num / den; }

public int[] bubbleSort(int[] myArray) {
        int n = myArray.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (myArray[j] > myArray[j + 1]) {
                    // Swap elements
                    int temp = myArray[j];
                    myArray[j] = myArray[j + 1];
                    myArray[j + 1] = temp;
                }
            }
        }
        return myArray;
    }

public int[] bubbleSort(int[] myArray) {
        int n = myArray.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (myArray[j] > myArray[j + 1]) {
                    // Swap elements
                    int temp = myArray[j];
                    myArray[j] = myArray[j + 1];
                    myArray[j + 1] = temp;
                }
            }
        }
        return myArray;
    }

public boolean isValidEmail(String email) {
        // code here
    }

public boolean isValidEmail(String email) {
        String localPart = "";
        String domain = "";
        int atSignIndex = email.indexOf('@');

        if (atSignIndex == -1) {
            return false;
        }

        localPart = email.substring(0, atSignIndex);
        domain = email.substring(atSignIndex + 1);

        // Check for valid local part
        if (!localPart.matches("^[a-zA-Z0-9_]+$")) {
            return false;
        }

        // Check for valid domain
        if (!domain.matches("^[a-zA-Z0-9.]+$")) {
            return false;
        }

        return true;
    }
}