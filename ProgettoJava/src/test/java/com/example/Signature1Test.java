package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class Signature1Test {
    @Test
    @DisplayName("Test divide with positive numbers")
    public void testDividePositive() {
        Signature1 signature1 = new Signature1();
        assertEquals(0.5, signature1.divide(2, 4), "Expected division to be 0.5");
    }

    // Add more test cases here...

@Test
    @DisplayName("Valid email test")
    void validEmailTest() {
        Signature1 signature1 = new Signature1();
        assertTrue(signature1.isValidEmail("localpart@domain.tld"));
    }

    @Test
    @DisplayName("Invalid email test (no '@')")
    void invalidEmailNoAtTest() {
        Signature1 signature1 = new Signature1();
        assertFalse(signature1.isValidEmail("localpartdomain.tld"));
    }

    @Test
    @DisplayName("Invalid email test (no domain)")
    void invalidEmailNoDomainTest() {
        Signature1 signature1 = new Signature1();
        assertFalse(signature1.isValidEmail("localpart@"));
    }

    @Test
    @DisplayName("Valid email test with dots")
    void validEmailWithDotsTest() {
        Signature1 signature1 = new Signature1();
        assertTrue(signature1.isValidEmail("local.part@domain.tld"));
    }

    @Test
    @DisplayName("Invalid email test (extra characters)")
    void invalidEmailExtraCharsTest() {
        Signature1 signature1 = new Signature1();
        assertFalse(signature1.isValidEmail("localpart@domain.tld!"));
    }

    @Test
    @DisplayName("Valid email test with plus sign")
    void validEmailWithPlusSignTest() {
        Signature1 signature1 = new Signature1();
        assertTrue(signature1.isValidEmail("local+part@domain.tld"));
    }

    @Test
    @DisplayName("Invalid email test (no local part)")
    void invalidEmailNoLocalPartTest() {
        Signature1 signature1 = new Signature1();
        assertFalse(signature1.isValidEmail("@domain.tld"));
    }

    @Test
    @DisplayName("Valid email test with hyphen")
    void validEmailWithHyphenTest() {
        Signature1 signature1 = new Signature1();
        assertTrue(signature1.isValidEmail("local-part@domain.tld"));
    }

    @Test
    @DisplayName("Invalid email test (no '@' at the end)")
    void invalidEmailNoAtEndTest() {
        Signature1 signature1 = new Signature1();
        assertFalse(signature1.isValidEmail("localpart@domain"));
    }

    @Test
    @DisplayName("Valid email test with subdomain")
    void validEmailWithSubdomainTest() {
        Signature1 signature1 = new Signature1();
        assertTrue(signature1.isValidEmail("localpart@subdomain.domain.tld"));
    }

    @Test
    @DisplayName("Invalid email test (no local part and no domain)")
    void invalidEmailNoLocalPartAndDomainTest() {
        Signature1 signature1 = new Signature1();
        assertFalse(signature1.isValidEmail(""));
    }
}