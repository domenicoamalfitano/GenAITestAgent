package com.example;

import java.net.IDN;
import java.util.regex.Pattern;

public class MyClass {
    public int sum(int a, int b) {
        return a+b;
    }

    public float divide(int num, int den) {
        return num/den;
    }

    public static int max(int[] array, int n)
    {
        int max=0;
        for(int i=0;i<n;i++){
            if(array[i]>max)
                max=array[i];
        }
        return max;
    }

    public String reverse(String s){
        int n = s.length();
        char[] out = new char[n];
        for (int i = 0; i < n; i++) {
            out[n - 1 - i] = s.charAt(i);
        }
        return new String(out);
    }

    public static int[] bubbleSort(int[] myArray) {

        int temp = 0;  //  temporary element for swapping
        int counter = 0;

        for (int i = 0; i < myArray.length; i++) {
            counter = i + 1;
            for (int j = 1; j < (myArray.length - i); j++) {

                if (myArray[j - 1] > myArray[j]) {
                    //  swap array’s elements using temporary element
                    temp = myArray[j - 1];
                    myArray[j - 1] = myArray[j];
                    myArray[j] = temp;
                }
            }
        }
        System.out.println("Steps quantity, non optimized = " + counter);
        return myArray;
    }

    // Caratteri ammessi nella parte locale (versione semplificata RFC 5322)
    private static final Pattern LOCAL_PART_PATTERN =
            Pattern.compile("^[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+$");

    // Etichetta di dominio: no trattino all’inizio/fine, 1..63, solo [A-Za-z0-9-]
    private static final Pattern DOMAIN_LABEL_PATTERN =
            Pattern.compile("^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$");

    /**
     * Valida un indirizzo email.
     * Regole principali:
     * - Formato <local>@<domain>, una sola '@'
     * - Lunghezza totale <= 254, local <= 64
     * - Parte locale: caratteri consentiti, niente "..", niente punto all'inizio/fine
     * - Dominio: supporto IDN (unicode -> punycode), lunghezza totale <= 253
     *   e ogni etichetta 1..63 con caratteri validi.
     */
    public static boolean isValidEmail(String email) {
        if (email == null) return false;

        String trimmed = email.trim();
        if (trimmed.isEmpty()) return false;

        // Lunghezza massima standard
        if (trimmed.length() > 254) return false;

        // Deve contenere una sola '@'
        int at = trimmed.indexOf('@');
        if (at <= 0 || at != trimmed.lastIndexOf('@') || at == trimmed.length() - 1) {
            return false;
        }

        String local = trimmed.substring(0, at);
        String domain = trimmed.substring(at + 1);

        // Parte locale: max 64, caratteri ammessi, niente punti doppi o ai bordi
        if (local.length() > 64) return false;
        if (!LOCAL_PART_PATTERN.matcher(local).matches()) return false;
        if (local.startsWith(".") || local.endsWith(".") || local.contains("..")) return false;

        // Dominio: consenti Unicode ma valida sul punycode
        String asciiDomain;
        try {
            asciiDomain = IDN.toASCII(domain, IDN.ALLOW_UNASSIGNED);
        } catch (IllegalArgumentException e) {
            return false;
        }

        // Lunghezze dominio
        if (asciiDomain.length() == 0 || asciiDomain.length() > 253) return false;
        if (asciiDomain.endsWith(".")) return false; // niente punto finale

        String[] labels = asciiDomain.split("\\.");
        if (labels.length < 2) return false; // richiedi almeno un TLD

        for (String label : labels) {
            if (label.length() == 0 || label.length() > 63) return false;
            if (!DOMAIN_LABEL_PATTERN.matcher(label).matches()) return false;
        }

        return true;
    }

    // Esempiolino rapido
    public static void main(String[] args) {
        String[] tests = {
                "alice@example.com",
                "a.b+c_d-1@example.co.uk",
                "utente@dominio.it",
                "nome.cognome@azienda-mia.eu",
                "üñîçøðé@dòmain.it",               // IDN
                ".alice@example.com",              // no
                "alice.@example.com",              // no
                "al..ice@example.com",             // no
                "alice@-example.com",              // no
                "alice@example-.com",              // no
                "alice@example..com",              // no
                "alice@exa_mple.com",              // no
                "toolonglocalparttoolonglocalparttoolonglocalparttoolong@example.com" // no
        };
        for (String t : tests) {
            System.out.printf("%-50s -> %s%n", t, isValidEmail(t));
        }
    }
}