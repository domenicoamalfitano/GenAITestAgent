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
            service.processPayment("account123", 0.0);
        });
    }

    @Test
    @DisplayName("processPayment should return false when PaymentGateway charge returns false")
    void processPaymentShouldReturnFalseWhenGatewayChargeReturnsFalse() {
        PaymentGateway mockGateway = mock(PaymentGateway.class);
        when(mockGateway.charge("account123", 10.0)).thenReturn(false);
        PaymentService service = new PaymentService(mockGateway);
        boolean result = service.processPayment("account123", 10.0);
        assertFalse(result);
    }
}