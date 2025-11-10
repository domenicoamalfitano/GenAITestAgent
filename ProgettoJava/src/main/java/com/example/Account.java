package com.example;

public class Account {
    private int accountNumber;
    private int pin;
    private Euro availableBalance;
    private Euro totalBalance;

    // Existing constructor
    public Account(int theAccountNumber, int thePIN, Euro theAvailableBalance, Euro theTotalBalance) {
        if (theAvailableBalance == null) {
            throw new NullPointerException("Available balance cannot be null");
        }
        if (theTotalBalance == null) {
            throw new NullPointerException("Total balance cannot be null");
        }
        this.accountNumber = theAccountNumber;
        this.pin = thePIN;
        this.availableBalance = theAvailableBalance;
        this.totalBalance = theTotalBalance;
    }

    // Added no‑argument constructor required by tests
    public Account() {
        this.accountNumber = 0;
        this.pin = 0;
        this.availableBalance = new Euro(0);
        this.totalBalance = new Euro(0);
    }

    public int getAccountNumber() {
        return accountNumber;
    }

    public int getPIN() {
        return pin;
    }

    public Euro getAvailableBalance() {
        return availableBalance;
    }

    public Euro getTotalBalance() {
        return totalBalance;
    }

    /**
     * Validates the provided PIN against the stored PIN.
     *
     * @param userPIN the PIN entered by the user
     * @return true if the provided PIN matches the stored PIN, false otherwise
     */
    public boolean validatePIN(int userPIN) {
        return this.pin == userPIN;
    }

    /**
     * Credits the specified amount to the total balance.
     *
     * @param amount the amount to credit; must not be null
     */
    public void credit(Euro amount) {
        if (amount == null) {
            throw new NullPointerException("Credit amount cannot be null");
        }
        // Assuming Euro provides an add method that returns a new Euro instance
        this.totalBalance = this.totalBalance.add(amount);
    }
}