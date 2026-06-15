package com.example;

public class InvalidArgumentException extends RuntimeException {
    public InvalidArgumentException(String message) {
        super(message);
    }
}