package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

public class PaymentServiceTest {

    @Mock
    private PaymentGateway mockGateway;

    @Test
    @DisplayName("should initialize PaymentService with provided gateway")
    public void shouldInitializePaymentServiceWithProvidedGateway() {
        MockitoAnnotations.openMocks(this);
        PaymentService service = new PaymentService(mockGateway);
        assertEquals(mockGateway, service.getGateway());
    }

    @Test
    @DisplayName("should return true when payment gateway charge returns true")
    public void shouldReturnTrueWhenGatewayChargeReturnsTrue() {
        MockitoAnnotations.openMocks(this);
        when(mockGateway.charge("acc123", 100.0)).thenReturn(true);
        PaymentService service = new PaymentService(mockGateway);
        boolean result = service.processPayment("acc123", 100.0);
        assertTrue(result);
    }

    @Test
    @DisplayName("should return false when payment gateway charge returns false")
    public void shouldReturnFalseWhenGatewayChargeReturnsFalse() {
        MockitoAnnotations.openMocks(this);
        when(mockGateway.charge("acc456", 50.0)).thenReturn(false);
        PaymentService service = new PaymentService(mockGateway);
        boolean result = service.processPayment("acc456", 50.0);
        assertFalse(result);
    }
}