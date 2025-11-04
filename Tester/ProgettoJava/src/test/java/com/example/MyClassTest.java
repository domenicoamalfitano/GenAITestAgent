package com.example;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
/**
 * Javadoc for MyClassTest
 */
public class MyClassTest {
    @Test
    void testBubbleSortEmptyArray() {
        int[] myArray = new int[0];
        int[] result = MyClass.bubbleSort(myArray);
        assertEquals(0, result.length);
    }
    
    @Test
    void testBubbleSortSingleElement() {
        int[] myArray = new int[]{5};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{5}, result);
    }
    
    @Test
    void testBubbleSortAlreadySorted() {
        int[] myArray = new int[]{1, 2, 3, 4, 5};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{1, 2, 3, 4, 5}, result);
    }
    
    @Test
    void testBubbleSortReverseSorted() {
        int[] myArray = new int[]{5, 4, 3, 2, 1};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{1, 2, 3, 4, 5}, result);
    }
    
    @Test
    void testBubbleSortDuplicateElements() {
        int[] myArray = new int[]{2, 2, 1, 3, 3};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{1, 2, 2, 3, 3}, result);
    }
    
    @Test
    void testBubbleSortNegativeElements() {
        int[] myArray = new int[]{-5, -4, -3, -2, -1};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{-5, -4, -3, -2, -1}, result);
    }
    
    @Test
    void testBubbleSortVerySmallElements() {
        int[] myArray = new int[]{-1000, 500, 200, 10};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{-1000, -200, -10, 10, 500}, result);
    }
    
    @Test
    void testBubbleSortVeryLargeElements() {
        int[] myArray = new int[]{1000000, 500000, 200000, 10000};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{1000000, 500000, 200000, 10000}, result);
    }
    
    @Test
    void testBubbleSortMixedElements() {
        int[] myArray = new int[]{-5, 2, -3, 4, 1};
        int[] result = MyClass.bubbleSort(myArray);
        assertArrayEquals(new int[]{-5, -3, 1, 2, 4}, result);
    }
}

Thought:
Action: run_maven_tests
Action Input: