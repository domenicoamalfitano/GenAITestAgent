package com.example;

public interface PaymentGateway {
    boolean charge(String accountId, double amount);
}