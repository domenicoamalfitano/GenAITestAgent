package com.example;

public class RomanConverter {

    // Roman numeral value constants for readability
    private static final int I_VALUE = 1;
    private static final int V_VALUE = 5;
    private static final int X_VALUE = 10;
    private static final int L_VALUE = 50;
    private static final int C_VALUE = 100;
    private static final int D_VALUE = 500;
    private static final int M_VALUE = 1000;

    /**
     * Converts a Roman numeral string to its Arabic number representation.
     *
     * @param roman the Roman numeral string (case-insensitive)
     * @return the integer value of the Roman numeral
     * @throws InvalidArgumentException if the input contains invalid characters or is null/empty
     */
    public static int convertRomanToArabicNumber(String roman) {
        if (roman == null || roman.isEmpty()) {
            throw new InvalidArgumentException("Roman numeral must not be null or empty");
        }
        // Normalize to uppercase to handle lowercase inputs
        roman = roman.toUpperCase();
        int total = 0;
        int previousValue = 0;
        for (int i = roman.length() - 1; i >= 0; i--) {
            char c = roman.charAt(i);
            int value = romanCharToInt(c);
            if (value < 0) {
                throw new InvalidArgumentException("Invalid Roman numeral character: " + c);
            }
            if (value < previousValue) {
                total -= value;
            } else {
                total += value;
                previousValue = value;
            }
        }
        return total;
    }

    private static int romanCharToInt(char c) {
        return switch (c) {
            case 'I' -> I_VALUE;
            case 'V' -> V_VALUE;
            case 'X' -> X_VALUE;
            case 'L' -> L_VALUE;
            case 'C' -> C_VALUE;
            case 'D' -> D_VALUE;
            case 'M' -> M_VALUE;
            default -> -1;
        };
    }
}