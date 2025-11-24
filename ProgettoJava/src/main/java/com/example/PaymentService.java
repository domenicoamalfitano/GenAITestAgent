package com.example;

public class PaymentService {
    private final PaymentGateway gateway;

    public PaymentService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public PaymentGateway getGateway() {
        return gateway;
    }

    public boolean processPayment(String accountId, double amount) {
        return gateway.charge(accountId, amount);
    }
}