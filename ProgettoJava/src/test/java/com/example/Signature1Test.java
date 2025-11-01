package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class Signature1Test {

    @Test
    @DisplayName("Test divide with positive numbers")
    public void testDividePositive() {
        Signature1 signature1 = new Signature1();
        assertEquals(0.5f, signature1.divide(2, 4), "Division of two positive numbers");
    }

    @Test
    @DisplayName("Test divide with zero denominator")
    public void testDivideZeroDenominator() {
        Signature1 signature1 = new Signature1();
        assertThrows(ArithmeticException.class, () -> signature1.divide(2, 0), "Division by zero");
    }

    @Test
    @DisplayName("Test divide with negative numbers")
    public void testDivideNegative() {
        Signature1 signature1 = new Signature1();
        assertEquals(-0.5f, signature1.divide(-2, 4), "Division of two negative numbers");
    }

    @Test
    @DisplayName("Test divide with zero numerator and denominator")
    public void testDivideZeroNumeratorAndDenominator() {
        Signature1 signature1 = new Signature1();
        assertEquals(0.0f, signature1.divide(0, 4), "Division of zero by a number");
    }

    @Test
    @DisplayName("Test divide with very large numbers")
    public void testDivideLargeNumbers() {
        Signature1 signature1 = new Signature1();
        assertEquals(1000000.0f, signature1.divide(2000000, 2), "Division of two large numbers");
    }

    @Test
    @DisplayName("Test divide with very small numbers")
    public void testDivideSmallNumbers() {
        Signature1 signature1 = new Signature1();
        assertEquals(-0.5f, signature1.divide(-10000, 20000), "Division of two small negative numbers");
    }

    @Test
    @DisplayName("Test divide with same numerator and denominator")
    public void testDivideSameNumbers() {
        Signature1 signature1 = new Signature1();
        assertEquals(1.0f, signature1.divide(2, 2), "Division of the same number by itself");
    }

    @Test
    @DisplayName("Test divide with very large numerator and small denominator")
    public void testDivideLargeNumeratorSmallDenominator() {
        Signature1 signature1 = new Signature1();
        assertEquals(500000.0f, signature1.divide(1000000, 2), "Division of a large number by a small number");
    }

    @Test
    @DisplayName("Test divide with very small numerator and large denominator")
    public void testDivideSmallNumeratorLargeDenominator() {
        Signature1 signature1 = new Signature1();
        assertEquals(-0.25f, signature1.divide(-10000, 40000), "Division of a small negative number by a large positive number");
    }

@Test
    @DisplayName("Test 1: Empty array")
    public void testEmptyArray() {
        Signature1 myClass = new Signature1();
        int[] myArray = {};
        int[] expected = {};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 2: Single element array")
    public void testSingleElementArray() {
        Signature1 myClass = new Signature1();
        int[] myArray = {5};
        int[] expected = {5};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 3: Two element array in ascending order")
    public void testTwoElementArrayAscendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {2, 4};
        int[] expected = {2, 4};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 4: Two element array in descending order")
    public void testTwoElementArrayDescendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {4, 2};
        int[] expected = {2, 4};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 5: Three element array in ascending order")
    public void testThreeElementArrayAscendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {1, 3, 2};
        int[] expected = {1, 2, 3};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 6: Three element array in descending order")
    public void testThreeElementArrayDescendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {3, 2, 1};
        int[] expected = {1, 2, 3};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 7: Four element array in ascending order")
    public void testFourElementArrayAscendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {1, 2, 3, 4};
        int[] expected = {1, 2, 3, 4};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 8: Four element array in descending order")
    public void testFourElementArrayDescendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {4, 3, 2, 1};
        int[] expected = {1, 2, 3, 4};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 9: Five element array in ascending order")
    public void testFiveElementArrayAscendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {1, 2, 3, 4, 5};
        int[] expected = {1, 2, 3, 4, 5};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }

    @Test
    @DisplayName("Test 10: Five element array in descending order")
    public void testFiveElementArrayDescendingOrder() {
        Signature1 myClass = new Signature1();
        int[] myArray = {5, 4, 3, 2, 1};
        int[] expected = {1, 2, 3, 4, 5};
        assertArrayEquals(expected, myClass.bubbleSort(myArray));
    }
}