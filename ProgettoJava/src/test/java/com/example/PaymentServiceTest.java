package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PaymentServiceTest {

    @Test
    @DisplayName("constructor should store the provided PaymentGateway")
    void constructorShouldStoreProvidedGateway() {
        PaymentGateway mockGateway = mock(PaymentGateway.class);
        PaymentService service = new PaymentService(mockGateway);
        assertEquals(mockGateway, service.getGateway());
    }

    @Test
    @DisplayName("constructor should throw IllegalArgumentException when null gateway is provided")
    void constructorShouldThrowExceptionWhenNullGatewayProvided() {
        assertThrows(IllegalArgumentException.class, () -> {
            new PaymentService(null);
        });
    }

    @Test
    @DisplayName("processPayment should throw IllegalArgumentException when amount is zero")
    void processPaymentShouldThrowExceptionWhenAmountIsZero() {
        PaymentGateway mockGateway = mock(PaymentGateway.class);
        PaymentService service = new PaymentService(mockGateway);
        assertThrows(IllegalArgumentException.class, () -> {
            service.processPayment("acc123", 0.0);
        });
    }

    @Test
    @DisplayName("processPayment should throw IllegalArgumentException when amount is negative")
    void processPaymentShouldThrowExceptionWhenAmountIsNegative() {
        PaymentGateway mockGateway = mock(PaymentGateway.class);
        PaymentService service = new PaymentService(mockGateway);
        assertThrows(IllegalArgumentException.class, () -> {
            service.processPayment("acc123", -10.0);
        });
    }

    @Test
    @DisplayName("processPayment should return the result of gateway.charge when amount is positive")
    void processPaymentShouldReturnGatewayChargeResultWhenAmountPositive() {
        PaymentGateway mockGateway = mock(PaymentGateway.class);
        when(mockGateway.charge("acc123", 50.0)).thenReturn(true);
        PaymentService service = new PaymentService(mockGateway);
        boolean result = service.processPayment("acc123", 50.0);
        assertTrue(result);
        verify(mockGateway).charge("acc123", 50.0);
    }

}