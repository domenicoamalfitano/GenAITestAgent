package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Assertions;

public class RomanConverterTest {

    @Test
    @DisplayName("convertRomanToArabicNumber should throw InvalidArgumentException for invalid characters")
    public void testConvertRomanToArabicNumber_InvalidCharacter_ThrowsException() {
        RomanConverter converter = new RomanConverter();
        Assertions.assertThrows(InvalidArgumentException.class, () -> {
            converter.convertRomanToArabicNumber("ABC");
        });
    }

    @Test
    @DisplayName("convertRomanToArabicNumber should correctly convert lowercase roman numerals to arabic")
    public void testConvertRomanToArabicNumber_LowercaseInput_ReturnsCorrectValue() {
        RomanConverter converter = new RomanConverter();
        int result = converter.convertRomanToArabicNumber("xvii");
        Assertions.assertEquals(17, result);
    }
}