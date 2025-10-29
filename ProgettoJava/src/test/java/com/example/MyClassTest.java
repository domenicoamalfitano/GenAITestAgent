package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class MyClassTest {
    @Test
    @DisplayName("Test Division Small Numbers")
    void testDivisionSmallNumbers() {
        MyClass myClass = new MyClass();
        float result = myClass.divide(2, 4);
        assertEquals(0.5f, result);
    }

    @Test
    @DisplayName("Test Division Negative Denominator")
    void testDivisionNegativeDenomination() {
        MyClass myClass = new MyClass();
        assertThrows(ArithmeticException.class, () -> myClass.divide(1, -2));
    }

    @Test
    @DisplayName("Test Division Mixed Signs")
    void testDivisionMixedSigns() {
        MyClass myClass = new MyClass();
        float result = myClass.divide(-2, 3);
        assertEquals(-0.666f, result);
    }

    // Add more test cases here...
}