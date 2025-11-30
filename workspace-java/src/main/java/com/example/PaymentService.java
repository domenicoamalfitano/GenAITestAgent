package com.example;

public class PaymentService {
    
    private final PaymentGateway gateway;
    
    public PaymentService(PaymentGateway gateway) {
        if (gateway == null) {
            throw new IllegalArgumentException("PaymentGateway cannot be null");
        }
        this.gateway = gateway;
    }
    
    public PaymentGateway getGateway() {
        return gateway;
    }
    
    public boolean processPayment(String accountId, double amount) {
        validateAccountId(accountId);
        validateAmount(amount);
        return gateway.charge(accountId, amount);
    }
    
    private void validateAccountId(String accountId) {
        if (accountId == null || accountId.trim().isEmpty()) {
            throw new IllegalArgumentException("Account ID cannot be null or empty");
        }
    }
    
    private void validateAmount(double amount) {
        if (amount == 0.0) {
            throw new IllegalArgumentException("Amount cannot be zero");
        }
        if (amount < 0.0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
    }
}