package com.example;

public class Euro {
    private final int amount;

    public Euro(int amount) {
        this.amount = amount;
    }

    public int getAmount() {
        return amount;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Euro euro = (Euro) obj;
        return amount == euro.amount;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(amount);
    }

    @Override
    public String toString() {
        return amount + " EUR";
    }
}