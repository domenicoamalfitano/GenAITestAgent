package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class Signature1Test {
    
    @Test
    @DisplayName("Test divide with positive numbers returns correct result")
    void testDividePositiveNumbers_returnsCorrectResult() {
        Signature1 instance = new Signature1();
        float result = instance.divide(4, 2);
        assertEquals(2.0f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide by zero throws ArithmeticException")
    void testDivideByZero_throwsArithmeticException() {
        Signature1 instance = new Signature1();
        assertThrows(ArithmeticException.class, () -> instance.divide(5, 0));
    }

    @Test
    @DisplayName("Test divide negative numerator by positive denominator returns correct result")
    void testDivideNegativeNumeratorByPositiveDenominator_returnsCorrectResult() {
        Signature1 instance = new Signature1();
        float result = instance.divide(-6, 3);
        assertEquals(-2.0f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide positive numerator by negative denominator returns correct result")
    void testDividePositiveNumeratorByNegativeDenominator_returnsCorrectResult() {
        Signature1 instance = new Signature1();
        float result = instance.divide(6, -3);
        assertEquals(-2.0f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide negative numerator by negative denominator returns correct result")
    void testDivideNegativeNumeratorByNegativeDenominator_returnsCorrectResult() {
        Signature1 instance = new Signature1();
        float result = instance.divide(-8, -4);
        assertEquals(2.0f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide zero numerator by positive denominator returns zero")
    void testDivideZeroNumeratorByPositiveDenominator_returnsZero() {
        Signature1 instance = new Signature1();
        float result = instance.divide(0, 5);
        assertEquals(0.0f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide 5 by 2 returns 2.5")
    void testDivideFiveByTwo_returnsTwoPointFive() {
        Signature1 instance = new Signature1();
        float result = instance.divide(5, 2);
        assertEquals(2.5f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide 10 by 3 returns 3.333")
    void testDivideTenByThree_returnsThreePointThreeThree() {
        Signature1 instance = new Signature1();
        float result = instance.divide(10, 3);
        assertEquals(3.333f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide by 1 returns numerator as float")
    void testDivideByOne_returnsNumeratorAsFloat() {
        Signature1 instance = new Signature1();
        float result = instance.divide(7, 1);
        assertEquals(7.0f, result, 0.001f);
    }

    @Test
    @DisplayName("Test divide 1 by 1000 returns 0.001")
    void testDivideOneByThousand_returnsZeroPointZeroZeroOne() {
        Signature1 instance = new Signature1();
        float result = instance.divide(1, 1000);
        assertEquals(0.001f, result, 0.001f);
    }

    @Test
    @DisplayName("Test unsorted array with bubbleSort returns sorted array")
    void testUnsortedArray_bubbleSort_returnsSortedArray() {
        Signature1 instance = new Signature1();
        int[] input = {3, 1, 2};
        int[] expected = {1, 2, 3};
        int[] result = instance.bubbleSort(input);
        assertArrayEquals(expected, result);
    }

    @Test
    @DisplayName("Test array with duplicates and negatives with bubbleSort returns sorted array")
    void testArrayWithDuplicatesAndNegatives_bubbleSort_returnsSortedArray() {
        Signature1 instance = new Signature1();
        int[] input = {5, -3, 0, 4, -3, 2};
        int[] expected = {-3, -3, 0, 2, 4, 5};
        int[] result = instance.bubbleSort(input);
        assertArrayEquals(expected, result);
    }

    @Test
    @DisplayName("Test reverse-sorted array with bubbleSort returns sorted array")
    void testReverseSortedArray_bubbleSort_returnsSortedArray() {
        Signature1 instance = new Signature1();
        int[] input = {5, 4, 3, 2, 1};
        int[] expected = {1, 2, 3, 4, 5};
        int[] result = instance.bubbleSort(input);
        assertArrayEquals(expected, result);
    }

    @Test
    @DisplayName("Test empty array with bubbleSort returns empty array")
    void testEmptyArray_bubbleSort_returnsEmptyArray() {
        Signature1 instance = new Signature1();
        int[] input = {};
        int[] expected = {};
        int[] result = instance.bubbleSort(input);
        assertArrayEquals(expected, result);
    }

    @Test
    @DisplayName("Test single-element array with bubbleSort returns same array")
    void testSingleElementArray_bubbleSort_returnsSameArray() {
        Signature1 instance = new Signature1();
        int[] input = {42};
        int[] expected = {42};
        int[] result = instance.bubbleSort(input);
        assertArrayEquals(expected, result);
    }

    @Test
    @DisplayName("Test array with multiple duplicates with bubbleSort returns sorted array")
    void testArrayWithMultipleDuplicates_bubbleSort_returnsSortedArray() {
        Signature1 instance = new Signature1();
        int[] input = {2, 1, 3, 3, 2};
        int[] expected = {1, 2, 2, 3, 3};
        int[] result = instance.bubbleSort(input);
        assertArrayEquals(expected, result);
    }

    @Test
    @DisplayName("Test valid standard email with isValidEmail returns true")
    void testValidStandardEmail_isValidEmail() {
        Signature1 instance = new Signature1();
        boolean result = instance.isValidEmail("user@example.com");
        assertTrue(result);
    }

    @Test
    @DisplayName("Test invalid email with no top-level domain returns false")
    void testInvalidEmailNoTopLevelDomain_isValidEmail() {
        Signature1 instance = new Signature1();
        boolean result = instance.isValidEmail("user@example");
        assertFalse(result);
    }

    @Test
    @DisplayName("Test valid email with special characters in local part returns true")
    void testValidEmailWithSpecialCharactersInLocalPart_isValidEmail() {
        Signature1 instance = new Signature1();
        boolean result = instance.isValidEmail("user+tag@example.com");
        assertTrue(result);
    }
}