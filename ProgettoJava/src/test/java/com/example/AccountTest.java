package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Assertions;

public class AccountTest {

    @Test
    @DisplayName("Constructor initializes account number, PIN, available balance, and total balance correctly")
    public void testConstructorInitializesFieldsCorrectly() {
        int accountNumber = 123456;
        int pin = 1234;
        Euro availableBalance = new Euro(1000);
        Euro totalBalance = new Euro(1500);

        Account account = new Account(accountNumber, pin, availableBalance, totalBalance);

        Assertions.assertNotNull(account, "Account object should not be null");
        Assertions.assertEquals(accountNumber, account.getAccountNumber(), "Account number should be set correctly");
        Assertions.assertEquals(pin, account.getPIN(), "PIN should be set correctly");
        Assertions.assertEquals(availableBalance, account.getAvailableBalance(), "Available balance should be set correctly");
        Assertions.assertEquals(totalBalance, account.getTotalBalance(), "Total balance should be set correctly");
    }

    @Test
    @DisplayName("Constructor throws NullPointerException when available balance is null")
    public void testConstructorThrowsWhenAvailableBalanceIsNull() {
        int accountNumber = 123456;
        int pin = 1234;
        Euro availableBalance = null;
        Euro totalBalance = new Euro(1500);

        Assertions.assertThrows(NullPointerException.class, () -> {
            new Account(accountNumber, pin, availableBalance, totalBalance);
        }, "Constructor should throw NullPointerException if available balance is null");
    }

    @Test
    @DisplayName("Constructor throws NullPointerException when total balance is null")
    public void testConstructorThrowsWhenTotalBalanceIsNull() {
        int accountNumber = 123456;
        int pin = 1234;
        Euro availableBalance = new Euro(1000);
        Euro totalBalance = null;

        Assertions.assertThrows(NullPointerException.class, () -> {
            new Account(accountNumber, pin, availableBalance, totalBalance);
        }, "Constructor should throw NullPointerException if total balance is null");
    }

    @Test
    @DisplayName("validatePIN returns true when user PIN matches stored PIN")
    public void testValidatePINReturnsTrueForMatchingPIN() {
        int accountNumber = 123456;
        int pin = 4321;
        Euro availableBalance = new Euro(1000);
        Euro totalBalance = new Euro(1500);
        Account account = new Account(accountNumber, pin, availableBalance, totalBalance);
        Assertions.assertTrue(account.validatePIN(pin), "validatePIN should return true for matching PIN");
    }

    @Test
    @DisplayName("validatePIN returns false when user PIN does not match stored PIN")
    public void testValidatePINReturnsFalseForNonMatchingPIN() {
        int accountNumber = 123456;
        int correctPin = 4321;
        int wrongPin = 1234;
        Euro availableBalance = new Euro(1000);
        Euro totalBalance = new Euro(1500);
        Account account = new Account(accountNumber, correctPin, availableBalance, totalBalance);
        Assertions.assertFalse(account.validatePIN(wrongPin), "validatePIN should return false for non‑matching PIN");
    }

    @Test
    @DisplayName("credit adds the specified amount to the total balance")
    public void testCreditAddsAmountToTotalBalance() {
        Account account = new Account();
        Euro creditAmount = new Euro(250);
        account.credit(creditAmount);
        Assertions.assertEquals(creditAmount, account.getTotalBalance(), "Total balance should reflect credited amount");
    }
}